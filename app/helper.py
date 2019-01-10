import re
import hashlib
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'shoto')
TRANSLITERATION_DICTIONARY = {
    'а':'a','б':'b','в':'v','г':'g','ґ':'g','д':'d',
    'е':'e','є':'e','э':'e','ë':'yo','ж':'zh','з':'z',
    'и':'i','ы':'y','і':'i','ї':'i','й':'i','к':'k',
    'л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
    'с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'ts',
    'ч':'ch','ш':'sh','щ':'shch','ь':'','ю':'iu','я':'ia'
}

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

def isSegment(string):
    return re.fullmatch(r'[0-9a-f]{3}', string)

def isResizedImage(filename):
    return re.fullmatch(r'.+-(?:w|h)[0-9]+\.(?:{ext})'.format(ext='|'.join(ALLOWED_EXTENSIONS)), filename)

def getRequestedParameters(filename):
    result = {
        'width': None,
        'height': None
    }
    raw_params_string = re.findall(r'(?:-(?:w|h)[0-9]+)+', filename)
    if not len(raw_params_string): return False
    raw_params = re.findall(r'-(?:w|h)[0-9]+', raw_params_string[-1])
    result['name'] = filename.replace(raw_params_string[-1], '')
    raw_params.reverse()
    for param in raw_params:
        if param[1] == 'w' and result['width'] is None:
            result['width'] = int(param[2:])
        if param[1] == 'h' and result['height'] is None:
            result['height'] = int(param[2:])
    return result