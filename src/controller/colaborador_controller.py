from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_senha, checar_senha
from flasgger import swag_from

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

# -------------------------------
# ✅ ROTA: Buscar todos os colaboradores
@bp_colaborador.route('/todos-colaboradores', methods=['GET'])
def pegar_dados_todos_colaboradores():
    colaboradores = db.session.execute(
        db.select(Colaborador)
    ).scalars().all()

    colaboradores = [colaborador.all_data() for colaborador in colaboradores]
    return jsonify(colaboradores), 200

# -------------------------------
# ✅ ROTA: Cadastrar novo colaborador
@bp_colaborador.route('/cadastrar', methods=['POST'])
def cadastrar_novo_colaborador():
    dados_requisicao = request.get_json()

    novo_colaborador = Colaborador(
        nome=dados_requisicao['nome'],
        email=dados_requisicao['email'],
        senha=hash_senha(dados_requisicao['senha']),
        cargo=dados_requisicao['cargo'],
        salario=dados_requisicao['salario']
    )

    db.session.add(novo_colaborador)
    db.session.commit()

    print(f"[DEBUG] Novo colaborador cadastrado: {novo_colaborador}")
    return jsonify({'mensagem': 'Colaborador cadastrado com sucesso'}), 201

# -------------------------------
# ✅ ROTA: Atualizar dados do colaborador
@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['PUT'])
def atualizar_dados_do_colaborador(id_colaborador):
    dados_requisicao = request.get_json()

    colaborador = db.session.execute(
        db.select(Colaborador).where(Colaborador.id == id_colaborador)
    ).scalar()

    if not colaborador:
        return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

    # Atualização de campos permitidos
    for campo in ['nome', 'cargo', 'salario', 'email', 'senha']:
        if campo in dados_requisicao:
            valor = dados_requisicao[campo]
            if campo == 'senha':
                valor = hash_senha(valor)
            setattr(colaborador, campo, valor)

    db.session.commit()
    print(f"[DEBUG] Colaborador {id_colaborador} atualizado: {colaborador}")
    return jsonify({'mensagem': 'Dados atualizados com sucesso'}), 200

# -------------------------------
# ✅ ROTA: Login do colaborador
@bp_colaborador.route('/login', methods=['POST'])
def login():
    dados_requisicao = request.get_json()
    email = dados_requisicao.get('email')
    senha = dados_requisicao.get('senha')

    if not email or not senha:
        return jsonify({'mensagem': 'Todos os dados precisam ser preenchidos'}), 400

    colaborador = db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar()

    print(f"[DEBUG] Login tentado para: {email}")
    if not colaborador:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404

    colaborador_dict = colaborador.to_dict()

    if checar_senha(senha, colaborador_dict.get('senha')):
        return jsonify({'mensagem': 'Login realizado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Credenciais inválidas'}), 400
