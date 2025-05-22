from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/arquivos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    arquivos = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', arquivos=arquivos)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    if f:
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(url_for('index'))

@app.route('/download/<nome_arquivo>')
def download(nome_arquivo):
    return send_from_directory(UPLOAD_FOLDER, nome_arquivo, as_attachment=True)

@app.route('/rename', methods=['POST'])
def rename():
    old_name = request.form['old_name']
    new_name = request.form['new_name'].strip().replace('/', '').replace('\\', '')
    old_path = os.path.join(UPLOAD_FOLDER, old_name)
    ext = os.path.splitext(old_name)[1]
    new_path = os.path.join(UPLOAD_FOLDER, new_name + ext)

    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return jsonify(success=True)
    return jsonify(success=False), 400

@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']
    path = os.path.join(UPLOAD_FOLDER, name)
    if os.path.exists(path):
        os.remove(path)
        return jsonify(success=True)
    return jsonify(success=False), 400

if __name__ == '__main__':
    app.run(debug=True)
