# RESPONSÁVEL PELA CRIAÇÃO DA INSTÂNCIA E CONFIGURAR O FLASK
# CREATE_APP() -> 
from flask import Flask
from src.controller.colaborador_controller import bp_colaborador
from src.model import db
from config import Config
from flask_cors import CORS
from flasgger import Swagger

# swagger_config = {
#     "headers":[],
#     "specs": [
#         {
#             "endpoint": "apispec",
#             "route": "/apispec.json",
#             "rule_filter": lambda rule: True,
#             "model_filter": lambda tag: True,
#         }
#     ],
#     "static_url_path": "/flasgger_static",
#     "swagger_ui": True,
#     "specs_route": "/apidocs/"
# }

swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json/',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

def create_app():
    app = Flask(__name__)
    CORS(app, origins='*') # <---- Ative o CORS para todas as rotas da API
    app.register_blueprint(bp_colaborador)
    app.config.from_object(Config) # Trouxemos a configuração do ambiente de desenvolvimento

    db.init_app(app) # Se inicia a conexão com o banco de dados
# <- Instanciando o Swagger e adicionando as configurações
    with app.app_context():
        db.create_all() #Cria as tabelas caso elas não existam
    Swagger(app, config=swagger_config)
    return app