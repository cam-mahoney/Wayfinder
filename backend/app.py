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
#   "good_orgs": [org_id, ...],
#   "bad_orgs": [org_id, ...]
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
@app.get("/health")
def health():
    return {"status":"ok"}, 200

# route for registering a new user 
@app.post("/register")
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
@app.patch("/user")
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
        abort(404, description="Unknown user id") 
        
    user_info = USERS[user_id]
    
    # ensure the user responses are integers 
    cleaned_responses = {}
    responses = request_body.get("responses") or {}
    
    for question, response in responses.items():
        cleaned_responses[question] = convert_to_int(response)
    user_info["slider_responses"]  = cleaned_responses
    
    return jsonify({"ok": True, "slider_responses": cleaned_responses})

@app.get("/user")
def get_user():
    user_id = request.args.get("user_id") # parses everything after the ? 
    if not user_id or user_id not in USERS: # error handling
        abort(404, description="Unknown user id") 
    user_info = USERS[user_id]
    
        
    return jsonify({
        "user_id": user_info["user_id"],
        "first_name": user_info["first_name"],
        "last_name": user_info["last_name"],
        "slider_responses": user_info.get("slider_responses", {}),
        "swipes": user_info.get("swipes", {}),
        "good_orgs": user_info.get("good_orgs", []),
        "bad_orgs": user_info.get("bad_orgs", [])
    })
    
    
        
# ----------------------------
# Questionaire Routes
# ----------------------------
@app.get("/prompts")
def get_prompts():
    return jsonify({"prompts": PROMPTS})

# save user preferences after questionaire submission
@app.post("/questionnaire/submit")
def submit_questionnaire():
    request_body = request.get_json(silent=True) or {}
    user_id = request_body.get("user_id")
    if not user_id or user_id not in USERS: # error handling
        abort(404, description="Unknown user id")
    
    user_info = USERS[user_id]
    
    # ensure the user responses are integers 
    cleaned_responses = {}
    responses = request_body.get("responses") or {}
    
    for question, response in responses.items():
        cleaned_responses[question] = convert_to_int(response)
    user_info["slider_responses"]  = cleaned_responses
    
    return jsonify({"ok": True, "slider_responses": cleaned_responses})


# ----------------------------
# Swiping logic
# ----------------------------
def _base_deck(user: dict, orgs: list[dict], limit:int=20) -> list:
    """
    Build a deck of organizations to swipe using recommender.model(user, k):
    Returns a list of organizations
    """
    from recommender import model as recommend_model
    
    user_id = user["user_id"]
    preferred_organizations = recommend_model(user_id, limit)
    
    id_to_org = {}
    
    for org in orgs:
        id_to_org[org["id"]] = org
        
    deck = []
    for org_id in preferred_organizations:
        deck.append(id_to_org[org_id])
            
    return deck 

@app.get("/swipe/deck")
def swipe_deck():
    user_id = request.args.get("user_id") # parses everything after the ? 
    if not user_id or user_id not in USERS: # error handling
        abort(404, description="Unknown user id")
    
    limit = 15
    
    user_info = USERS[user_id]
    orgs_deck = _base_deck(user_info, ORGS, limit)
    
    return jsonify({"deck": orgs_deck})

@app.post('/swipe')
def swipe_action():
    """
    Record a swipe on an organization card.
    Body:
      {
        "user_id": "...",
        "org_id": "...",
        "decision": "yes" | "no"
      }
    Updates:
      - USERS[user_id]["swipes"][org_id] = decision
      - good_orgs
      - bad_orgs 
    """
    request_body = request.get_json(silent=True) or {}
    user_id = request_body.get("user_id")
    org_id = request_body.get("org_id")
    decision = request_body.get("decision")
    
    if not user_id or user_id not in USERS: # error handling
        abort(404, description="Unknown user id")
    if not org_id or org_id not in ORG_INDEX: # error handling
        abort(404, description="Unknown organization id")
    if decision not in ("yes", "no"):
        abort(400, description="Decision must be yes or no")
        
    user_info = USERS[user_id]
    user_info.setdefault("swipes", {})[org_id] = decision # record the swipe decision
    
    if decision == "yes":
        if org_id not in user_info["good_orgs"]:
            user_info["good_orgs"].append(org_id)
        if org_id in user_info["bad_orgs"]: # remember to remove from bad_orgs if previously swiped no
            user_info["bad_orgs"].remove(org_id)
    else:  # decision is "no"
        if org_id not in user_info["bad_orgs"]:
            user_info["bad_orgs"].append(org_id)
        if org_id in user_info["good_orgs"]: # remember to remove from good_orgs if previously swiped yes
            user_info["good_orgs"].remove(org_id)
    
    return jsonify({"ok": True, 
                    "swipes": user_info["swipes"], 
                    "good_orgs": user_info["good_orgs"],
                    "bad_orgs": user_info["bad_orgs"]})
            
@app.get("/swipe/info")
def swipe_info():
    """
    Return the user's swipe history info.
    Query: ?user_id=...
    Response:
      {
        "swipes": { org_id: "yes"|"no", ... },
        "good_orgs": [org_id, ...],
        "bad_orgs": [org_id, ...]
      }
    """    
    user_id = request.args.get("user_id")
    if not user_id or user_id not in USERS: # error handling
        abort(404, description="Unknown user id")
        
    user_info = USERS[user_id]
    
    return jsonify({"swipes": user_info.get("swipes",{}),
                    "good_orgs": user_info.get("good_orgs", []),
                    "bad_orgs": user_info.get("bad_orgs", [])})





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)