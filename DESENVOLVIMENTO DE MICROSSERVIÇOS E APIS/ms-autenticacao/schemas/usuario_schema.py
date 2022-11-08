from pydantic import BaseModel
from typing import Optional



class UsuarioIn(BaseModel):

    nomecompleto : str
    usuario: str
    telefone: str
    email: str
    datacadastro: str
    senha: str

    class Config:
        orm_mode = True


class UsuarioOut(BaseModel):

    id: str
    nomecompleto : str
    usuario: str
    telefone: str
    email: str
    datacadastro: str
#    senha: str

    class Config:
        orm_mode = True


class UsuarioUpdate(BaseModel):
    senha: str

    class Config:
        orm_mode = True
