import os


def global_settings(request):
    return {
        'APP_ID': os.environ.get('APP_ID')
    }
