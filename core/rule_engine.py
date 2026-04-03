import re

def rule_engine(text):
    score = 0
    flags = []

    patterns = [
        "congratulations", "winner", "loan", "urgent",
        "click", "offer", "free", "limited", "reward"
    ]

    for p in patterns:
        if p in text.lower():
            score += 1
            flags.append(p)

    if "hour" in text.lower():
        score += 1
        flags.append("urgency")

    urls = re.findall(r'(https?://\S+)', text)

    return score, flags, urls