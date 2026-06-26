import json
import re
from datetime import datetime
import google.generativeai as genai


def analyze_root_cause(watson_report, sherlock_report, location):
    """Inspector: Generates full investigation report with root cause."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    case_id = f"ISS-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    prompt = f"""You are the Inspector, a senior AI agent who writes official civic investigation reports.
Return ONLY a valid JSON object — no extra text, no markdown fences.

WATSON IMAGE ANALYSIS:
{json.dumps(watson_report, indent=2)}

SHERLOCK PATTERN ANALYSIS:
{json.dumps(sherlock_report, indent=2)}

LOCATION: {location}
DATE: {datetime.now().strftime("%d %B %Y")}
CASE ID: {case_id}

JSON format:
{{
  "case_id": "{case_id}",
  "headline": "<dramatic one-line case title>",
  "root_cause": "<primary root cause>",
  "contributing_factors": ["<factor1>", "<factor2>", "<factor3>"],
  "infrastructure_health_score": <0-100>,
  "urgency_level": "immediate|high|medium|low",
  "estimated_resolution_time": "<X days/weeks>",
  "recommended_department": "<which municipal dept>",
  "action_plan": [
    {{"step": 1, "action": "<action>", "timeline": "<within X hours/days>"}},
    {{"step": 2, "action": "<action>", "timeline": "<timeline>"}},
    {{"step": 3, "action": "<action>", "timeline": "<timeline>"}}
  ],
  "prevention_recommendations": ["<rec1>", "<rec2>"],
  "investigation_summary": "<2-3 sentence formal summary>",
  "inspector_verdict": "<official verdict>"
}}"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"```json\s*|\s*```", "", text).strip()
        result = json.loads(text)
        result["case_id"] = case_id
        return result
    except Exception as e:
        return {
            "case_id": case_id,
            "headline": "Community Issue Under Investigation",
            "root_cause": "Under investigation",
            "contributing_factors": [],
            "infrastructure_health_score": 50,
            "urgency_level": "medium",
            "estimated_resolution_time": "7 days",
            "recommended_department": "Municipal Corporation",
            "action_plan": [{"step": 1, "action": "Inspect site", "timeline": "within 48 hours"}],
            "prevention_recommendations": ["Regular inspection"],
            "investigation_summary": "Case opened and under review.",
            "inspector_verdict": "Awaiting full analysis"
        }