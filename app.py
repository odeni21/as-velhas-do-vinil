
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os

app = Flask(__name__)
app.secret_key = 'asvelhasdovinil2024'
UPLOAD_FOLDER = 'uploads'
ADMIN_USER = 'admin'
ADMIN_PASS = '141821Manu@'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return '''
        <h1>As Velhas do Vinil</h1>
        <a href="/admin">Painel Admin</a><br><br>
        <h2>Músicas Disponíveis:</h2>
        ''' + ''.join(f'<p>{file} - <a href="/download/{file}">Download</a></p>' for file in files)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('upload'))
    return '''
        <h2>Login Admin</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Usuário"><br>
            <input type="password" name="password" placeholder="Senha"><br>
            <button type="submit">Entrar</button>
        </form>
    '''

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
    return '''
        <h2>Enviar Música</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file"><br>
            <button type="submit">Enviar</button>
        </form>
        <a href="/">Voltar ao Site</a>
    '''

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
