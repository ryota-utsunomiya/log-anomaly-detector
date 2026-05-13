import joblib
import pandas as pd
import time
from fastapi import FastAPI,Depends,HTTPException,status,BackgroundTasks
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt,JWTError
from . import models,auth,database,schemas
from .database import SessionLocal, engine, get_db
from .services.notifier import send_discord_notification
import os


app=FastAPI()

models.Base.metadata.create_all(bind=engine)

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "ml", "bgl_logistic_model.pkl")

try:
    print(f"DEBUG: Trying to load model from: {model_path}") # これでどこを探してるか分かります
    ml_model = joblib.load(model_path)
    print("✅ SUCCESS: Model loaded successfully!")
except Exception as e:
    print(f"❌ ERROR: Model load failed: {e}")
    ml_model = None

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,auth.SECRET_KEY,algorithms=[auth.ALGORITHM])
        username:str=payload.get("sub")
        if username is None:
            raise
        HTTPException(status_code=401,detail="無効なトークンです")
        return username
    except JWTError:
        raise HTTPException(status_code=401,detail="認証に失敗しました")
 
 #サインアップ   
@app.post("/signup")
def login(username:str,password:str,db:Session=Depends(database.get_db)):
    user=models.User(username=username,hashed_password=auth.get_password_hash(password))
    db.add(user)
    db.commit()
    return {"status":"success"}

#ログイン
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.username==form_data.username).first()
    if not user or not auth.verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="名前かパスワードが違います")
    token=auth.create_access_token({"sub":user.username})
    return{"access_token":token,"token_type":"bearer"}
    
#ログ投稿
@app.post("/logs")
def create_log(
    log_in: schemas.LogCreate,
    background_tasks: BackgroundTasks,
    db: Session=Depends(database.get_db),
    current_user: str=Depends(get_current_user)
):
  
    
    input_data=pd.DataFrame([{
        "content": log_in.message,
        "node": log_in.source
    }])

    #推論
    is_anomaly=False
    
    if ml_model:
        print("Model loaded successfully!")
        input_data=input_data[['content','node']]
        prediction=ml_model.predict(input_data)[0]
        is_anomaly=True if int(prediction)==1 else False
        print(f"DEBUG: prediction_raw={prediction}, is_anomaly={is_anomaly}")
        
    #異常なら通知を実行
    if is_anomaly:
        print("DEBUG: Anomaly detected! Sending Discord notification...")
        background_tasks.add_task(
            send_discord_notification,
            message=log_in.message,
            source=log_in.source
        )
    else:
        print("DEBUG: Normal log. No notification sent.")
    
    
    #DBへ保存
    db_log=models.Log(
        message=log_in.message,
        source=log_in.source,
        is_anomaly=is_anomaly
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return {"status":"success","is_anomaly":is_anomaly,"user":current_user}

@app.get("/logs/")
def read_logs(db:Session=Depends(get_db)):
    return db.query(models.Log).all()


