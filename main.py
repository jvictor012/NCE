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

@app.route('/')
def noticias():
    noticias_resp = supabase.table("noticias").select("titulo, created_at, conteudo, link1, link2, link3, link4, link5, categoria").execute()
    imagens_resp = supabase.table("images_links").select("image_url").execute()

    noticias_data = noticias_resp.data
    imagens_data = imagens_resp.data 


    noticias = []
    for i, noticia in enumerate(noticias_data):
        noticias.append(
            {
                "imagem" : imagens_data[i]["image_url"] if i < len(imagens_data) else None, 
                "titulo" : noticia["titulo"],
                "created_at" : noticia["created_at"],
                "conteudo" : noticia["conteudo"],
                "link1" : noticia["link1"],
                "link1" : noticia["link1"],
                "link1" : noticia["link1"],
                "link1" : noticia["link1"],
                "link1" : noticia["link1"],
                "categoria" : noticia["categoria"]
            }
        )
    
    return render_template('home_user.html', noticias=noticias)
    

@app.route('/eventos')
def eventos():
    #fazer a consulta e printar os eventos
    selecao = supabase.table("noticias").select('created_at, titulo, conteudo, categoria').in_('categoria', ['Eventos Esportivos', 'Eventos Educacionais']).order('created_at', desc=True).execute()
    imagens_resp = supabase.table("images_links").select("image_url").execute()

    selecao_data = selecao.data
    imagens_data = imagens_resp.data 

    eventos = []
    for i, evento in enumerate(selecao_data):
        eventos.append({
            "imagem": imagens_data[i]["image_url"] if i < len(imagens_data) else None,
            "created_at": evento["created_at"],
            "titulo": evento["titulo"],
            "conteudo": evento["conteudo"],
            "categoria": evento["categoria"]
        })
    return render_template("eventos.html", evento = eventos)

@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        noticia = {'titulo':request.form['titulo'],
                   'categoria':request.form['categoria'],
                   'conteudo':request.form['conteudo'],
                   'link1':request.form.get('link1'),
                   'link2':request.form.get('link2'),
                   'link3':request.form.get('link3'),
                   'link4':request.form.get('link4'),
                   'link5':request.form.get('link5')
                   }
        noticia = supabase.table("noticias").insert(noticia).execute()
        id_noticia = noticia.data[0]['id']


        imagens = ["imagem1","imagem2","imagem3"]

        for campo in imagens:
            arquivo = request.files.get(campo)
            if arquivo and arquivo.filename != None:
                upload = cloudinary.uploader.upload(arquivo)
                link_up = upload['secure_url']
                supabase.table("images_links").insert({'noticia_id':id_noticia, 'image_url': link_up}).execute()

        
        
    

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
