import json
import re
import google.generativeai as genai
import PIL.Image


def analyze_image(image_path, description, location):
    """Watson: Analyzes photo and identifies the civic issue."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""You are Watson, an AI image analysis agent for civic issue detection.
Analyze the image (if provided) and the description below.
Return ONLY a valid JSON object — no extra text, no markdown fences.

Description: {description}
Location: {location}

JSON format:
{{
  "issue_type": "pothole|waterlogging|streetlight|garbage|drainage|graffiti|road_damage|other",
  "severity": "critical|high|medium|low",
  "severity_score": <1-10>,
  "confidence": <0.0-1.0>,
  "visible_damage": "<what you see>",
  "estimated_area": "small|medium|large",
  "immediate_risk": <true|false>,
  "risk_reason": "<why or why not immediate risk>",
  "recommended_action": "<what should be done>",
  "watson_notes": "<detailed observations>"
}}"""

    try:
        if image_path:
            image = PIL.Image.open(image_path)
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(prompt)

        text = response.text.strip()
        text = re.sub(r"```json\s*|\s*```", "", text).strip()
        return json.loads(text)

    except Exception as e:
        return {
            "issue_type": "unknown",
            "severity": "medium",
            "severity_score": 5,
            "confidence": 0.5,
            "visible_damage": description,
            "estimated_area": "medium",
            "immediate_risk": False,
            "risk_reason": "Could not analyze image",
            "recommended_action": "Manual inspection required",
            "watson_notes": f"Analysis note: {str(e)}"
        }