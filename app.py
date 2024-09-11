from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import os
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {
    'png', 'jpg', 'jpeg', 'gif', 'webp', 'tiff', 'bmp', 'ico', 'svg', 'heic', 'heif', 'jfif', 'jp2', 'j2k', 'jpf', 
    'jpx', 'jpm', 'pbm', 'pgm', 'ppm', 'pnm', 'xbm', 'xpm', 'dds', 'hdr', 'exr', 'tga', 'avif'
}


# Função para verificar a extensão do arquivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para upload e conversão de imagem
@app.route('/convert', methods=['POST'])
def convert_image():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Formato de conversão
        output_format = request.form.get('format').lower()

        # Abrindo a imagem usando PIL e convertendo
        with Image.open(filepath) as img:
            img = img.convert("RGB")  # Converte para RGB para compatibilidade
            img_io = io.BytesIO()
            img.save(img_io, format=output_format.upper())
            img_io.seek(0)

        os.remove(filepath)  # Remove a imagem original após conversão

        return send_file(img_io, mimetype=f'image/{output_format}', as_attachment=True, download_name=f'converted_image.{output_format}')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
