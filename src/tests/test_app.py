import pytest # Módulo para teste
from src.model.colaborador_model import Colaborador
from src.app import create_app
import time

# -------------------CONFIGURAÇÕES---------------------------------------------------   
@pytest.fixture
def app():
    app = create_app()
    yield app
    
@pytest.fixture
def client(app):
    return app.test_client()

#--------------------------------------------------------------------------------------------

def test_pegar_todos_colaboradores(client):
    resposta = client.get('/colaborador/todos-colaboradores')
    assert resposta.status_code == 200
    

def test_desempenho_requisicao_get(client):
    comeco = time.time() #100
    
    for _ in range(100):
        resposta = client.get('/colaborador/todos-colaboradores')
    #     150
    fim = time.time() - comeco # 150 - 100
    
    assert fim < 1.0 # 1 seg
    
def test_desempenho_requisicao_post(client):
    comeco = time.time() #100
    
    colaborador = {
        'nome': 'teste josé',
        'email': 'teste@teste.com',
        'senha': '12345',
        'cargo': 'cargo teste',
        'salario': 123.45
    }
    
    for _ in range(100):
        resposta = client.post('/colaborador/cadastrar', json=colaborador)
        
    fim = time.time() - comeco 
    assert fim < 20.0
    
def test_soma():
    assert 2 + 2 == 3
    
