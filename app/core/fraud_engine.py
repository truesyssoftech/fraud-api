# app/core/fraud_engine.py

ML_WEIGHT = 0.4
RULE_WEIGHT = 0.3
LLM_WEIGHT = 0.3


def rule_score(flags):
    score = 0

    weights = {
        "urgency": 0.3,
        "congratulations": 0.25,
        "lottery": 0.4,
        "free_money": 0.4,
        "short_link": 0.35,
        "unknown_sender": 0.3,
        "normal_domain": -0.1
    }

    for f in flags:
        score += weights.get(f, 0)

    return max(0, min(score, 1))


def llm_score(llm_output):
    if not llm_output or llm_output.get("status") != "success":
        return 0.5  # fallback neutral

    try:
        return llm_output["data"]["risk_score"] / 10
    except:
        return 0.5


def final_decision(score):
    if score >= 0.75:
        return "Scam"
    elif score >= 0.45:
        return "Suspicious"
    else:
        return "Safe"


def fraud_engine(ml_conf, flags, llm_output):
    ml = ml_conf
    rule = rule_score(flags)
    llm = llm_score(llm_output)

    final_score = (
        ml * ML_WEIGHT +
        rule * RULE_WEIGHT +
        llm * LLM_WEIGHT
    )

    decision = final_decision(final_score)

    return {
        "final_label": decision,
        "confidence": round(final_score, 2),
        "breakdown": {
            "ml": round(ml, 2),
            "rule": round(rule, 2),
            "llm": round(llm, 2)
        }
    }