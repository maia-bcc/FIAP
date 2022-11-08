from typing import List
from sqlalchemy.orm import Session
from models.credito import CreditoModel

class CreditoRepository:
    @staticmethod
    def find_all(db: Session) -> List[CreditoModel]:
        return db.query(CreditoModel).all()

    @staticmethod
    def save(db: Session, credito: CreditoModel) -> CreditoModel:
        if credito.id:
            db.merge(credito)
        else:
            db.add(credito)
        db.commit()
        return credito

    @staticmethod
    def find_by_id(db: Session, id: int) -> CreditoModel:
        return db.query(CreditoModel).filter(CreditoModel.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(CreditoModel).filter(CreditoModel.id == id).first() is not None