from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from uuid import uuid4
import json, os



app = Flask(__name__)
CORS(app)


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
#   "slider_responses": { key: int },
#   "swipes": { org_id: "yes"|"no" },
#   "liked_orgs": [org_id, ...],
#   "disliked_orgs": [org_id, ...]
# }
"""
USERS = {}

def new_user(first_name:str, last_name:str):
    uid = str(uuid4())
    
    user = {
        "user_id": uid,
        "first_name": first_name,
        "last_name": last_name, 
        "slider_responses": {},
        "swipes": {},
        "good_orgs": [],
        "bad_orgs": []
    }
    
    USERS[uid] = user
    return user 


# ----------------------------
# Helper functions 
# ----------------------------

def convert_to_int(i, default=0):
    try:
        return(int(float(i))) # float in case is a string like "7.5"
    except Exception:
        return int(default)

# (for the all organizations page)



# ----------------------------
# Basic Routes
# ----------------------------
@app.get("/api/health")
def health():
    return {"status":"ok"}, 200

# route for registering a new user 
@app.post("/api/register")
def register():
    request_body = request.get_json(silent=True) or {} # in case empty. converts to python dictionarys
    user = new_user(request_body.get("first_name"), request_body.get("last_name")) # register new user
    
    return jsonify({"user_id": user["user_id"], 
                    "profile": {
                        "user_id": user["user_id"],
                        "first_name": user["first_name"],
                        "last_name": user["last_name"]
                    }})
    
# route for updating a user profile (updates the questionaire answers from the user)
@app.patch("/api/user")
def update_user():
    """
        Body:
    {
      "user_id": "...",
      "responses": {            # required; any subset is fine
        "question_1": 7,
        "question_2": 150,
        "question_3": 8
      },
      "replace": false          # optional; if true, replace all answers
    }
    """
    request_body = request.get_json(silent=True) or {}
    
    user_id = request_body.get("user_id")
    
    if not user_id or user_id not in USERS: # error handling
        abort(404, "Unknown user id") 
        
    user_info = USERS[user_id]
    
    # ensure the user responses are integers 
    cleaned_responses = {}
    
    for question, response in request_body["responses"]:
        cleaned_responses[question] = convert_to_int(response)
    user_info["slider_responses"]  = cleaned_responses
    
    return jsonify({"ok": True, "slider_responses": cleaned_responses})
        


# ----------------------------
# Questionaire Routes
# ----------------------------


# ----------------------------
# Swiping Routes
# ----------------------------




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)