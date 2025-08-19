from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)

# Initialize Firebase
if not firebase_admin._apps:
    cred_path = os.environ.get("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/get_ip", methods=["GET"])
def get_ip():
    # Get user IP from request
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "unknown")

    # Save to Firestore
    doc_ref = db.collection("user_ips").document()
    doc_ref.set({
        "ip": user_ip,
        "user_agent": user_agent
    })

    # Send IP back to client
    return jsonify({"ip": user_ip, "user_agent": user_agent})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
