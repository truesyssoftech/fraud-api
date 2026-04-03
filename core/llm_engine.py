from openai import OpenAI
from app.config import OPENAI_API_KEY

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

def llm_analysis(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": text}
        ]
    )

    return response.choices[0].message.content