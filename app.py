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
        db.session.commit() # para aplicar nossas alterações me nossa base de dados
        
        return jsonify({ 'message': 'Product added successfully' })

    return jsonify({ 'message': 'Invalid product data' }), 400


@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    # [x] Recuperar produto da base de dados
    # [x] Verificar se o produto existe
    # [x] Se existe, apagar da base de dados
    # [x] Se não existe, retornar 404 Not Found
    product = Product.query.get(product_id)

    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({ 'message': 'Product deleted successfully' })
    
    return jsonify({ 'message': 'Product not found' }), 404


@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)

    if product:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        })

    return jsonify({ 'message': 'Product not found' }), 404

# Criando uma rota raiz (página inicial) e função que será executado ao usuário fazer a requisição para essa rota
@app.route('/')
def hello_world():
    return 'Hello World!'

# Executando aplicação
if __name__ == '__main__':
    app.run(debug=True, port=3000)
