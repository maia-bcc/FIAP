from sqlalchemy import Column, Integer, String
from database.database import Base


class CreditoModel(Base):
    __tablename__ = "credito"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String)
    nome_banco = Column(String)
    tipo_conta = Column(String)
    nome_titular = Column(String)
    limite_cartao = Column(Integer)
