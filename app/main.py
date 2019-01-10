import os
from flask import Flask, render_template, url_for, request, abort, send_from_directory
from PIL import Image
from helper import allowed_file, prepare_name, getPathSegment, isSegment, isResizedImage, getRequestedParameters
import config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['MAX_IMAGE_SIZE'] = config.MAX_IMAGE_SIZE
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

@app.route('/')
def main():
    return 'Ukubuka Image Storage'

@app.route('/images/<path:path>', methods=['GET'])
def getImage(path):
    l_path = path.split('/')
    if len(l_path) != 2: abort(404)
    if not isSegment(l_path[0]): abort(404)
    segment = l_path[0]
    image_name = l_path[1]
    if not allowed_file(image_name): abort(400)
    directory = os.path.join(app.config['UPLOAD_FOLDER'], segment)
    image_path = os.path.join(directory, image_name)
    if os.path.exists(image_path): return send_from_directory(directory, image_name)
    if not isResizedImage(image_name): abort(404)
    params = getRequestedParameters(image_name)
    if not params: abort(500)
    stock_image_path = os.path.join(directory, params['name'])
    if not os.path.exists(stock_image_path):abort(404)
    img = Image.open(stock_image_path)
    size = (
        round(params['height'] * img.size[0] / img.size[1]) if params['width'] is None else params['width'],
        round(params['width'] * img.size[1] / img.size[0]) if params['height'] is None else params['height']
    )
    if size[0] > app.config['MAX_IMAGE_SIZE'][0] or size[1] > app.config['MAX_IMAGE_SIZE'][1]: abort(400)
    if size == img.size: return send_from_directory(directory, params['name'])
    img.resize(size, Image.BICUBIC).save(image_path)
    if os.path.exists(image_path): return send_from_directory(directory, image_name)
    abort(500)

@app.route('/upload', methods=['POST'])
def upload():
    if request.form['secret_key'] != config.SECRET_KEY: abort(403)
    if 'image' not in request.files: abort(400)
    image = request.files['image']
    if image.filename == '': return abort(400)
    if not image or not allowed_file(image.filename): return abort(400)
    filename = prepare_name(image.filename)
    path_segment = getPathSegment(filename)
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], path_segment)
    if not os.path.exists(full_path): os.makedirs(full_path)
    image_path = os.path.join(full_path, filename)
    image.save(image_path)
    return image_path[1:]

if __name__ == '__main__':
    app.run(**config.APP_PARAMS)