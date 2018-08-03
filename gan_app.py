from flask import Flask, render_template, redirect, request
import base64
from io import BytesIO
import glob
import os
from PIL import Image
import image_generator
import pggan_generator
import random

app = Flask(__name__)
resultpath = './results/*'
n_hidden = 100
file_list = []

@app.route('/', methods=['GET', 'POST'])
def render():

    files = glob.glob(resultpath)
    load_file = random.choice(files)
    file_list.insert(0, load_file)

    img_read = Image.open(load_file)
    buf = BytesIO()
    img_read.save(buf, format="png")
    im_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")
    im_b64data = "data:image/png;base64,{}".format(im_b64str)

    name = os.path.basename(files[0])

    return render_template("index.html",
        generated_image_b64=im_b64data,
        generated_image_name = name,
        list = file_list
        )

@app.route('/load_old',methods=['GET', 'POST'])
def load_old():
    return redirect('/', code=303)

@app.route('/load', methods=['GET','POST'])
def load():
    return redirect('/', code=303)

@app.route('/generate', methods=['GET','POST'])
def generate():
    file_list = []
    regenerate()
    return redirect('/', code=303)

@app.route('/back', methods=['GET', 'POST'])
def back():
    if len(file_list) > 1:
        img_read = Image.open(file_list[1])
        file_list.insert(0, file_list[1])
        name = os.path.basename(file_list[1])
    else:
        return redirect('/', code=303)

    buf = BytesIO()
    img_read.save(buf, format="png")
    im_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")
    im_b64data = "data:image/png;base64,{}".format(im_b64str)


    return render_template("index.html",
        generated_image_b64=im_b64data,
        generated_image_name = name,
        list = file_list
        )

def regenerate():
    files = glob.glob(resultpath)
    if len(files) > 0:
        for file in files:
            os.remove(file)

    if(random.randint(0,1) == 0):
        imgen = image_generator.ImageGenerator(n_hidden)
        imgen()
    else:
        pgan = pggan_generator.PgganGenerator(6)
        pgan(100)


    return

if __name__ == "__main__":
    app.run(debug=False, port=22222)
