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


def euron_helper(doc):
    doc["iid"] = str(doc["_id"])
    del doc["_id"]
    return doc


@app.get("/students/data")
async def get_data():
    iterms = []
    cursor = euroon_data.find({})
    async for document in cursor:
        iterms.append(euron_helper(document))
    return iterms




@app.delete("/students/delete/{id}")
async def delete_student_data(id: int):
    result = await euroon_data.delete_one({"id": id})
    
    if result.deleted_count == 1:
        return {"message": "Data deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail="Data not found")
        
@app.post("/students/update/{id}")
async def update_student_data(id: int,data:student_login):
    result = await euroon_data.update_one({"id": id}, {"$set": data.model_dump()})
    if result.modified_count == 1:
        return {"message": "Data updated Successfully"}
    else:
        raise HTTPException(status_code=404, detail="Data not found")
