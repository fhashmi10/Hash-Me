import traceback
import requests
import asyncio

# Flask modules
from flask import flash, request, redirect, render_template
from jinja2 import TemplateNotFound

# App modules
from app import app
from app.util import Util
from app.post import Post

@app.route('/image-captioning.html', methods=['POST'])
def eye_for_blind_post():
    flash_msg = ''
    img_json = None
    try:
        if request.form.get('sample1'):
            img_json = Util.get_imagepath_json(1)
        elif request.form.get('sample2'):
            img_json = Util.get_imagepath_json(2)
        elif request.form.get('sample3'):
            img_json = Util.get_imagepath_json(3)
        else:
            flash_msg = Util.validate_uploaded_file(request.files)
            if flash_msg=='':
                img_json = Util.get_image_json(request.files)

        if img_json is not None:
            if app.config['POST_ASYNC']==True:
                caption = asyncio.run(Post.post_async(app.config['ENDPOINT_URL'], img_json))
            else:
                caption = Post.post_sync(app.config['ENDPOINT_URL'], img_json)
            flash_msg = caption

        if flash_msg != '':
            if flash_msg[0]=='<':
                flash_msg = 'Caption generation service is down. Please contact developer.'
            is_converted = Util.text_to_speech(flash_msg)
            if not is_converted:
                flash_msg = 'error converting to speech'
        else:
            flash_msg = 'Not able to generate caption. Please contact developer.'
    except requests.Timeout:
        flash_msg = 'Timeout occured at caption generation service. Please contact developer.'
    except Exception as e:
        print('An exception occured : ' + traceback.format_exc())
        flash_msg = 'an error occured. please contact developer.'

    flash(flash_msg)
    return redirect(request.url)


# App main route + generic routing
@app.route('/', defaults={'path': 'projects-dashboard.html'})
@app.route('/<path>')
def index(path):
    try:
        if not path.endswith('.html'):
            path += '.html'
        if path == 'projects-dashboard.html':
            Util.delete_older_files()
        return render_template(path)
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500


# Context processor to dynamically update html content
@app.context_processor
def inject_user():
    return dict(audio_filename=Util.get_latest_audio())
