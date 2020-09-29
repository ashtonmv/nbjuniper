#!/usr/bin/env python

import json
import sys
from markdown import markdown

with open(sys.argv[1]) as i:
    notebook = json.load(i)

url = "https://mybinder.org"
repo = "ashtonmv/conda"
theme = "callysto"

language = notebook["metadata"]["kernelspec"]["language"]

content = [
    "<script src='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/juniper.min.js'></script>",
    "<script src='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/events.js'></script>",
    "<link rel='stylesheet' href='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/style.css'></link>",
    "<div class='notebook'>"
]

for cell in notebook["cells"]:
    if cell["cell_type"] == "code":
        content.append("      <pre data-executable>")
        content.append("".join(cell["source"]))
        content.append("</pre>")
    else:
        content.append(markdown("".join(cell["source"])))

content.append("</div>")

content.append(f"<script>new Juniper({{url: '{url}', repo: '{repo}', theme: '{theme}'}});</script>")

with open(sys.argv[2], "w") as o:
    o.write("\n".join(content)) 