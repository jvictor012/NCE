from flask import Flask, render_template, request
from cloudinary_service import cloudinary
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    UserMixin,
    current_user,
)
import bcrypt
from supabase_service import supabase 

app = Flask(__name__)
app.secret_key = 'chave_muito_secreta'
config = cloudinary.config(secure=True)

@app.route('/noticias')
def noticias():
    return render_template('home_user.html')


@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        image1 = request.files['imagem1']
        image2 = request.files['imagem2']
        image3 = request.files['imagem3']


        res1 = cloudinary.uploader.upload(image1)
        imglink1 = res1["secure_url"]
        
        if image2:
            res2 = cloudinary.uploader.upload(image2)
            imglink2 = res2["secure_url"]

        if image3:
            res3 = cloudinary.uploader.upload(image3)
            imglink3 = res3["secure_url"]


        noticia = {'titulo':request.form['titulo'],
                   'categoria':request.form['categoria'],
                   'conteudo':request.form['conteudo'],
                   'link1':request.form.get('link1'),
                   'link2':request.form.get('link2'),
                   'link3':request.form.get('link3'),
                   'link4':request.form.get('link4'),
                   'link5':request.form.get('link5'),
                   'imglink1': imglink1,
                   'imglink2': None,
                   'imglink3': None}
        noticia = supabase.table("noticias").insert(noticia).execute()
        print("Feito")
        

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
