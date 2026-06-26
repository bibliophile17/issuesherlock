import os
import uuid
import json
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

from agents.watson import analyze_image
from agents.sherlock import detect_patterns
from agents.inspector import analyze_root_cause
from agents.herald import decide_escalation

load_dotenv()

app = Flask(__name__)

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Firebase safely
db = None
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    cred_path = os.getenv("FIREBASE_CREDENTIALS", "firebase-key.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase connected")
    else:
        print("⚠️ Firebase key not found — running without database")
except Exception as e:
    print(f"⚠️ Firebase error: {e} — running without database")

# In-memory fallback when no Firebase
in_memory_issues = []


def save_issue(case_data):
    if db:
        try:
            db.collection("issues").document(case_data["case_id"]).set(case_data)
            return True
        except Exception as e:
            print(f"Firebase save error: {e}")
    in_memory_issues.append(case_data)
    return True


def get_all_issues():
    if db:
        try:
            return [doc.to_dict() for doc in db.collection("issues").stream()]
        except Exception as e:
            print(f"Firebase read error: {e}")
    return in_memory_issues


def get_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,rain&daily=precipitation_sum&past_days=7&forecast_days=1"
        r = requests.get(url, timeout=5)
        data = r.json()
        return {
            "temperature": data["current"]["temperature_2m"],
            "current_rain": data["current"]["rain"],
            "past_7_days_rain": data["daily"]["precipitation_sum"]
        }
    except:
        return {"temperature": "unknown", "current_rain": 0, "past_7_days_rain": []}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/case/<case_id>")
def case_detail(case_id):
    return render_template("case.html", case_id=case_id)


@app.route("/api/report", methods=["POST"])
def submit_report():
    description = request.form.get("description", "")
    location    = request.form.get("location", "Unknown Location")
    lat         = float(request.form.get("lat", 20.5937))
    lon         = float(request.form.get("lon", 78.9629))
    reporter    = request.form.get("name", "Anonymous Citizen")

    image_path = None
    image_file = request.files.get("image")
    if image_file and image_file.filename:
        image_path = f"/tmp/{uuid.uuid4().hex}.jpg"
        image_file.save(image_path)

    past_issues = get_all_issues()
    weather     = get_weather(lat, lon)

    print("🔬 Watson analyzing...")
    watson = analyze_image(image_path, description, location)

    print("🕵️ Sherlock detecting patterns...")
    sherlock = detect_patterns(watson, past_issues, weather)

    print("📋 Inspector building case...")
    inspector = analyze_root_cause(watson, sherlock, location)

    print("📣 Herald deciding escalation...")
    herald = decide_escalation(inspector, days_unresolved=0)

    case_id = inspector.get("case_id", f"ISS-{uuid.uuid4().hex[:8].upper()}")

    case_data = {
        "case_id":        case_id,
        "reporter":       reporter,
        "description":    description,
        "location":       location,
        "lat":            lat,
        "lon":            lon,
        "date":           datetime.now().isoformat(),
        "resolved":       False,
        "days_unresolved": 0,
        "issue_type":     watson.get("issue_type", "unknown"),
        "severity":       watson.get("severity", "medium"),
        "severity_score": watson.get("severity_score", 5),
        "headline":       inspector.get("headline", "Community Issue Reported"),
        "urgency_level":  inspector.get("urgency_level", "medium"),
        "watson":         watson,
        "sherlock":       sherlock,
        "inspector":      inspector,
        "herald":         herald,
    }

    save_issue(case_data)
    return jsonify({"success": True, "case": case_data})


@app.route("/api/issues")
def get_issues():
    return jsonify(get_all_issues())


@app.route("/api/issue/<case_id>")
def get_issue(case_id):
    for issue in get_all_issues():
        if issue.get("case_id") == case_id:
            return jsonify(issue)
    return jsonify({"error": "Case not found"}), 404


@app.route("/api/stats")
def get_stats():
    issues   = get_all_issues()
    total    = len(issues)
    resolved = sum(1 for i in issues if i.get("resolved"))
    critical = sum(1 for i in issues if i.get("severity") == "critical")
    hotspots = sum(1 for i in issues if i.get("sherlock", {}).get("hotspot"))
    return jsonify({
        "total":           total,
        "resolved":        resolved,
        "pending":         total - resolved,
        "critical":        critical,
        "hotspots":        hotspots,
        "resolution_rate": round((resolved / total * 100) if total > 0 else 0, 1)
    })


@app.route("/api/resolve/<case_id>", methods=["POST"])
def resolve_issue(case_id):
    if db:
        try:
            db.collection("issues").document(case_id).update({"resolved": True})
            return jsonify({"success": True})
        except:
            pass
    for issue in in_memory_issues:
        if issue.get("case_id") == case_id:
            issue["resolved"] = True
    return jsonify({"success": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)