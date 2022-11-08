from typing import List
from sqlalchemy.orm import Session
from models.usuario import UsuarioModel

class UsuarioRepository:
    @staticmethod
    def find_all(db: Session) -> List[UsuarioModel]:
        return db.query(UsuarioModel).all()

    @staticmethod
    def save(db: Session, usuario: UsuarioModel) -> UsuarioModel:
        if usuario.id:
            db.merge(usuario)
        else:
            db.add(usuario)
        db.commit()
        return usuario

    @staticmethod
    def find_by_id(db: Session, id: int) -> UsuarioModel:
        return db.query(UsuarioModel).filter(UsuarioModel.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(UsuarioModel).filter(UsuarioModel.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        usuario = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
        if usuario is not None:
            db.delete(usuario)
            db.commit()