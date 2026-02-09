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

# =======================
# USUÁRIO
# =======================
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

# =======================
# HOME (/)
# =======================
@app.route('/')
def noticias():
    noticias_resp = (
        supabase
        .table("noticias")
        .select(
            "id, titulo, created_at, conteudo, link1, link2, link3, link4, link5, categoria"
        )
        .order("created_at", desc=True)
        .execute()
    )

    imagens_resp = (
        supabase
        .table("images_links")
        .select("image_url, noticia_id")
        .execute()
    )

    imagens_map = {
        img["noticia_id"]: img["image_url"]
        for img in imagens_resp.data
    }

    noticias = []
    for noticia in noticias_resp.data:
        noticias.append({
            "imagem": imagens_map.get(noticia["id"]),
            "titulo": noticia["titulo"],
            "created_at": noticia["created_at"],
            "conteudo": noticia["conteudo"],
            "link1": noticia["link1"],
            "link2": noticia["link2"],
            "link3": noticia["link3"],
            "link4": noticia["link4"],
            "link5": noticia["link5"],
            "categoria": noticia["categoria"]
        })

    return render_template("home_user.html", noticias=noticias)

# =======================
# EVENTOS (/eventos)
# =======================
@app.route('/eventos')
def eventos():
    selecao = (
        supabase
        .table("noticias")
        .select("id, created_at, titulo, conteudo, categoria")
        .in_("categoria", ["Eventos Esportivos", "Eventos Educacionais"])
        .order("created_at", desc=True)
        .execute()
    )

    imagens_resp = (
        supabase
        .table("images_links")
        .select("image_url, noticia_id")
        .execute()
    )

    imagens_map = {
        img["noticia_id"]: img["image_url"]
        for img in imagens_resp.data
    }

    eventos = []
    for evento in selecao.data:
        eventos.append({
            "imagem": imagens_map.get(evento["id"]),
            "created_at": evento["created_at"],
            "titulo": evento["titulo"],
            "conteudo": evento["conteudo"],
            "categoria": evento["categoria"]
        })

    return render_template("eventos.html", evento=eventos)

# =======================
# ADMIN / CRIAR NOTÍCIA
# =======================
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.id != 1:
        return render_template("aviso.html")

    if request.method == 'POST':
        noticia = {
            "titulo": request.form["titulo"],
            "categoria": request.form["categoria"],
            "conteudo": request.form["conteudo"],
            "link1": request.form.get("link1"),
            "link2": request.form.get("link2"),
            "link3": request.form.get("link3"),
            "link4": request.form.get("link4"),
            "link5": request.form.get("link5"),
            "created_at": "now()"
        }

        insert = (
            supabase
            .table("noticias")
            .insert(noticia, default_to_null=False)
            .execute()
        )

        id_noticia = insert.data[0]["id"]

        arquivo = request.files.get("imagem1")
        if arquivo and arquivo.filename:
            upload = cloudinary.uploader.upload(arquivo)
            supabase.table("images_links").insert({
                "noticia_id": id_noticia,
                "image_url": upload["secure_url"]
            }).execute()

    return render_template("index.html")

# =======================
# FILTRAR NOTÍCIAS
# =======================
@app.route('/noticias', methods=['GET', 'POST'])
def filtrar():
    query = (
        supabase
        .table("noticias")
        .select(
            "id, titulo, created_at, conteudo, link1, link2, link3, link4, link5, categoria"
        )
        .order("created_at", desc=True)
    )

    filtro = None
    if request.method == "POST":
        filtro = request.form.get("filtro")
        if filtro:
            query = query.eq("categoria", filtro)

    selecao = query.execute()

    imagens_resp = (
        supabase
        .table("images_links")
        .select("image_url, noticia_id")
        .execute()
    )

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

    return render_template("noticias.html", noticias=noticias, filtragem=filtro)

# =======================
# LOGIN / CADASTRO / PERFIL
# =======================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["lemail"]
        senha = request.form["lsenha"].encode()

        result = supabase.table("users").select("*").eq("email", email).execute()
        if result.data:
            senha_hash = result.data[0]["senha"].encode()
            if bcrypt.checkpw(senha, senha_hash):
                user = User(result.data[0]["id"], email)
                login_user(user)
                return redirect(url_for("noticias"))
    return render_template("login.html")

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == "POST":
        email = request.form["cemail"]
        senha = request.form["csenha"]

        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
        supabase.table("users").insert({"email": email, "senha": senha_hash}).execute()
        return render_template("login.html")

    return render_template("cadastrar.html")

@app.route('/perfil')
@login_required
def perfil():
    return render_template("perfil.html", email=current_user.email)

@app.route('/contatos')
def contatos():
    return render_template("contatos.html")

if __name__ == "__main__":
    app.run(debug=True)
