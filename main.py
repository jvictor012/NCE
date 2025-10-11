from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        return render_template('index.htlm')
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