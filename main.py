from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI(title="Team P7 Backend API")

# CORS Enable karna taaki Netlify website isse connect ho sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "database.json"

# Database Initialize karna
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"members": [], "partners": [], "applications": []}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Data Models
class Member(BaseModel):
    id: Optional[str] = None
    name: str
    role: str
    pfp: Optional[str] = ""  # Yahan save hoga tumhara Profile Picture ka URL!
    rank: Optional[str] = "Member"

class Partner(BaseModel):
    id: Optional[str] = None
    name: str
    logo: Optional[str] = ""
    link: Optional[str] = ""

class Application(BaseModel):
    id: Optional[str] = None
    username: str
    skills: str
    age: str
    status: Optional[str] = "Pending"

# --- ROUTES ---

@app.get("/")
def home():
    return {"status": "Team P7 Backend is Running Successfully!"}

# Members API
@app.get("/api/members", response_model=List[Member])
def get_members():
    return load_data()["members"]

@app.post("/api/members")
def add_member(member: Member):
    data = load_data()
    member_dict = member.model_dump()
    if not member_dict["id"]:
        member_dict["id"] = str(len(data["members"]) + 1)
    data["members"].append(member_dict)
    save_data(data)
    return {"message": "Member added successfully", "member": member_dict}

# Applications API
@app.post("/api/apply")
def apply_now(app_data: Application):
    data = load_data()
    app_dict = app_data.model_dump()
    app_dict["id"] = str(len(data["applications"]) + 1)
    data["applications"].append(app_dict)
    save_data(data)
    return {"message": "Application submitted!"}

@app.get("/api/applications")
def get_apps():
    return load_data()["applications"]
