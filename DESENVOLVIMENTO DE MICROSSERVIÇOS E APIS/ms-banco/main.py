import uvicorn
from fastapi import FastAPI, status, Depends, HTTPException
from core.seguranca import  JWTBearer
from typing import List
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.credito_schema import CreditoIn, CreditoOut, CreditoUpdate
from database.database import engine, Base, get_db
from models.repository import CreditoRepository
from models.credito import CreditoModel
from fastapi.security import OAuth2PasswordRequestForm


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Banco'
)




@app.post("/contas", response_model=CreditoOut, status_code=status.HTTP_201_CREATED)
def cadastrar_credito(creditoReq: CreditoIn,  db: Session = Depends(get_db), usuario = Depends(JWTBearer())):
    credito = CreditoRepository.save(db, CreditoModel(usuario=usuario,**creditoReq.dict()))
    return credito

@app.put("/contas/{user}", response_model=CreditoOut)
def atualizar_usuario(id: int, creditoReq: CreditoUpdate, db: Session = Depends(get_db), usuario = Depends(JWTBearer())):
    if not CreditoRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada"
        )   
    CreditoDb = CreditoRepository.save(db, CreditoModel(id=id, **creditoReq.dict()))
    return CreditoRepository.find_by_id(db, id=id)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8002, log_level="info")