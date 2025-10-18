from flask import Flask, jsonify
from flask_cors import CORS
import json, os 
from uuid import uuid4


app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():
    return {"status":"ok"}, 200

# ----------------------------
# Load  JSON datasets
# ----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # absolute path of the current script
DATA_DIR = os.path.join(BASE_DIR, "data")
ORGS_DIR = os.path.join(DATA_DIR, "orgs.json") # path to the organization data
PROMPTS_DIR = os.path.join(DATA_DIR, "prompts.json") # path to the prompt data

with open(ORGS_DIR, "r", encoding="utf-8") as file:
    ORGS = json.load(file) # convert JSON file to dictionary object
    
with open(PROMPTS_DIR, "r", encoding="utf-8") as file:
    PROMPTS = json.load(file) # convert JSON file to dictionary object

"""
EG:
ORG_INDEX = {
    "org_001": {"id": "org_001", "name": "HackUT"},
    "org_002": {"id": "org_002", "name": "Texas Rocket Club"},
    "org_003": {"id": "org_003", "name": "Bevo Data Builders"}
"""
ORG_INDEX = {}

for o in ORGS:
    ORG_INDEX[o["id"]] = o


# ----------------------------
# In-memory user storage
# ----------------------------
"""
# USERS[user_id] = {
#   "user_id": str,
#   "first_name": str,
#   "last_name": str,   
#   "slider_responses": {question: int},
# }
"""
USERS = {}

def new_user(first_name:str, last_name:str):
    uid = str(uuid4())
    
    user = {
        "user_id": uid,
        "first_name": first_name,
        "last_name": last_name, 
        "slider_responses": {} 
    }
    
    USERS[uid] = user
    return user 


# ----------------------------
# Helper functions
# ----------------------------





# ----------------------------
# Routes
# ----------------------------







if __name__ == "__main__":
    app.run(port=5000, debug=True)