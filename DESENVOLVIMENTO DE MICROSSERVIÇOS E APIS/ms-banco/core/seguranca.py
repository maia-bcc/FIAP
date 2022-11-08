from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from schemas.token_schema import TokenPayload


ALGORITHM="HS256"
SECRET_KEY="2723a36b2df31dd7aa14365ab928cc106dc0f38ea68251bfba07e62225baa338"

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Scheme de autenticação inválido")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token inválido")

            payload = self.decodeJWT(credentials.credentials)
            token_data = TokenPayload(**payload)
            return token_data.sub
        else:
            raise HTTPException(status_code=403, detail="Código de autorização inválido")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = self.decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


    def decodeJWT(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            return payload
        except:
            return {}