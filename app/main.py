import os
import hashlib
import re
from flask import Flask, render_template, url_for, request, abort, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')
TRANSLITERATION_DICTIONARY = {
    'а':'a','б':'b','в':'v','г':'g','ґ':'g','д':'d',
    'е':'e','є':'e','э':'e','ë':'yo','ж':'zh','з':'z',
    'и':'i','ы':'y','і':'i','ї':'i','й':'i','к':'k',
    'л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
    'с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'ts',
    'ч':'ch','ш':'sh','щ':'shch','ь':'','ю':'iu','я':'ia'
}
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepare_name(name):
    temp_name = []
    trans_dict = TRANSLITERATION_DICTIONARY.keys()
    for char in name.lower():
        if char in trans_dict:
            temp_name.append(TRANSLITERATION_DICTIONARY[char])
        else:
            temp_name.append(char)
    return secure_filename(''.join(temp_name))

def getPathSegment(filename):
    m = hashlib.md5()
    m.update(filename.encode('utf-8'))
    return m.hexdigest()[:3]

@app.route('/')
def main():
    return 'Image Storage'

@app.route('/images/<path:path>', methods=['GET'])
def getImage(path):
    path = path.split('/')
    if len(path) != 2:
        abort(404)
    if not re.fullmatch('[0-9a-f]{3}', path[0]):
        abort(404)
    directory = os.path.join(app.config['UPLOAD_FOLDER'], path[0])
    return send_from_directory(directory, path[1])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        if 'image' not in request.files:
            return redirect(url_for('test'))
        image = request.files['image']
        if image.filename == '':
            return redirect(url_for('test'))
        if image and allowed_file(image.filename):
            filename = prepare_name(image.filename)
            path_segment = getPathSegment(filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], path_segment)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            image_path = os.path.join(full_path, filename)
            image.save(image_path)
            return render_template('upload.html', image_path=image_path)

@app.route('/test', methods=['GET'])
def test():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)