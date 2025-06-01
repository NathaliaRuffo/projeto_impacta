from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import pymysql
from functools import wraps
pymysql.install_as_MySQLdb()

# Adicionando imports para o teste de conexão
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://nathalia:12345@localhost/projeto_impacta'
app.secret_key = 'sua_chave_secreta_aqui'  # Configure uma chave secreta para sessões


# Teste de conexão com o banco de dados
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(engine.url):
    create_database(engine.url)
print(f"Database exists: {database_exists(engine.url)}")

db = SQLAlchemy(app)

# Modelo para itens
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

# Modelo para usuários
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

# Decorador para proteger rotas que exigem login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para proteger rotas que exigem admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
@login_required
def add_item():
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])
    new_item = Item(nome=nome, quantidade=quantidade, preco=preco, ativo=True)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.nome = request.form['nome']
        item.quantidade = int(request.form['quantidade'])
        item.preco = float(request.form['preco'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/toggle/<int:id>')
@login_required
def toggle_item(id):
    item = Item.query.get_or_404(id)
    item.ativo = not item.ativo
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash("Item deletado com sucesso!", "success")
    return redirect(url_for('index'))

@app.route('/delete_all', methods=['POST', 'GET'])
@login_required
def delete_all_items():
    db.session.query(Item).delete()
    db.session.commit()
    flash("Todos os itens foram deletados com sucesso!", "success")
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
@login_required
def search_item():
    query = request.args.get('query')
    if query:
        items = Item.query.filter(Item.nome.ilike(f"%{query}%")).all()
        if not items:  # Se não houver resultados
            flash('Produto não encontrado.', 'danger')
            return redirect(url_for('index'))  # Redireciona para /index
    else:
        items = Item.query.all()
        flash("Nenhum termo de busca foi inserido.", 'warning')
        return redirect(url_for('index'))  # Redireciona para /index
    
    # Se produtos forem encontrados, renderiza a página com os resultados
    return render_template('index.html', items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/create_user', methods=['GET', 'POST'])
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Usuário já existe!', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('login'))  # Redireciona para a página de login após criar o usuário
    return render_template('create_user.html')

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Conexão com o banco de dados estabelecida com sucesso!")
        except SQLAlchemyError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    
    app.run(debug=True)
