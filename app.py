# Importações
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'


# Database Config
db = SQLAlchemy(app)


# Modelagem (modelando o formato que os nosso dados terá para ir para o banco de dados)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


# Product Routes
@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json

    if 'name' in data and 'price' in data:
        # .get('value', 'defaultValue') => retornar uma valor especificado do dicionário ou o valor padrão se este valor não existir
        product = Product(name=data['name'], price=data['price'], description=data.get('description', ''))

        # Cadastrando produto no banco
        db.session.add(product)
        db.session.commit()
        
        return jsonify({ 'message': 'Product added successfully' })

    return jsonify({ 'message': 'Invalid product data' }), 400


# Criando uma rota raiz (página inicial) e função que será executado ao usuário fazer a requisição para essa rota
@app.route('/')
def hello_world():
    return 'Hello World!'

# Executando aplicação
if __name__ == '__main__':
    app.run(debug=True, port=3000)
