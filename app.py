# Importações
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiJ9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'


login_manager = LoginManager()

# Database Config
db = SQLAlchemy(app)

login_manager.init_app(app)
login_manager.login_view = 'login' # nome da nossa rota de login

CORS(app)

# Modelagem (modelando o formato que os nosso dados terá para ir para o banco de dados)
'''
# Comandos de modelagem (no terminal):
- flask shell (ativa o terminal embutido do flask para aceitar comandos para nossa aplicação)
- db.create_all() (cria os nosso models/tables em nosso banco de dados configurado)
- db.drop_all() (exclui ou desfaz todas alterações que realizamos em nosso banco)
- db.session.add() (para adicionar algum registro a alguma tabela no banco de dados)
- db.session.commit() (para nossas alterações feitas serem de fato commitadas no banco de dados)
- exit() (sai do terminal integrado do flask)

* obs: você também pode realizar criação de registros em uma determinada table no banco através do próprio terminal integrado do flask, ex:
>>> user = User(username="admin", password="123")
>>> db.session.add(user)
>>> db.session.commit()

* dica: sempre que criar um novo model execute os comandos db.drop_all(), db.create_all() e db.session.commit() respectivamente, para resetar o banco de dados e não haver conflito com as novas tabelas caso estar apresentem algum tipo de relação.
'''


# User (id, username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


# Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


# Authentication Middleware
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Authentication Routes
@app.route('/login', methods=["POST"])
def login():
    data = request.json

    if ('username' not in data) or ('password' not in data):
        return jsonify({ 'message': 'Invalid user data' }), 404
    
    user = User.query.filter_by(username=data['username']).first()

    if not user:
        return jsonify({ 'message': 'Unauthorized. Invalid credentials' }), 401
    
    if data.get('password') != user.password:
        return jsonify({ 'message': 'Unauthorized. Invalid credentials' }), 401

    login_user(user)

    return jsonify({ 'message': 'Logged in successfully' })


@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({ 'message': 'Logged out successfully' })


# Product Routes
@app.route('/api/products/add', methods=["POST"])
@login_required
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
@login_required
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


@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({ 'message': 'Product not found' }), 404

    data = request.json

    if 'name' in data:
        product.name = data['name']
    
    if 'price' in data:
        product.price = data['price']
    
    if 'description' in data:
        product.description = data['description']
    
    db.session.commit()
    
    return jsonify({ 'message': 'Product updated successfully' })


@app.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()

    product_list = []

    for product in products:
        # Os detalhes do produto podem ser acessador na rota de detalhes de um produto
        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
        }

        product_list.append(product_data)

    return jsonify(product_list)

# Criando uma rota raiz (página inicial) e função que será executado ao usuário fazer a requisição para essa rota
@app.route('/')
def hello_world():
    return 'Hello World!'

# Executando aplicação
if __name__ == '__main__':
    app.run(debug=True, port=3000)
