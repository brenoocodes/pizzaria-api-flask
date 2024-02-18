from flask import jsonify, request
from src import app, db
from src.config.verificadorcampo import *
from src.models.models import Produtos, Categorias
from werkzeug.utils import secure_filename
import os

# UPLOAD_FOLDER = 'src/static/imagens'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/produtos', methods=['POST'])
@verifica_campos_tipos(['nome', 'preco', 'categorias'], {'nome': str, 'preco': float, 'categorias': list})
def adicionar_produtos():
    try:
        produto_novo = request.get_json()
        nome = produto_novo['nome']
        preco = produto_novo['preco']
        categorias_nomes = produto_novo['categorias']

        # Verificar se o produto já existe
        produto_existente = Produtos.query.filter_by(nome=nome).first()
        if produto_existente:
            return jsonify({'mensagem': 'Produto existente'}), 400

        categorias = []
        for categoria_nome in categorias_nomes:
            categoria_existente = Categorias.query.filter_by(nome=categoria_nome).first()
            if not categoria_existente:
                return jsonify({'mensagem': f'Categoria "{categoria_nome}" não encontrada'}), 400
            categorias.append(categoria_existente)

        # Criar novo produto
        novo_produto = Produtos(nome=nome, preco=preco)
        
        # Associar o novo produto às categorias encontradas
        novo_produto.categoria.extend(categorias)

        db.session.add(novo_produto)
        db.session.commit()

        return jsonify({'mensagem': 'Produto cadastrado com sucesso'}), 201
        
    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Erro ao cadastrar novo produto'}), 500


