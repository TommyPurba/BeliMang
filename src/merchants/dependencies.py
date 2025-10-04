from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

def get_current_admin(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload
