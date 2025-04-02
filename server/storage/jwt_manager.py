from datetime import datetime, timedelta
import jwt
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException

class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.security = HTTPBearer()

    async def verify_token(self, request: Request):
        credentials = await self.security(request)
        try:
            payload = jwt.decode(
                credentials.credentials,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def create_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
