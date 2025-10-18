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

USERS = {}


# ----------------------------
# Helper functions
# ----------------------------





# ----------------------------
# Routes
# ----------------------------





if __name__ == "__main__":
    app.run(port=5000, debug=True)