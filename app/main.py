from flask import Flask, request, redirect, render_template
from storage import Storage
# try:
#     import customconfig as config
# except:
#     import config
import config

app = Flask(__name__)
storage = Storage()

@app.route('/acp', methods=['GET'])
def acp():
    return render_template('acp/main.html')

@app.route('/acp/upload', methods=['GET', 'POST'])
def upload():
    image_urls = []
    if request.method == 'POST':
        if 'images' not in request.files:
            return redirect(request.url)
        images = request.files.getlist('images')
        for image in images:
            result = storage.save(image)
            if result['status'] == 'success':
                image_urls.append(result['url'])
    return render_template('acp/upload.html', image_urls=image_urls)

if __name__ == '__main__':
    app.run(**config.APP_PARAMS)