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
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    administrador = db.Column(db.Boolean, default=False)





# Criar o database
# with app.app_context():
#     db.drop_all()
#     db.create_all()