import json
import re
import google.generativeai as genai


def decide_escalation(inspector_report, days_unresolved=0):
    """Herald: Decides escalation level and drafts formal complaint."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""You are Herald, an AI escalation agent ensuring civic issues get resolved.
Return ONLY a valid JSON object — no extra text, no markdown fences.

INVESTIGATION REPORT:
{json.dumps(inspector_report, indent=2)}

DAYS UNRESOLVED: {days_unresolved}

JSON format:
{{
  "should_escalate": <true|false>,
  "escalation_level": "none|ward_officer|municipal_commissioner|social_media|rti",
  "escalation_reason": "<why escalating or not>",
  "shame_score": <0-100>,
  "formal_complaint": "<full formal complaint letter text>",
  "social_media_post": "<tweet-length public post>",
  "rti_draft": "<RTI request if applicable, else empty string>",
  "pressure_tactics": ["<tactic1>", "<tactic2>"],
  "herald_message": "<message to citizen about next steps>"
}}"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"```json\s*|\s*```", "", text).strip()
        return json.loads(text)
    except Exception as e:
        return {
            "should_escalate": False,
            "escalation_level": "none",
            "escalation_reason": "Issue newly reported",
            "shame_score": 0,
            "formal_complaint": "Issue has been formally logged and is under review.",
            "social_media_post": "Reported a civic issue via IssueSherlock. Awaiting resolution.",
            "rti_draft": "",
            "pressure_tactics": ["Follow up in 7 days"],
            "herald_message": "Your issue has been logged. We will escalate if unresolved in 7 days."
        }