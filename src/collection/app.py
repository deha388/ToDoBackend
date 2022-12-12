import uvicorn
from fastapi import FastAPI, Request
from datetime import timedelta
from api_routes import register_blueprints
from fastapi.middleware.cors import CORSMiddleware
from config import load_config_yaml
from pydantic import BaseModel
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse

app = FastAPI()
cfg = load_config_yaml()

class Settings(BaseModel):
    authjwt_secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    authjwt_access_token_expires = timedelta(days=10)

@AuthJWT.load_config
def get_config():
    return Settings()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Init"])
async def read_root():
    return {"Hello": "World"}

if __name__ == '__main__':
    register_blueprints(app)
    uvicorn.run(app, port=cfg["app"]["port"])
