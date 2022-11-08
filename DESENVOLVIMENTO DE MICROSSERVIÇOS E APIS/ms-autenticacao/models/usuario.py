from sqlalchemy import Column, Integer, String
from database.database import Base


class UsuarioModel(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nomecompleto = Column(String)
    usuario = Column(String)
    telefone = Column(String)
    email = Column(String)
    datacadastro = Column(String)
    senha = Column(String)
