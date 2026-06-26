import json
import re
import google.generativeai as genai


def detect_patterns(current_issue, past_issues, weather_data):
    """Sherlock: Detects patterns across historical reports."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    past_summary = [
        {
            "type":     i.get("issue_type"),
            "location": i.get("location"),
            "date":     i.get("date"),
            "severity": i.get("severity"),
            "resolved": i.get("resolved", False),
        }
        for i in past_issues[-20:]
    ]

    prompt = f"""You are Sherlock, an AI pattern detection agent for civic issues.
Return ONLY a valid JSON object — no extra text, no markdown fences.

CURRENT ISSUE:
{json.dumps(current_issue, indent=2)}

PAST REPORTS (last 20):
{json.dumps(past_summary, indent=2)}

WEATHER DATA:
{json.dumps(weather_data, indent=2)}

JSON format:
{{
  "pattern_detected": <true|false>,
  "pattern_type": "recurring|seasonal|infrastructure_failure|neglect|none",
  "recurrence_count": <number>,
  "pattern_description": "<what pattern you found>",
  "weather_correlation": "<how weather relates>",
  "connected_issues": [],
  "hotspot": <true|false>,
  "hotspot_reason": "<why this area is or isn't a hotspot>",
  "time_pattern": "morning|evening|monsoon|winter|random",
  "sherlock_deduction": "<main detective conclusion>",
  "elementary": "<one punchy Sherlock-style line>"
}}"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"```json\s*|\s*```", "", text).strip()
        return json.loads(text)
    except Exception as e:
        return {
            "pattern_detected": False,
            "pattern_type": "none",
            "recurrence_count": 0,
            "pattern_description": "Insufficient data for pattern detection",
            "weather_correlation": "Unknown",
            "connected_issues": [],
            "hotspot": False,
            "hotspot_reason": "Not enough data",
            "time_pattern": "random",
            "sherlock_deduction": "More data needed to draw conclusions.",
            "elementary": "The game is afoot, but evidence is scarce."
        }