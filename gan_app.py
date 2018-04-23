from flask import Flask, render_template, redirect, request
import base64
from io import BytesIO
import glob
import os
from PIL import Image
import image_generator
import random
import pdb

app = Flask(__name__)
resultpath = './results/*'
n_hidden = 100


@app.route('/', methods=['GET', 'POST'])
def render():
            
    files = glob.glob(resultpath)

    img_read = Image.open(random.choice(files))
    buf = BytesIO()
    img_read.save(buf, format="png")
    im_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")
    im_b64data = "data:image/png;base64,{}".format(im_b64str)

    name = os.path.basename(files[0])

    return render_template("index.html",
        generated_image_b64=im_b64data,
        generated_image_name = name
    )

@app.route('/load', methods=['GET','POST'])
def load():
    return redirect('/', code=303)

@app.route('/generate', methods=['GET','POST'])
def generate():
    regenerate()
    return redirect('/', code=303)

def regenerate():
    files = glob.glob(resultpath)
    if len(files) > 0:
        for file in files:
            os.remove(file)

    imgen = image_generator.ImageGenerator(n_hidden)
    imgen()
    return

if __name__ == "__main__":
    app.run(debug=False, port=22222)
