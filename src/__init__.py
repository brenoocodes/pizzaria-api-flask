from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import os


# Inicialização do aplicativo Flask
app = Flask(__name__)
load_dotenv()
# Configuração da chave secreta para proteger sessões e outros dados
app.config['SECRET_KEY'] = "FsjdejefweFRFWG#3452%@%@TRWWewrgwg4rtwghyettwwt254536g"

# Configuração da URI do banco de dados SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:breno19042003@localhost/pizzaria"

# Inicialização do objeto de banco de dados SQLAlchemy
db = SQLAlchemy(app)

# Inicialização do objeto Bcrypt para criptografia de senhas
bcrypt = Bcrypt(app)

cors = CORS(app)