import os
import json
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT = """
You are an AI fraud detection system specialized in Indian scam messages.

Analyze the message and classify it strictly into ONE category:
- Scam
- Marketing
- Safe

Return ONLY valid JSON (no text outside JSON):

{
  "category": "Scam OR Marketing OR Safe",
  "risk_score": number between 1 to 10,
  "reason": "short explanation"
}
"""


def llm_analysis(text: str):
    # ---------- NO API KEY ----------
    if client is None:
        return {
            "status": "skipped",
            "data": {
                "category": "Unknown",
                "risk_score": 5,
                "reason": "LLM not configured"
            }
        }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # ---------- PARSE JSON ----------
        try:
            parsed = json.loads(content)

            # ---------- VALIDATION ----------
            category = parsed.get("category", "Unknown")
            risk_score = parsed.get("risk_score", 5)
            reason = parsed.get("reason", "No reason provided")

            # Fix invalid category
            if category not in ["Scam", "Marketing", "Safe"]:
                category = "Unknown"

            # Clamp risk_score
            try:
                risk_score = float(risk_score)
                risk_score = max(1, min(risk_score, 10))
            except:
                risk_score = 5

            return {
                "status": "success",
                "data": {
                    "category": category,
                    "risk_score": risk_score,
                    "reason": reason
                }
            }

        except json.JSONDecodeError:
            return {
                "status": "invalid_json",
                "data": {
                    "category": "Unknown",
                    "risk_score": 5,
                    "reason": content
                }
            }

    except Exception as e:
        return {
            "status": "failed",
            "data": {
                "category": "Unknown",
                "risk_score": 5,
                "reason": str(e)
            }
        }