import re

def rule_engine(text: str):
    text_lower = text.lower()

    flags = []
    score = 0
    urls = []

    # ---------- URL EXTRACTION ----------
    urls = re.findall(r'(https?://\S+)', text)

    # ---------- PATTERN DEFINITIONS ----------
    patterns = {
        "lottery_scam": {
            "keywords": ["won", "winner", "lottery", "prize", "congratulations"],
            "weight": 0.4
        },
        "loan_scam": {
            "keywords": ["instant loan", "no cibil", "low interest", "approved loan"],
            "weight": 0.35
        },
        "job_scam": {
            "keywords": ["work from home", "earn daily", "part time job", "easy income"],
            "weight": 0.35
        },
        "upi_scam": {
            "keywords": ["upi", "collect request", "request money", "scan qr"],
            "weight": 0.4
        },
        "bank_fraud": {
            "keywords": ["account blocked", "verify kyc", "update pan", "bank alert"],
            "weight": 0.45
        },
        "urgency": {
            "keywords": ["urgent", "immediately", "act now", "limited time"],
            "weight": 0.3
        },
        "fear": {
            "keywords": ["blocked", "suspended", "legal action", "penalty"],
            "weight": 0.35
        },
        "too_good_offer": {
            "keywords": ["free money", "guaranteed return", "double your money"],
            "weight": 0.45
        }
    }

    # ---------- DETECTION ----------
    for key, pattern in patterns.items():
        for kw in pattern["keywords"]:
            if kw in text_lower:
                flags.append(key)
                score += pattern["weight"]
                break

    # ---------- INDIAN-SPECIFIC RULES (ADD HERE) ----------
    if any(x in text_lower for x in ["aadhaar", "pan card", "kyc update"]):
        flags.append("kyc_scam")
        score += 0.4

    if any(x in text_lower for x in ["sbi", "hdfc", "icici", "axis bank"]):
        flags.append("bank_impersonation")
        score += 0.35

    if any(x in text_lower for x in ["paytm", "phonepe", "gpay"]):
        flags.append("upi_brand_abuse")
        score += 0.3

    if "whatsapp group" in text_lower and "earn" in text_lower:
        flags.append("group_scam")
        score += 0.35
    # ---------- SPECIAL RULES ----------

    # Short suspicious link
    if any(domain in text_lower for domain in ["bit.ly", "tinyurl", "shorturl"]):
        flags.append("short_link")
        score += 0.35

    # Too many numbers (OTP / money bait)
    if len(re.findall(r'\d+', text)) > 3:
        flags.append("numeric_trap")
        score += 0.2

    # ALL CAPS (aggressive spam)
    if text.isupper():
        flags.append("all_caps")
        score += 0.2

    # ---------- NORMALIZE ----------
    score = max(0, min(score, 1))

    return score, list(set(flags)), urls