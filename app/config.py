import os
import sys
import pathlib

mode = 'prod' if len(sys.argv) > 1 and sys.argv[1] == 'prod' else 'dev'

mode_app_params = {
    'dev': {
        'debug': True,
        'host': '0.0.0.0',
        'port': 80
    },
    'prod': {
        'debug': False,
        'host': '0.0.0.0',
        'port': 5000
    }
}
APP_PARAMS = mode_app_params[mode]
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')
STORAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'storage')