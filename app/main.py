import os
from flask import Flask, render_template, url_for, request, abort, send_from_directory
from PIL import Image
from helper import allowed_file, prepare_name, getPathSegment, isSegment, isResizedImage, getRequestedParameters

UPLOAD_FOLDER = './images'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    # Если есть файл, отдаем
    if os.path.exists(image_path):
        return send_from_directory(directory, image_name)
    else:
        # Если файла нет, проверяем, запрашивается ли ресайз
        if isResizedImage(image_name):
            params = getRequestedParameters(image_name)
            if not params: abort(500)
            image_path = os.path.join(directory, params['name'])
            if not os.path.exists(image_path):abort(404)
            img = Image.open(image_path)
            size = []
            size.append(round(params['height'] * img.size[0] / img.size[1]) if params['width'] is None else params['width'])
            size.append(round(params['width'] * img.size[1] / img.size[0]) if params['height'] is None else params['height'])
            size = tuple(size)
            if size == img.size: return send_from_directory(directory, params['name'])
            # img.resize(size)
            return 'resize'
        else:
            abort(404)

# Загрузка картинки на сервер
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        if 'image' not in request.files:
            return render_template('upload.html', message='err1')
        image = request.files['image']
        if image.filename == '':
            return render_template('upload.html', message='err2')
        if not image or not allowed_file(image.filename):
            return render_template('upload.html', message='err3')
        # Подготовка безопасного имени для картинки
        filename = prepare_name(image.filename)
        # Определение сегмента для размещения картинки
        path_segment = getPathSegment(filename)
        # Построение полного пути
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], path_segment)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        image_path = os.path.join(full_path, filename)
        # Сохранение
        image.save(image_path)
        return render_template('upload.html', message=image_path)

@app.route('/test', methods=['GET'])
def test():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)