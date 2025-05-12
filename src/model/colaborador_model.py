from src.model import db # Traz a instancia SQLAlchemy para este arquivo
from sqlalchemy.schema import Column # Traz o recurso que transforma atributos em colunas 
from sqlalchemy.types import String, DECIMAL, Integer # Traz o recurso que identifica os tipos de dados para as colunas

class Colaborador(db.Model): # db.Model -> Mapear e criar a tabela
    
#---------------- Atributos --------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True) # id INT AUTO_INCREMENT PRIMARY KEY
    nome = Column(String(255)) # nome VARCHAR(255)
    email = Column(String(150))
    senha = Column(String(255))
    cargo = Column(String(100))
    salario = Column(DECIMAL(10,2)) 
#-----------------------------------------------------------------------------------------------
    
#------------------ CONSTRUTOR ---------------------------------------------------------------
    def __init__ (self, nome, email, senha, cargo, salario):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cargo = cargo
        self.salario = salario
#----------------------------------------------------------------------------------------------        

    def to_dict(self) -> dict: 
        return {
            'email': self.email,
            'senha': self.senha
        }
        
    def all_data(self) -> dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'cargo': self.cargo,
            'salario': self.salario
        }