def final_decision(text, rule_score, domain_score, ml_label, ml_conf):
    total_score = rule_score + domain_score + (ml_conf * 5)

    if total_score >= 10:
        category = "Scam"
    elif total_score >= 6:
        category = "Marketing"
    else:
        category = "Safe"

    return {
        "category": category,
        "risk_score": round(total_score, 2),
        "ml_label": ml_label,
        "ml_confidence": round(ml_conf, 2),
        "use_llm": 5 < total_score < 8
    }