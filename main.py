from flask import Flask, render_template, request, send_file
import bcrypt
from bd import executar_comandos
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'chave_muito_secreta'



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
        # Salva na memória para a outra rota
        with open('temp_image', 'wb') as f:
            f.write(binario)
        return render_template('index.html', imagem=True)
    return render_template('index.html', imagem=False)

# Rota para enviar a imagem
@app.route('/imagem')
def imagem():
    with open('temp_image', 'rb') as f:
        original = BytesIO(f.read())
    return send_file(original, download_name='imagem.jpg', mimetype='image/jpeg')


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == "POST":
        return render_template('perfil.html')
    else:
        return render_template('perfil.html')



@app.route('/cadastrar', methods = ['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        email = request.form.get('cemail')
        matricula = request.form.get('cmatricula')
        senha = request.form.get('csenha')
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = '''INSERT INTO usuario(email, matricula, senha_hash) VALUES(%s,%s,%s)'''
        valores = (email, matricula, senha_hash)
        executar_comandos(query, valores, retornar_id=False)
        mensagem = "Cadastro efetuado com sucesso!"
        return render_template('cadastrar.html', mensagem = mensagem)
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