import sys
from pathlib import Path
# Obtém o diretório do arquivo atual e seu diretório pai
file = Path(__file__).resolve()
parent = file.parent.parent.parent
# Adiciona o diretório pai ao sys.path
sys.path.append(str(parent))
# Importa os módulos necessários
from datetime import datetime
from src import db, app

# Definição da classe Funcionarios
class Funcionarios(db.Model):
    __tablename__ = 'funcionarios'
    # Atributos da tabela funcionarios
    matricula = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    administrador = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
 

class Categorias(db.Model):
    __tablename__ = 'categorias'
    #atributos
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Produtos(db.Model):
    __tablename__= 'produtos'
    #atributos
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    preco = db.Column(db.Float, nullable=False, default=0.0)
    banner = db.Column(db.String(256), default='banner.png')
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #relação com a tabela categorias
    categoria = db.relationship('Categorias', secondary='produtos_categorias', backref=db.backref('produtos', lazy='dynamic'))


#relação n => muitos produtos e categorias

class ProdutosCategorias(db.Model):
    __tablename__ = 'produtos_categorias'
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), primary_key=True)


class Pedidos(db.Model):
    __tablename__ = 'pedidos'
    pedido_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    mesa = db.Column(db.Integer, unique=True, nullable=False)
    confirmado = db.Column(db.Boolean, default=False)
    finalizado = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class PedidosProdutos(db.Model):
    __tablename__ = 'pedidos_produtos'
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.pedido_id'), primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    # Outros atributos relevantes podem ser adicionados aqui, como preço unitário na hora do pedido, por exemplo

    # Define a relação com a tabela de pedidos
    pedido = db.relationship('Pedidos', backref=db.backref('produtos', lazy='dynamic'))

    # Define a relação com a tabela de produtos
    produto = db.relationship('Produtos', backref=db.backref('pedidos', lazy='dynamic'))



# Criar o database
# with app.app_context():
#     db.drop_all()
#     print('excluido com sucesso')
#     db.create_all()
#     print('criado com sucesso')