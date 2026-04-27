from sqlalchemy import Column,Integer,String,DateTime,Boolean
from datetime import datetime,timezone
from database import Base

class User(Base):
    __tablename__="users"
    
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,Unique=True,index=True)
    hashed_password=Column(String)

class Log(Base):
    __tablename__="logs"

    id=Column(Integer,primary_key=True,index=True)
    message=Column(String) #ログの内容
    source=Column(String) #送信元
    timestamp=Column(DateTime,default=lambda:datetime.now(timezone.utc)) #時間
    is_anomaly=Column(Boolean,default=False) #異常フラグ
    
