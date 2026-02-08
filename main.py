from flask import Flask, render_template, request, redirect, url_for
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

class User(UserMixin):
    def __init__(self, id, email, role=None):
        self.id = id
        self.email = email
        self.role = role


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    result = supabase.table("users").select("*").eq("id", user_id).execute()

    if not result.data:
        return None

    u = result.data[0]
    return User(u["id"], u["email"], u.get("role"))

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
                "link2" : noticia["link2"],
                "link3" : noticia["link3"],
                "link4" : noticia["link4"],
                "link5" : noticia["link5"],
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
@login_required
def home():
    print(current_user.id)

    if current_user.id == 1:
        print(current_user.id)
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


            imagens = ["imagem1"]

            for campo in imagens:
                arquivo = request.files.get(campo)
                if arquivo and arquivo.filename != None:
                    upload = cloudinary.uploader.upload(arquivo)
                    link_up = upload['secure_url']
                    supabase.table("images_links").insert({'noticia_id':id_noticia, 'image_url': link_up}).execute()
        return render_template("index.html")
        
    else:
        print(current_user.id)
        return render_template("aviso.html")

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    id_user = current_user.id
    if id_user:
        select = supabase.table("users").select("id, email").eq("id", id_user).execute()
        email = select.data[0]['email']
        print(select)
        return render_template('perfil.html', email=email)
    else:
        return redirect(url_for('login'))


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        email = request.form.get('cemail')
        senha = request.form.get('csenha')
        # Apenas hash local (sem salvar)
        senha_hash = bcrypt.hashpw(
            senha.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        exists = supabase.table("users").select("*").eq("email", email).execute()
        if exists.data:
            print("erro")
        else:
            supabase.table("users").insert({"email": email, "senha": senha_hash}).execute()
            return render_template("login.html")


    return render_template('cadastrar.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":

        email = request.form.get("lemail")
        senha = request.form.get("lsenha").encode("utf-8")


        result = supabase.table("users").select("*").eq("email", email).execute()
        if result.data:
            senha_hash = result.data[0]["senha"].encode("utf-8")
            if bcrypt.checkpw(senha, senha_hash):
                user_db = result.data[0]
                user = User(user_db["id"], user_db["email"])
                login_user(user)
                return redirect(url_for("noticias"))
            else:
                print("erro")

    
    return render_template('login.html')

@app.route('/noticias', methods=['GET', 'POST'])
def filtrar():
    filtro = None

    query = (
        supabase
        .table("noticias")
        .select(
            "id, titulo, created_at, conteudo, link1, link2, link3, link4, link5, categoria"
        )
        .order('created_at', desc=True)
    )

    if request.method == 'POST':
        filtro = request.form.get('filtro')
        if filtro:
            query = query.eq('categoria', filtro)

    selecao = query.execute()

    imagens_resp = (
        supabase
        .table("images_links")
        .select("image_url, noticia_id")
        .execute()
    )

    # Mapa: noticia_id -> image_url
    imagens_map = {
        img["noticia_id"]: img["image_url"]
        for img in imagens_resp.data
    }

    noticias = []
    for noticia in selecao.data:
        noticias.append({
            "imagem": imagens_map.get(noticia["id"]),
            "created_at": noticia["created_at"],
            "titulo": noticia["titulo"],
            "conteudo": noticia["conteudo"],
            "categoria": noticia["categoria"],
            "link1": noticia["link1"],
            "link2": noticia["link2"],
            "link3": noticia["link3"],
            "link4": noticia["link4"],
            "link5": noticia["link5"]
        })

    return render_template(
        'noticias.html',
        noticias=noticias,
        filtragem=filtro
    )


@app.route('/contatos')
def contatos():
    return render_template('contatos.html')



if __name__ == '__main__':
    app.run(debug=True)
