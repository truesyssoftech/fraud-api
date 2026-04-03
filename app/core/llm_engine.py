import os
import json
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT = """
You are a fraud detection system trained on Indian scams.

Return ONLY JSON:
{
  "category": "Scam | Marketing | Safe",
  "risk_score": 1-10,
  "reason": "short"
}
"""

def llm_analysis(text: str):
    # ✅ Case 1: No API key
    if client is None:
        return {
            "status": "skipped",
            "reason": "LLM not configured"
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

        # ✅ Try parsing JSON safely
        try:
            parsed = json.loads(content)
            return {
                "status": "success",
                "data": parsed
            }
        except json.JSONDecodeError:
            return {
                "status": "invalid_json",
                "raw": content
            }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }