from flask import jsonify, request
from src.config.login import *
from src.config.verificadorcampo import *
from src import app, db
from src.models.models import Categorias

#Cadastrar categorias
@app.route('/categorias', methods=['POST'])
@token_obrigatorio
@verifica_campos_tipos(['nome'], {'nome': str})
def cadastrar_categoria(adm):
    try:
        if not adm.administrador:
            return jsonify({'mensagem': 'Você não tem permissão para cadastrar uma nova categoria'}), 403
        try:
            nova_categoria = request.get_json()
            nome = nova_categoria['nome']
            cat_existente = Categorias.query.filter_by(nome=nome).first()
            if cat_existente:
                return jsonify({'mensagem': 'Categoria já cadastrada'}),400
            categoria_cadastrada = Categorias(
                nome = nome
            )
            db.session.add(categoria_cadastrada)
            db.session.commit()
            return jsonify({'mensagem': f'A categoria {nome} foi cadastrada com sucesso'})
        except Exception as e:
            print(e)
            return jsonify({'mensagem': 'Ocorreu algum erro ao tentar cadastrar uma nova categoria'}), 500

    except Exception as e:
        print(e)
        return jsonify({'mensagem': 'Ocorreu algum erro interno'}), 500

@app.route('/categorias/<int:id>', methods=['PUT'])
@token_obrigatorio
@verifica_alterar(['nome'], {'nome': str})
def alterar_categoria(adm, id):
    if not adm.administrador:
        return jsonify({'Mensagem': 'Você não tem permissão para trocar uma categoria'}), 403
    try:
        categoria_alterar = request.get_json()
        categoria = Categorias.query.filter_by(id=id).first()
        if not categoria:
            return jsonify({'Mensagem': 'Essa categoria não está cadastrada'}), 400
        
        if 'nome' in categoria_alterar:
            novo_nome = categoria_alterar['nome']
            if novo_nome != categoria.nome:
                categoria_existente = Categorias.query.filter_by(nome=novo_nome).first()
                if categoria_existente:
                    return jsonify({'Mensagem': f'Você está tentando alterar o nome da categoria para {novo_nome} e ela já existe.'}), 400
                categoria.nome = novo_nome
        db.session.commit()
        return jsonify({'Mensagem': f'A categoria {categoria.nome} foi alterada com sucesso para {novo_nome}'}), 200
    except Exception as e:
        print(e)
        return jsonify({'Mensagem': 'Erro ao alterar essa categoria'}), 500
