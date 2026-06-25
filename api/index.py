from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from enum import Enum
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reuse MongoDB connection across serverless invocations
_client = None


def get_collection():
    global _client
    if _client is None:
        _client = MongoClient(os.getenv("MONGO_URI"))
    return _client["secureitlab_compaigning"]["enquiry"]


class CompanySize(str, Enum):
    small = "1-50 Employees"
    medium = "51-200 Employees"
    large = "201-1000 Employees"
    enterprise = "1000+ Employees"


class LookingToStart(str, Enum):
    immediately = "Immediately"
    within_1_month = "Within 1 Month"
    one_to_3_months = "1-3 Months"
    just_exploring = "Just Exploring"


class EnquiryForm(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    company_size: CompanySize
    looking_to_start: LookingToStart


@app.post("/api/enquiry")
async def submit_enquiry(form: EnquiryForm):
    try:
        data = form.model_dump()
        result = get_collection().insert_one(data)
        return {
            "message": "Enquiry submitted successfully",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api")
async def root():
    return {"status": "API is running"}
