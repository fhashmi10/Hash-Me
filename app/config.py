from decouple import config


class Config():
    CSRF_ENABLED = True

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='H@shM3K3y_10')

    # Set up file upload config
    AUDIO_FOLDER = config('AUDIO_FOLDER', default='app/static/assets/audio')
    ALLOWED_EXTENSIONS = config('ALLOWED_EXTENSIONS', default={'jpeg', 'jpg', 'png'})

    # End point to call model
    ENDPOINT_URL = 'http://fh-itos.herokuapp.com/predict'
    # Post async indicator
    POST_ASYNC = True