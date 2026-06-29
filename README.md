# 🔍 IssueSherlock

### _"Elementary, my dear citizen."_

> AI-powered civic detective platform that doesn't just log community issues it **investigates** them.

Built for **Vibe2Ship Hackathon 2026** | Problem Statement: Community Hero Hyperlocal Problem Solver

---

## 🌐 Live Demo

**[https://issuesherlock-268865731349.us-central1.run.app](https://issuesherlock-268865731349.us-central1.run.app)**

---

## 🕵️ What is IssueSherlock?

Most civic reporting apps just log a complaint and forget about it. **IssueSherlock is different.**

It runs a **4-agent AI pipeline** powered by Google Gemini that:

- Analyzes your photo evidence
- Detects patterns across past reports
- Finds the root cause of the problem
- Autonomously escalates if authorities don't act

Every issue becomes a **case file**. Every area gets an **investigation**.

---

## 🤖 The 4-Agent Pipeline

```
Citizen reports issue (photo + description + location)
              ↓
   🔬 WATSON — Image Analysis Agent
   Analyzes photo using Gemini Vision
   Identifies issue type, severity, immediate risk
              ↓
   🕵️ SHERLOCK — Pattern Detection Agent
   Cross-references with past reports
   Detects recurring patterns, hotspots, weather correlation
              ↓
   📋 INSPECTOR — Root Cause Agent
   Generates full investigation report
   Identifies root cause, action plan, responsible department
              ↓
   📣 HERALD — Escalation Agent
   Decides escalation level
   Auto-generates formal complaint + social media draft
              ↓
   🗺️ CONSPIRACY BOARD
   Visual map of all cases, hotspots, patterns
```

---

## ✨ Key Features

- **🔬 Watson Agent** — Gemini Vision analyzes uploaded photos to identify issue type, severity (1–10), and immediate risk
- **🕵️ Sherlock Agent** — Detects recurring patterns, seasonal trends, and weather correlations across all historical reports
- **📋 Inspector Agent** — Generates formal investigation reports with root cause, contributing factors, and step-by-step action plan
- **📣 Herald Agent** — Autonomously decides escalation level, drafts formal complaints and RTI requests
- **🗺️ Conspiracy Board** — Interactive map with color-coded severity markers and hotspot detection
- **📊 Real-time Dashboard** — Live stats: total cases, critical issues, resolution rate, hotspots
- **📄 Auto-generated Formal Complaints** — Ready to send to municipal authorities
- **🌦️ Weather Correlation** — Links infrastructure issues to weather patterns
- **✅ Case Resolution Tracking** — Mark issues resolved, track pending cases

---

## 🛠️ Tech Stack

| Layer          | Technology                   |
| -------------- | ---------------------------- |
| AI Brain       | Gemini 1.5 Flash (Google AI) |
| Image Analysis | Gemini Vision                |
| Backend        | Python + Flask               |
| Database       | Firebase Firestore           |
| Maps           | Leaflet.js + OpenStreetMap   |
| Weather        | Open-Meteo API (free)        |
| Frontend       | HTML + CSS + Vanilla JS      |
| Deployment     | Google Cloud Run             |
| Code           | GitHub                       |

**100% free tools. Zero paid services.**

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/YOURUSERNAME/issuesherlock
cd issuesherlock

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your credentials
# Create .env file:
# GEMINI_API_KEY=your_key_here
# FIREBASE_CREDENTIALS=firebase-key.json

# Run
python app.py
```

Visit `http://localhost:8080`

---

## 📁 Project Structure

```
issuesherlock/
│
├── app.py                  # Main Flask backend + API routes
│
├── agents/
│   ├── watson.py           # Image analysis agent (Gemini Vision)
│   ├── sherlock.py         # Pattern detection agent
│   ├── inspector.py        # Root cause analysis agent
│   └── herald.py           # Escalation management agent
│
├── templates/
│   ├── index.html          # Homepage + report form + map
│   ├── dashboard.html      # Conspiracy Board dashboard
│   └── case.html           # Individual case detail page
│
├── static/css/
│   └── style.css           # Detective dark theme
│
├── Dockerfile              # Google Cloud Run deployment
├── requirements.txt        # Python dependencies
└── .env.example            # Environment variables template
```

---

## 📡 API Endpoints

| Method | Endpoint            | Description                              |
| ------ | ------------------- | ---------------------------------------- |
| GET    | `/`                 | Homepage with report form                |
| GET    | `/dashboard`        | Conspiracy Board                         |
| GET    | `/case/<id>`        | Case detail page                         |
| POST   | `/api/report`       | Submit new issue (runs 4-agent pipeline) |
| GET    | `/api/issues`       | Get all reported issues                  |
| GET    | `/api/issue/<id>`   | Get single case                          |
| GET    | `/api/stats`        | Dashboard statistics                     |
| POST   | `/api/resolve/<id>` | Mark case as resolved                    |

---

## 🌍 How to Use

1. **Go to homepage** → Fill in your name and description
2. **Click on map** → Pin the exact location of the issue
3. **Upload a photo** → Watson will analyze it with Gemini Vision
4. **Click "Open Investigation"** → Watch all 4 agents work in real time
5. **Get full case report** → Root cause, action plan, formal complaint
6. **View Conspiracy Board** → See all cases on the map with patterns

---
