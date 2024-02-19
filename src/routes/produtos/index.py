from flask import jsonify, request
from src import app, db
from src.config.verificadorcampo import *
from src.models.models import Produtos, Categorias
from werkzeug.utils import secure_filename
import os
import uuid
import requests  # Import adicionado
import base64   # Import adicionado

UPLOAD_FOLDER = 'src/static/imagens'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    try:
        produtos = Produtos.query.all()
        lista_produtos = []
        for produto in produtos:
            categorias = [categoria.nome for categoria in produto.categoria]
            dados_produto = {
                'nome': produto.nome,
                'preco': produto.preco,
                'categorias': categorias,
                'banner': produto.banner
            }
            lista_produtos.append(dados_produto)
        return jsonify(lista_produtos), 200
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Erro ao listar produtos'}), 500


@app.route('/produtos', methods=['POST'])

def adicionar_produtos():
    try:
        produto_novo = request.get_json()
        nome = produto_novo['nome']
        preco = produto_novo['preco']
        categorias_nomes = produto_novo['categorias']
        banner = produto_novo.get('banner')  # Banner é opcional

        # Verificar se o produto já existe
        produto_existente = Produtos.query.filter_by(nome=nome).first()
        if produto_existente:
            return jsonify({'mensagem': 'Produto existente'}), 400

        # Verificar se as categorias existem
        categorias = []
        for categoria_nome in categorias_nomes:
            categoria_existente = Categorias.query.filter_by(nome=categoria_nome).first()
            if not categoria_existente:
                return jsonify({'mensagem': f'Categoria "{categoria_nome}" não encontrada'}), 400
            categorias.append(categoria_existente)

        # Salvar o banner se for fornecido
        nome_banner = None
        if banner:
            nome_banner = salvar_banner(banner)

        # Criar novo produto
        novo_produto = Produtos(nome=nome, preco=preco, banner=nome_banner)

        # Associar o novo produto às categorias encontradas
        novo_produto.categoria.extend(categorias)

        db.session.add(novo_produto)
        db.session.commit()

        return jsonify({'mensagem': 'Produto cadastrado com sucesso'}), 201
        
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Erro ao cadastrar novo produto'}), 500

def salvar_banner(banner):
    if banner.startswith('http'):
        # Se a URL for fornecida, gerar um nome único para o arquivo
        nome_arquivo = str(uuid.uuid4()) + '.png'
        # Baixar a imagem da URL e salvar no diretório UPLOAD_FOLDER
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        with open(caminho_arquivo, 'wb') as arquivo:
            response = requests.get(banner)
            arquivo.write(response.content)
        return nome_arquivo
    else:
        # Se o banner for uma imagem codificada em base64, decodificar e salvar no diretório UPLOAD_FOLDER
        extensao = banner.split(';')[0].split('/')[-1]
        if extensao.lower() not in ALLOWED_EXTENSIONS:
            raise ValueError("Extensão de arquivo inválida")
        nome_arquivo = str(uuid.uuid4()) + '.' + extensao
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        with open(caminho_arquivo, 'wb') as arquivo:
            encoded_image = banner.split(',')[1]
            decoded_image = base64.b64decode(encoded_image)
            arquivo.write(decoded_image)
        return nome_arquivo
