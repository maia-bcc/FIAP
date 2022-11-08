from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from models.usuario import UsuarioModel
from models.repository import UsuarioRepository
import hashlib

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/login/access-token"
)


ALGORITHM="HS256"
SECRET_KEY="2723a36b2df31dd7aa14365ab928cc106dc0f38ea68251bfba07e62225baa338"

def create_access_token(
            subject: Union[str, Any], 
            expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes= 60000
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature