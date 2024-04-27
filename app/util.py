import os
import random
import glob
import numpy as np
import traceback

from PIL import Image
from werkzeug.utils import secure_filename

# Text to speech conversion
from gtts import gTTS

# App modules
from app import app


class Util():

    @staticmethod
    def allowed_file(filename):
        try:
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
        except:
            return False

    @staticmethod
    def validate_uploaded_file(dict_files):
        flash_msg = ''
        try:
            # file part not present in post
            if 'file' not in dict_files:
                flash_msg = 'no file part found'
            else:
                file = dict_files['file']
                # Empty file without filename
                if file.filename == '':
                    flash_msg = 'please upload an image'
                else:
                    # File exists and is allowed
                    if not Util.allowed_file(file.filename):
                        flash_msg = 'only jpeg, jpg and png files are allowed'
        except Exception as e:
            print('An exception occured : ' + traceback.format_exc())
        return flash_msg

    @staticmethod
    def get_imagepath_json(sample_num):
        img_json = None
        img_path = ''
        try:
            if sample_num == 1:
                img_path = 'app/static/assets/img/sample/efb-1.jpg'
            elif sample_num == 2:
                img_path = 'app/static/assets/img/sample/efb-2.jpg'
            elif sample_num == 3:
                img_path = 'app/static/assets/img/sample/efb-3.jpg'
            image = np.asarray(Image.open(img_path)).astype(np.float32)
            img_json = {'image': image.tolist()}
        except Exception as e:
            print('An exception occured : ' + traceback.format_exc())
        return img_json

    @staticmethod
    def get_image_json(dict_files):
        img_json = None
        try:
            img = dict_files['file']
            image = np.asarray(Image.open(img)).astype(np.float32)
            img_json = {'image': image.tolist()}
        except Exception as e:
            print('An exception occured : ' + traceback.format_exc())
        return img_json

    @staticmethod
    def get_latest_audio():
        audio_filename = ''
        try:
            if os.listdir(app.config['AUDIO_FOLDER']):
                audio_filename = max(
                    glob.glob(app.config['AUDIO_FOLDER']+'/*'), key=os.path.getctime).replace('app', '')
        except:
            audio_filename = ''
        return audio_filename

    @staticmethod
    def delete_older_files():
        try:
            for f in os.listdir(app.config['AUDIO_FOLDER']):
                if f.endswith('.mp3'):
                    os.remove(os.path.join(app.config['AUDIO_FOLDER'], f))
        except:
            pass

    @staticmethod
    def text_to_speech(cap_text):
        is_converted = False
        Util.delete_older_files()
        try:
            # Generate new audio file
            aud_filename = str(random.random())+'.mp3'
            tts = gTTS(text=cap_text, lang="en", slow=False, tld="com")
            tts.save(os.path.join(app.config['AUDIO_FOLDER'], aud_filename))
            is_converted = True
        except:
            pass
        return is_converted
