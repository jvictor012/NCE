from flask import Flask, render_template, request

app = Flask(__name__)

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
        imagem1 = request.files.get('imagem1')
        imagem2 = request.files.get('imagem2')
        imagem3 = request.files.get('imagem3')

        # Aqui você pode salvar as imagens e os dados no banco ou pasta

        return render_template('index.html', 
                               titulo=titulo, 
                               categoria=categoria,
                               conteudo=conteudo,
                               link1=link1,
                               link2=link2,
                               link3=link3,
                               link4=link4,
                               link5=link5,
                               imagem1=imagem1.filename if imagem1 else None,
                               imagem2=imagem2.filename if imagem2 else None,
                               imagem3=imagem3.filename if imagem3 else None)

    return render_template('index.html')


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == "POST":
        return render_template('perfil.html')
    else:
        return render_template('perfil.html')



@app.route('/cadastrar', methods = ['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        return render_template('cadastrar.html')
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