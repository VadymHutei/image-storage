import os
import hashlib
from werkzeug.utils import secure_filename
# try:
#     import customconfig as config
# except:
#     import config
import config

class Storage():

    def __init__(self):
        self._errors = {
            'ERR01': {'status': 'error', 'error': 'file extension is not allowed'},
            'ERR02': {'status': 'error', 'error': 'empty filename'}
        }

    def _savingError(self, code):
        return self._errors[code] if code in self._errors else {'status': 'error', 'error': f'unknown error - {code}'}

    def _isAllowedExtension(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

    def _getImageSegment(self, filename):
        m = hashlib.md5()
        m.update(filename.encode('utf-8'))
        return m.hexdigest()[:3]

    def _createPath(self, filename):
        secure_name = secure_filename(filename)
        segment = self._getImageSegment(secure_name)
        path = os.path.join(config.STORAGE_PATH, segment)
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(path, secure_name)

    def save(self, image):
        if not self._isAllowedExtension(image.filename): return self._savingError('ERR01')
        if image.filename.rsplit('.', 1)[0] == '': return self._savingError('ERR02')
        path = self._createPath(image.filename)
        image.save(path)
        return {
            'status': 'success',
            'url': 'test'
        }