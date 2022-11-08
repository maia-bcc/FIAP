from typing import List
from datetime import timedelta
from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.usuario_schema import UsuarioIn, UsuarioOut, UsuarioUpdate
from database.database import engine, Base, get_db
from models.repository import UsuarioRepository
from models.usuario import UsuarioModel
from fastapi.security import OAuth2PasswordRequestForm
from core.seguranca import create_access_token, encrypt_string
from schemas.token_schema import Token
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Usuários'
)

@app.post("/login/access-token", response_model=Token)
def login_acesso_por_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):

    with db as session:
        usuario_database =  session.execute(
            select(UsuarioModel).where(UsuarioModel.usuario == form_data.username)
        ).scalar_one()

    if not usuario_database:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inexistente.",
        )
    elif usuario_database.senha != encrypt_string(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário ou senha incorreto.",
        )

    access_token_expires = timedelta(minutes=60000)
    access_token = create_access_token(
        subject=usuario_database.usuario, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/usuarios", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuarioReq: UsuarioIn,  db: Session = Depends(get_db)):
    usuarioReq.senha = encrypt_string(usuarioReq.senha)
    usuario = UsuarioRepository.save(db, UsuarioModel(**usuarioReq.dict()))
    return usuario


@app.get("/usuarios", response_model=List[UsuarioOut])
def pesquisar_usuarios(db: Session = Depends(get_db)):
    usuarios = UsuarioRepository.find_all(db)
    return usuarios


@app.put("/usuarios/{id}", response_model=UsuarioOut)
def atualizar_usuario(id: int, usuarioReq: UsuarioUpdate, db: Session = Depends(get_db)):
    if not UsuarioRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    usuarioReq.senha = encrypt_string(usuarioReq.senha)    
    usuarioDb = UsuarioRepository.save(db, UsuarioModel(id=id, **usuarioReq.dict()))
    return UsuarioRepository.find_by_id(db, id=id)



if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, log_level="info")
