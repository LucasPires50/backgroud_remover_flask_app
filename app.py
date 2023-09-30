import os
from flask import Flask
from script_image.background_remover import app_backg_rem, UPLOAD_FOLDER


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Instance
app = Flask(__name__)
app.register_blueprint(app_backg_rem)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Configuração do diretório statico
app.static_folder = f'{BASE_DIR}/script_image/static'


if __name__ == '__main__':
    app.run(debug=True)