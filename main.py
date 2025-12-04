from flask import Flask, render_template, request, send_file
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    UserMixin,
    current_user,
)
import bcrypt
from bd import executar_comandos

app = Flask(__name__)
app.secret_key = 'chave_muito_secreta'
# ===== Configuração do Flask-Login (ativa e correta) =====
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_submit"

class User(UserMixin):
    def __init__(self, id, nome, email, senha=None):
        # flask-login exige atributo .id (string ou int)
        self.id = str(id)
        self.nome = nome
        self.email = email
        self.senha = senha

    def __repr__(self):
        return f"<User {self.id} {self.nome}>"


@login_manager.user_loader
def load_user(user_id):
    try:
        query = "SELECT id, nome, matricula, email FROM user WHERE id = ?"
        valores = (user_id,)
        resultado = executar_comandos(query, valores, fetchone=True, retornar_id=False)

        if resultado:
            id_db, nome_usuario, email = resultado
            return User(id_db, nome_usuario, email)
    except Exception as e:
        app.logger.error("load_user error: %s", e)

    return None



@app.route('/noticias')
def noticias():
    return render_template('home_user.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Campos de texto
        titulo = request.form['titulo']
        categoria = request.form['categoria']
        conteudo = request.form['conteudo']
        link1 = request.form.get('link1')  # get() evita erro se vazio
        link2 = request.form.get('link2')
        link3 = request.form.get('link3')
        link4 = request.form.get('link4')
        link5 = request.form.get('link5')

        # Imagens
        imagem1 = request.files['imagem1']  # pega o arquivo do form
        imagem2 = request.files.get('imagem2')
        imagem3 = request.files.get('imagem3')
        binario = imagem1.read()
    return render_template('index.html', imagem=False)

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == "POST":
        return render_template('perfil.html')
    else:
        return render_template('perfil.html')



@app.route('/cadastrar', methods = ['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        try:
            nome = request.form.get('cenome')
            email = request.form.get('cemail')
            matricula = request.form.get('cmatricula')
            senha = request.form.get('csenha')
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            query = '''INSERT INTO user(email, matricula, senha_hash) VALUES(%s,%s,%s)'''
            valores = (email, matricula, senha_hash)
            executar_comandos(query, valores, retornar_id=False)
            mensagem = "Cadastro efetuado com sucesso!"
            return render_template('cadastrar.html', mensagem = mensagem)
        
        except Exception as e:
            app.logger.exception("Erro ao cadastrar usuário: %s", e)
            erro = "Ocorreu um erro. Por favor, tente novamente!"
            return render_template("cadastro.html", erro=erro)
        
    return render_template('cadastrar.html')




@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form['lmatricula']
        senha = request.form['lsenha']
        return render_template('index.html', mat = matricula, sen = senha)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)