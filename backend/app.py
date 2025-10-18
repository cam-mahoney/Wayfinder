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