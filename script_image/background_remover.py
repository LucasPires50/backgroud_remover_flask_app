import os
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename
from flask import request,render_template, Blueprint

# Obtém o caminho do diretório atual onde este script está localizado.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# UPLOAD_FOLDER = 'script_image/static/uploads'
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
# Formatos de imagens permitidos
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','webp'])

# Verificar se existe a pasta "static", se não existir cria
if 'static' not in os.listdir(BASE_DIR):
    os.mkdir(f'{BASE_DIR}/static')

# Verificar se dentro da pasta "static", existe a pasta "uploads", se não existir cria
if 'uploads' not in os.listdir(f'{BASE_DIR}/static'):
    os.mkdir(f'{BASE_DIR}/static/uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def remove_background(input_path,output_path):
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)

app_backg_rem = Blueprint('script_image', __name__)

@app_backg_rem.route('/')
def home():
    return render_template('home.html')

@app_backg_rem.route('/remback',methods=['POST'])
def remback():
    file = request.files['file']
    if not file:
        return render_template('status/erro_400.html'), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
    
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        rembg_img_name = f"{filename.split('.')[0]}_rembg.png"
        
        remove_background(os.path.join(UPLOAD_FOLDER, filename),os.path.join(UPLOAD_FOLDER, rembg_img_name))
        return render_template('home.html',org_img_name=filename,rembg_img_name=rembg_img_name)

def delete_files_in_folder(pasta):
    try:
        for arquivo in os.listdir(pasta):
            caminho_arquivo = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)
        print(f"Todos os arquivos em '{pasta}' foram excluídos com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao excluir os arquivos em '{pasta}': {e}")

# Chame a função para deletar arquivos na pasta "static/uploads"
pasta_uploads = UPLOAD_FOLDER
delete_files_in_folder(pasta_uploads)
