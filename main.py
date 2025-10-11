from flask import Flask

app = Flask("__name__")

@app.route('/', methods=['GET', 'POST'])
def home():
    pass 

@app.route('/cadastrar', methods = ['GET', 'POST'])
def cadastrar():
    pass

@app.route('/login', methods = ['GET', 'POST'])
def login():
    pass


if '__name__' == '__main__':
    app.run(debug=True)