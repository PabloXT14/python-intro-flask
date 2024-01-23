# Importações
from flask import Flask

app = Flask(__name__)

# Criando uma rota raiz (página inicial) e função que será executado ao usuário fazer a requisição para essa rota
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True, port=3000)
