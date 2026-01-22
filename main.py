from flask import Flask, render_template, request
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    UserMixin,
    current_user,
)
import bcrypt

app = Flask(__name__)
app.secret_key = 'chave_muito_secreta'
config = cloudinary.config(secure=True)

@app.route('/noticias')
def noticias():
    return render_template('home_user.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        titulo = request.form['titulo']
        categoria = request.form['categoria']
        conteudo = request.form['conteudo']
        link1 = request.form.get('link1')
        link2 = request.form.get('link2')
        link3 = request.form.get('link3')
        link4 = request.form.get('link4')
        link5 = request.form.get('link5')

        imagem1 = request.files['imagem1']
        link_imagem1 = None
        imagem2 = request.files.get('imagem2')
        link_imagem2 = None
        imagem3 = request.files.get('imagem3')
        link_imagem3 = None
        binario = imagem1.read()


        if titulo and categoria and conteudo and imagem1:
            print(imagem1)
            img = cloudinary.uploader.upload(imagem1)
            img_link = img["secure_url"]
            print(img_link)
        

    return render_template('index.html')


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    return render_template('perfil.html')


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('cenome')
        email = request.form.get('cemail')
        matricula = request.form.get('cmatricula')
        senha = request.form.get('csenha')

        # Apenas hash local (sem salvar)
        senha_hash = bcrypt.hashpw(
            senha.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        mensagem = "Cadastro recebido (processamento via Supabase)"
        return render_template('cadastrar.html', mensagem=mensagem)

    return render_template('cadastrar.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
