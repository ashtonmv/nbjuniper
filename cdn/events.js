// Start the Juniper connection to the Binder kernel
function startKernel(juniperInstance) {
    juniperInstance._event('requesting-kernel');

    for (var i=0; i<$(".juniper-button").length; i++) {
        var button = $(".juniper-button")[i];
        $(button).html("<div class='spinner'><div class='bounce1'></div><div class='bounce2'></div><div class='bounce3'></div></div>");
    }

    for (var i=0; i<$(".juniper-output").length; i++) {
        var output = $(".juniper-output")[i];
        $(output).append("<p class='temporaryMsg'>Connecting to kernel...</p>");
    }

    if (juniperInstance._kernel && juniperInstance.isolateCells) {
        juniperInstance._kernel.restart();
    }
    new Promise((resolve, reject) =>
    juniperInstance.getKernel().then(resolve).catch(reject))
    .then(kernel => {
        juniperInstance._kernel = kernel;
    })
    .catch(() => {
        juniperInstance._event('failed');
        juniperInstance._kernel = null;
        if (juniperInstance.useStorage && typeof window !== 'undefined') {
            juniperInstance._fromStorage = false;
            window.localStorage.removeItem(juniperInstance.storageKey);
        }
    })
}

// Kernel is ready to go, so make cells executable
document.addEventListener('juniper', event => {
    if (event.detail.status == 'ready') {
        for (var i=0; i<$(".juniper-button").length; i++) {
            var button = $(".juniper-button")[i];
            $(button).text("run");
        }
        for (var i=0; i<$(".temporaryMsg").length; i++) {
            $(".temporaryMsg")[i].hide();
        }
    }
})

// Listen for events sent back by the jupyterlab KernelFutureHandler
// as cellExecuted (the name I gave them in juniper.min.js)
document.addEventListener("cellExecuted", event => {
    if (event.detail.content.execution_count) {
        var activeCell = $(".juniper-cell.active").first();
        $(activeCell).removeClass("active");

        // Display In[n], like on most jupyter servers
        var activeButton = $(activeCell).find(".juniper-button").first();
        $(activeButton).text("In [" + event.detail.content.execution_count + "]");

        // Should either be "ok" or "error"
        var status = event.detail.content.status;

        // Color the tab based on the response
        if (status == "ok") {
            // make the tab green
            $(activeButton).addClass("finished");
        } else if (status == "error") {
            // make the tab red
            $(activeButton).addClass("errored");
        }
    };
});

// Select the actively running juniper cell.
document.addEventListener('juniper', event => {
    if (event.detail.status == 'executing') {
        var div1 = $(event.target.activeElement).parent();

        // if the juniper-button was clicked
        if ($(div1).hasClass("juniper-cell")) {
            var activeCell = $(div1);
        }

        // if the cell was run using shift-enter
        else {
            var codeMirror = $(div1).parent();
            var juniperInput = $(codeMirror).parent();
            var activeCell = $(juniperInput).parent();            
        }

        $(activeCell).addClass("active");

        // Display loading animation
        var activeButton = $(activeCell).find(".juniper-button").first();
        $(activeButton).html("<div class='spinner'><div class='bounce1'></div><div class='bounce2'></div><div class='bounce3'></div></div>");
    }
})

// Select the actively running juniper cell.
document.addEventListener('juniper', event => {
    if (event.detail.status == 'failed') {
        var div1 = $(event.target.activeElement).parent();

        // If loading the kernel failed
        console.log($(div1).attr("onclick"));
        if ($(div1).attr("onclick") == "juniperInit()") {
            for (var i=0; i<$(".juniper-button").length; i++) {
                var button = $(".juniper-button")[i];
                $(button).text("reload");
                $(button).removeClass("finished");
                $(button).addClass("errored");
            }
            for (var i=0; i<$(".temporaryMsg").length; i++) {
                $(".temporaryMsg")[i].hide();
            }
        }

        // If execution of a cell failed
        else {
            // if a juniper-button was clicked
            if ($(div1).hasClass("juniper-cell")) {
                var activeCell = $(div1);
            }

            // if the cell was run using shift-enter
            else {
                var codeMirror = $(div1).parent();
                var juniperInput = $(codeMirror).parent();
                var activeCell = $(juniperInput).parent();            
            }

            // make the output area yellow
            var activeButton = $(activeCell).find(".juniper-button").first();
            $(activeButton).removeClass("finished");
            $(activeButton).addClass("errored");

            // Display In[*], like on most jupyter servers
            $(activeButton).text("In []");
        }
    }
})