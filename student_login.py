from fastapi import FastAPI,HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client=AsyncIOMotorClient(MONGO_URI)
db=client["genaiproject"]
euroon_data=db["student_login"]

app = FastAPI()

class student_login(BaseModel):
    id:int
    name:str
    stream:str
    mobile_no:int

@app.post("/students/insert")
async def student_data(data:student_login):
    result = await euroon_data.insert_one(data.model_dump())
    return {"message":"Data inserted Successfully"}

