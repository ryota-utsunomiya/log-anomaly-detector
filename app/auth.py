import os
from jose import JWTError,jwt
from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hash=PasswordHash.recommended()

#パスワードが正しいかチェック
def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

#パスワードをハッシュ化
def get_password_hash(password):
    return password_hash.hash(password)

#JWTトークンを作成
def create_access_token(data:dict,expires_delta:timedelta|None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt
