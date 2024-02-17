from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os


# Inicialização do aplicativo Flask
app = Flask(__name__)
load_dotenv()
# Configuração da chave secreta para proteger sessões e outros dados
app.config['SECRET_KEY'] = os.getenv("SECRETY_KEY")

# Configuração da URI do banco de dados SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

# Inicialização do objeto de banco de dados SQLAlchemy
db = SQLAlchemy(app)

# Inicialização do objeto Bcrypt para criptografia de senhas
bcrypt = Bcrypt(app)