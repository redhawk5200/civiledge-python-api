from dotenv import load_dotenv
from core.config import get_config
from schema import schemas
from fastapi import FastAPI
from typing import List

load_dotenv()



app = FastAPI()

db: List[User]

@app.get("/")

async def root():
    return {"Hello": "Mundo"}



# config = get_config()
# print(config)
