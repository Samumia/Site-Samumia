from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Configuração do Cloudinary
cloudinary.config(
    cloud_name="dz41grdow",
    api_key="127866414955154",
    api_secret="BAIqUg3OYW0yPFtN5Iefu8H8YUM"
)

# Lista temporária para mostrar arquivos (simula um banco)
arquivos_cloud = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', arquivos=arquivos_cloud)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    if f:
        filename = secure_filename(f.filename)
        result = cloudinary.uploader.upload(f, public_id=filename)
        arquivos_cloud.append({
            'nome': filename,
            'url': result['secure_url']
        })
    return redirect(url_for('index'))

@app.route('/rename', methods=['POST'])
def rename():
    old_name = request.form['old_name']
    new_name = request.form['new_name'].strip().replace('/', '').replace('\\', '')
    ext = os.path.splitext(old_name)[1]
    new_name_full = new_name + ext

    for arquivo in arquivos_cloud:
        if arquivo['nome'] == old_name:
            # Renomeia no Cloudinary
            cloudinary.uploader.rename(old_name, new_name_full, overwrite=True)
            arquivo['nome'] = new_name_full
            arquivo['url'] = arquivo['url'].replace(old_name, new_name_full)
            return jsonify(success=True)
    return jsonify(success=False), 400

@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']
    public_id = os.path.splitext(name)[0]

    try:
        cloudinary.uploader.destroy(public_id)
        global arquivos_cloud
        arquivos_cloud = [arq for arq in arquivos_cloud if arq['nome'] != name]
        return jsonify(success=True)
    except:
        return jsonify(success=False), 400

if __name__ == '__main__':
    app.run(debug=True)
