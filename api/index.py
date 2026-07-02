from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from enum import Enum
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import httpx
import logging

load_dotenv()

logger = logging.getLogger("enquiry")

app = FastAPI(
    root_path="/year-round-security-bundle/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# MongoDB
# ─────────────────────────────────────────────
_client = None


def get_collection():
    global _client
    if _client is None:
        _client = MongoClient(os.getenv("MONGO_URI"))
    return _client["secureitlab_compaigning"]["enquiry"]


# ─────────────────────────────────────────────
# Twenty CRM config
# ─────────────────────────────────────────────
TWENTY_GRAPHQL_URL = os.getenv("TWENTY_GRAPHQL_URL", "https://secureitlab.twenty.com/graphql")
TWENTY_API_KEY = os.getenv("TWENTY_API_KEY")

# Map form display values → Twenty CRM enum values
COMPANY_SIZE_MAP = {
    "1-50 Employees":    "OPT1_50_EMPLOYEES",
    "51-200 Employees":  "OPT51_200_EMPLOYEES",
    "201-1000 Employees": "OPT201_1000_EMPLOYEES",
    "1000+ Employees":   "OPT1000_EMPLOYEES",
}

LOOKING_TO_START_MAP = {
    "Immediately":    "IMMEDIATELY",
    "Within 1 Month": "WITHIN_1_MONTH",
    "1-3 Months":     "OPT1_3_MONTHS",
    "Just Exploring": "JUST_EXPLORING",
}


# ─────────────────────────────────────────────
# Pydantic model
# ─────────────────────────────────────────────
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
    company: str = ""
    email: EmailStr
    phone: str = ""
    company_size: CompanySize
    looking_to_start: LookingToStart


# ─────────────────────────────────────────────
# Twenty CRM helper
# ─────────────────────────────────────────────
async def push_to_twenty_crm(form: EnquiryForm) -> dict:
    """Create a YearRoundSecurityBundle record in Twenty CRM via GraphQL."""

    if not TWENTY_API_KEY:
        logger.warning("TWENTY_API_KEY not set — skipping CRM push")
        return {"crm": "skipped", "reason": "API key not configured"}

    mutation = """
    mutation CreateYearRoundSecurityBundle($input: YearRoundSecurityBundleCreateInput!) {
        createYearRoundSecurityBundle(data: $input) {
            id
            name
            lastname
            company
            email
            phone
            companysize
            lookingtostart
        }
    }
    """

    variables = {
        "input": {
            "name":           form.firstname,
            "lastname":       form.lastname,
            "company":        form.company,
            "email":          {"primaryEmail": form.email},
            "phone":          {"primaryPhoneNumber": form.phone},
            "companysize":    COMPANY_SIZE_MAP[form.company_size.value],
            "lookingtostart": LOOKING_TO_START_MAP[form.looking_to_start.value],
        }
    }

    headers = {
        "Authorization": f"Bearer {TWENTY_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            TWENTY_GRAPHQL_URL,
            json={"query": mutation, "variables": variables},
            headers=headers,
        )

    result = resp.json()

    if "errors" in result:
        logger.error(f"Twenty CRM error: {result['errors']}")
        return {"crm": "error", "details": result["errors"]}

    crm_id = result.get("data", {}).get("createYearRoundSecurityBundle", {}).get("id", "")
    return {"crm": "success", "crm_id": crm_id}


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.post("/api/enquiry")
async def submit_enquiry(form: EnquiryForm):
    try:
        # 1. Save to MongoDB
        data = form.model_dump()
        result = get_collection().insert_one(data)
        mongo_id = str(result.inserted_id)

        # 2. Push to Twenty CRM
        crm_result = await push_to_twenty_crm(form)

        return {
            "message": "Enquiry submitted successfully",
            "id": mongo_id,
            "crm": crm_result,
        }
    except Exception as e:
        logger.exception("Enquiry submission failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api")
async def root():
    return {"status": "API is running"}