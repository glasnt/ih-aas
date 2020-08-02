import os
import shutil
import requests

from flask import Flask, request, Response

from ih.chart import chart as ih_chart

UPLOAD_FOLDER = "tmp"
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def proforma(): 
    
    html = """
    <div class="container">
    <div class="row"><div class="twelve columns">
        <h2><code>ih</code>, as a service™️</h2>
        <p>Specify a <code>?url</code> of an image, with optional <code>scale,
        colors, palette</code> parameters, and optional <code>render,
        guidelines</code> flags. <a
        href="?url=https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/180/parrot_1f99c.png&scale=3&colors=16">Example</a><p>
        <p>Coming soon: file uploads</p>
    </div></div>
    </div>
    """
    return html


@app.route("/", methods=["GET", "POST"])
def api():
    
    file_name = 'document' 
    folder_name = 'convert'
    input_dir = os.path.join(UPLOAD_FOLDER, folder_name)
    input_file =  os.path.join(input_dir, file_name)
    output_dir = input_dir
    output_file = os.path.join(output_dir, file_name + '.pdf')
    
    os.makedirs(input_dir, exist_ok=True)

    if request.method == 'GET':
        url = request.args.get('url', type = str)

        if not url:
            # Landing page
            return proforma()

        response = requests.get(url, stream=True)
        with open(input_file, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        del response

    # Passing through the flags to the CLI
    scale = request.args.get('scale', 10, type=int)
    colors = request.args.get('colors', 16, type=int)
    palette = request.args.get('palette', "wool")
    render = request.args.get('render', False, type=bool)
    guidelines = request.args.get('guidelines', False, type=bool)

    if "text/html" in request.headers.get("Accept", ""):
        fileformat = "html"
    else:
        fileformat = "term"
    
    chart = ih_chart(image_name=input_file, scale=scale, colors=colors, save=False, guidelines=guidelines, palette_name=palette, render=render, fileformat=fileformat) 

    if fileformat == "html": 
        return proforma() + chart
    else:
        return Response(chart, mimetype="text/plain; charset=utf-8")


@app.after_request
def cleanup(response):
    location = os.path.join(UPLOAD_FOLDER, 'convert')
    if os.path.isdir(location):
        shutil.rmtree(location)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
