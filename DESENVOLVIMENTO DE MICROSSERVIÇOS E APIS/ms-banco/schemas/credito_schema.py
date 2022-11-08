from pydantic import BaseModel
from typing import Optional



class CreditoIn(BaseModel):

    nome_banco: str
    tipo_conta: str
    nome_titular: str
    limite_cartao: str

    class Config:
        orm_mode = True


class CreditoOut(BaseModel):

    id: str
    usuario: str
    nome_banco: str
    tipo_conta: str
    nome_titular: str
    limite_cartao: str

    class Config:
        orm_mode = True


class CreditoUpdate(BaseModel):
    nome_banco: str
    tipo_conta: str
    nome_titular: str
    limite_cartao: str

    class Config:
        orm_mode = True
