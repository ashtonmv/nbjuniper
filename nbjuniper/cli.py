#!/usr/bin/env python

"""Converts notebooks to interactive HTML pages with Juniper + Binder.

Usage:
  nbjuniper NOTEBOOK (-f juniper_settings.yaml)
  nbinteract (-h | --help)

`nbinteract NOTEBOOK ...` converts notebooks into HTML pages.

Arguments:
  NOTEBOOK   IPython notebook to convert.

Options:
  -h --help                  Show this screen.
  -f FILENAME                yaml file containing specific settings for the Juniper client.
                             See https://github.com/ines/juniper for all possibilities.
"""

import json
import yaml
import sys
from markdown import markdown

def main():

    juniper_settings = {
        "url": "https://mybinder.org",
        "repo": "ashtonmv/python_binder",
        "theme": "callysto",
        "msgLoading": " ",
        "useStorage": True,
        "isolateCells": False
    }

    notebook = None
    for i, arg in enumerate(sys.argv):
        if i == 1:
            with open(arg) as f:
                notebook = json.load(f)

        if arg == "-f":
            with open(sys.argv[i+1]) as f:
                juniper_settings.update(yaml.safe_load(f))

        if arg == "--binderhub":
            juniper_settings.update({"url": sys.argv[i+1]})

        if arg == "--repo":
            juniper_settings.update({"repo": sys.argv[i+1]})

    if notebook is None or "cells" not in notebook:
        raise ValueError("Please specify a valid notebook to convert: nbjuniper example_notebook.ipynb")

    for k, v in juniper_settings.items():
        if type(v) != bool:
            juniper_settings[k] = f"'{v}'"
        else:
            juniper_settings[k] = str(v).lower()

    juniper_json = ", ".join([f"{key}: {value}" for key, value in juniper_settings.items()]) 

    head = [
        "<head>",
        "  <script type='text/javascript' src='https://code.jquery.com/jquery-3.5.1.min.js'></script>",
        "  <script type='text/javascript' src='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/cdn/juniper.min.js'></script>",
        "  <script type='text/javascript' src='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/cdn/events.js'></script>",
        "  <script type='text/javascript' src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>",
        f"  <script>$(document).ready(function() {{new Juniper({{ {juniper_json} }})}});</script>",
        "  <link rel='stylesheet' href='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/cdn/style.css'></link>",
        "</head>",
    ]

    body = ["<body>"]
    body.append("<div class='juniper-notebook'>")
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            body.append("<pre data-executable>")
            body.append("".join(cell["source"]))
            body.append("</pre>")
        else:
            body.append(markdown("".join(cell["source"])))
    body.append("</div>")
    body.append("</body>")

    if "--no-head" not in sys.argv and "--decapitate" not in sys.argv:
        with open(sys.argv[1].replace("ipynb", "html"), "w") as o:
            o.write("\n".join(head))
            o.write("\n".join(body))
    else:
        if "--no-head" not in sys.argv:
            with open("juniper_head.html", "w") as o:
                o.write("\n".join(head))
        with open(sys.argv[1].replace("ipynb", "html"), "w") as o:
            o.write("\n".join(body))
   

if __name__ == "__main__":
    main()