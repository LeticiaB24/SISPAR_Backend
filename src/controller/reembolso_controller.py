
# db.session.bulk_save_objects(Lista dos json)

# id = 298
from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db
from datetime import datetime
from flasgger import swag_from

# Cria um blueprint para as rotas de reembolso
bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolso')

# -------------------------------
# ✅ ROTA: Criar um ou vários reembolsos
@bp_reembolso.route('/solicitar', methods=['POST'])
@swag_from('../docs/reembolso/solicitar.yml')
def solicitar_reembolso():
    dados = request.get_json()

    if not isinstance(dados, list):  # Se for um único reembolso, transforma em lista
        dados = [dados]

    reembolsos = []
    for item in dados:
        try:
            # Cria uma instância de reembolso com os dados recebidos
            reembolso = Reembolso(
                colaborador=item['colaborador'],
                empresa=item['empresa'],
                num_prestacao=item['num_prestacao'],
                descricao=item.get('descricao'),
                data=datetime.strptime(item['data'], '%Y-%m-%d'),
                tipo_reembolso=item['tipo_reembolso'],
                centro_custo=item['centro_custo'],
                ordem_interna=item.get('ordem_interna'),
                divisao=item.get('divisao'),
                pep=item.get('pep'),
                moeda=item['moeda'],
                distancia_km=item.get('distancia_km'),
                valor_km=item.get('valor_km'),
                valor_faturado=item['valor_faturado'],
                despesa=item.get('despesa'),
                id_colaborador=item['id_colaborador'],
                status=item.get('status', 'Em analise')
            )
            reembolsos.append(reembolso)
        except KeyError as e:
            return jsonify({'erro': f'Campo obrigatório ausente: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'erro': f'Erro ao processar reembolso: {str(e)}'}), 400

    db.session.bulk_save_objects(reembolsos)  # Salva todos de uma vez
    db.session.commit()
    return jsonify({'mensagem': f'{len(reembolsos)} reembolso(s) registrado(s) com sucesso'}), 201

# -------------------------------
# ✅ ROTA: Visualizar um reembolso por número de prestação
@bp_reembolso.route('/<int:num_prestacao>', methods=['GET'])
@swag_from('../docs/reembolso/visualizar.yml')
def visualizar_reembolso(num_prestacao):
    reembolso = Reembolso.query.filter_by(num_prestacao=num_prestacao).first()

    if not reembolso:
        return jsonify({'mensagem': 'Reembolso não encontrado'}), 404

    return jsonify(reembolso.to_dict()), 200  # Usa o método to_dict() do modelo

# -------------------------------
# ✅ ROTA: Listar todos os reembolsos
@bp_reembolso.route('/', methods=['GET'])
def listar_todos_reembolsos():
    reembolsos = Reembolso.query.all()
    return jsonify([r.to_dict() for r in reembolsos]), 200

# -------------------------------
# ✅ ROTA: Atualizar o status ou outro campo de um reembolso
@bp_reembolso.route('/<int:id>', methods=['PUT'])
def atualizar_reembolso(id):
    reembolso = Reembolso.query.get(id)

    if not reembolso:
        return jsonify({'mensagem': 'Reembolso não encontrado'}), 404

    data = request.get_json()

    # Atualiza apenas os campos que vierem na requisição
    for campo in ['status', 'descricao', 'valor_faturado', 'tipo_reembolso']:
        if campo in data:
            setattr(reembolso, campo, data[campo])

    try:
        db.session.commit()
        return jsonify({'mensagem': 'Reembolso atualizado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

# -------------------------------
# ✅ ROTA: Deletar um reembolso
@bp_reembolso.route('/<int:id>', methods=['DELETE'])
def deletar_reembolso(id):
    reembolso = Reembolso.query.get(id)

    if not reembolso:
        return jsonify({'mensagem': 'Reembolso não encontrado'}), 404

    try:
        db.session.delete(reembolso)
        db.session.commit()
        return jsonify({'mensagem': 'Reembolso deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400
