import pytest
from httpx import AsyncClient,ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base,get_db
from app.main import app
import os

SQLALCHEMY_DATABASE_URL="sqlite:///.test.db"
engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})
TestingSessionLocal=sessionmaker(autoflush=False,bind=engine)

def override_get_db():
    db=TestingSessionLocal()
    try:
        db=TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db]=override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    
@pytest.mark.asyncio
async def test_signup_and_login():
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test")as ac:
        signup_res=await ac.post("/signup",params={"username":"testuser","password":"password123"})
        assert signup_res.status_code==200
        assert signup_res.json()["status"]=="success"
        
        login_res=await ac.post("/login",data={"username":"testuser","password":"password123"})
        assert login_res.status_code==200
        assert "access_token" in login_res.json()
        return login_res.json()["access_token"]
    
@pytest.mark.asyncio
async def test_create_log_unauthorized():  
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test")as ac:
        response=await ac.post("/logs",data={"message":"test error","source":"node-01"})
        assert response.status_code==401
        
@pytest.mark.asyncio
async def test_create_log_authrized():
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test")as ac:
        await ac.post("/signup",params={"username":"user1","password":"pwd"})
        login_res=await ac.post("/login",data={"username":"user1","password":"pwd"})
        token=login_res.json()["access_token"]
        headers={"Authorization":f"Bearer {token}"}
        
        
        response=await ac.post(
            "/logs",
            json={"message":"NORMAL log message","source":"node-01"},
            headers=headers
        )
        assert response.status_code==200
        assert response.json()["status"]=="success"
        assert "is_anomaly" in response.json()
        
@pytest.mark.asyncio
async def test_read_logs():
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test")as ac:
        response=await ac.get("/logs/")
        assert response.status_code==200
        assert isinstance(response.json(),list)
        