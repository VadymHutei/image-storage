import sys

mode = 'prod' if len(sys.argv) > 1 and sys.argv[1] == 'prod' else 'dev'

mode_app_params = {
    'dev': {
        'debug': True,
        'host': '0.0.0.0',
        'port': 80
    }
    'prod': {
        'debug': True,
        'host': '0.0.0.0',
        'port': 80
    }
}
app_params = mode_app_params[mode]