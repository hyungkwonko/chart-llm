# cd vizeitgeist
# python -m http.server

def change_var(i):
    return """<!DOCTYPE html>
    <html>

    <head>
    <title>Embedding Vega-Lite</title>
    <script src="https://cdn.jsdelivr.net/npm/vega@5.25.0"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@5.9.0"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6.22.1"></script>
    <style>
        .button {
            display: inline-block;
            width: 80px;
            height: 15px;
            background: #4E9CAF;
            padding: 10px;
            text-align: center;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            line-height: 15px;
        }
        .container {
            height: 1000px;
            width: 1000px;
        }
    </style>

    </head>

    <body>
    <h2> CHART """ + str(int(i)).zfill(4) + """ (total_num: 68)</h2>
    <p style="margin-left:40%"><a class="button" href="./vis_""" + str(int(i)-1).zfill(4) + """.html" target="top">Prev</a><a style="margin-left:5%"
        class="button" href="./vis_""" + str(int(i)+1).zfill(4) + """.html" target="top">Next</a></p>

        <div class="container" id="vis"></div>

    <script type="text/javascript">
        var yourVlSpec = '../../jsonfiles/d0_v2/vl_""" + i + """.vl.json'
        vegaEmbed('#vis', yourVlSpec);
    </script>
    </body>

    </html>
    """

from glob import glob
import os

num = glob('./files/v2v3vl/jsonfiles/d0_v2/*.vl.json')

os.makedirs('./files/v2v3vl/visfiles/v2_v0', exist_ok=True)

for i in range(len(num)):
    print(f"{i}... progress")
    i = str(i).zfill(4)
    file = change_var(i)
    with open(f"./files/v2v3vl/visfiles/v2_v0/vis_{i}.html", "w") as f:
        f.write(file)
print("end")