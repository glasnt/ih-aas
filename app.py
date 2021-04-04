import os
import shutil
import string
import requests
import random

from flask import Flask, request, Response, send_file, render_template

from ih.chart import chart as ih_chart
from ih.cli import main as cli
import click

UPLOAD_FOLDER = "tmp/upload"
OUTPUT_FOLDER = "tmp/output"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def proforma():
    form = []

    ignore = ["fileformat", "version"]

    for param in cli.params:
        form.append("<div class='row'><div class='column'>")

        name = param.name
        if name in ignore:
            continue

        # File input
        if type(param.type) == click.types.File:
            form.append(f"<label>{name}</label>")
            form.append(f"<input type='file' name='{name}' id='{name}'>")
        # Choice -> radio button
        elif type(param.type) == click.types.Choice:
            form.append(f"<label>{name}</label>")
            for option in param.type.choices:
                form.append(
                    f"<input type='radio' name='{name}' id='{option}' value='{option}'><label class='label-inline' or='{option}'>{option}</label>"
                )
        # integer
        elif type(param.type) == click.types.IntParamType:
            form.append(
                f"<label for='{name}'>{name}</label><input type='number' name='{name}' id='{name}' value='{param.default}'><div class='help'>{param.help}</div>"
            )
        # boolean checkbox
        elif type(param.type) == click.types.BoolParamType:
            form.append(
                f"""
            <input type='checkbox' id='{name}' value='True' name='{name}'/>
            <label class='label-inline' for='{name}'>{name}</label>
            <div class='help'>{param.help}</div>
            """
            )
        else:
            print("Unknown type:", param, type(param.type))
        form.append("</div></div>")

    return "\n".join(form)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html", content=proforma())

    input_dir = UPLOAD_FOLDER
    os.makedirs(input_dir, exist_ok=True)

    upload = request.files["image"]
    if not allowed_file(upload.filename):
        return "File upload type not allowed."

    ext = upload.filename.split(".")[-1]
    rand_fn = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    input_file = os.path.join(input_dir, f"{rand_fn}.{ext}")

    if upload.filename != "":
        upload.save(input_file)

    inputs = dict(request.form.items())

    # Cast types
    for param in cli.params:
        if param.name in inputs:
            if type(param.type) == click.types.IntParamType:
                inputs[param.name] = int(inputs[param.name])
        if param.name in inputs:
            if type(param.type) == click.types.BoolParamType:
                inputs[param.name] = bool(inputs[param.name])

    inputs["image"] = input_file
    inputs["outputfolder"] = OUTPUT_FOLDER
    # hack - some elements have different names
    if "palette" in inputs.keys():
        inputs["palette_name"] = inputs["palette"]
        del inputs["palette"]

    # Return terminal if curled, otherwise HTML
    if "text/html" in request.headers.get("Accept", ""):
        fileformat = "html"
    else:
        fileformat = "term"
    inputs["fileformat"] = fileformat

    chart_file = ih_chart(**inputs)

    if fileformat == "html":
        return send_file(chart_file.replace("Result: ", ""))
    else:
        return Response(chart_file, mimetype="text/plain; charset=utf-8")


@app.after_request
def cleanup(response):
    if os.path.isdir(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
    if os.path.isdir(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
