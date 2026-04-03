def generate_user_response(final_result, flags):
    label = final_result["final_label"]
    confidence = final_result["confidence"]

    # ---------- TITLE ----------
    if label == "Scam":
        title = "⚠️ High Risk Message Detected"
    elif label == "Suspicious":
        title = "⚠️ Suspicious Message"
    else:
        title = "✅ Safe Message"

    # ---------- REASONS ----------
    reason_map = {
        "lottery_scam": "Lottery or prize scam pattern detected",
        "loan_scam": "Unrealistic loan or financial offer",
        "job_scam": "Suspicious job or earning opportunity",
        "upi_scam": "UPI or payment request detected",
        "bank_fraud": "Possible bank-related fraud",
        "urgency": "Creates urgency to rush your decision",
        "fear": "Uses fear or threats",
        "too_good_offer": "Offer looks too good to be true",
        "kyc_scam": "KYC or identity verification scam",
        "bank_impersonation": "Pretending to be a bank",
        "upi_brand_abuse": "Misuse of payment apps like GPay/PhonePe",
        "group_scam": "WhatsApp group earning scam",
        "short_link": "Suspicious shortened link",
        "numeric_trap": "Too many numbers (possible OTP/money trap)",
        "all_caps": "Aggressive or spammy message style"
    }

    reasons = []
    for f in flags:
        if f in reason_map:
            reasons.append(f"• {reason_map[f]}")

    # limit reasons (don’t overload user)
    reasons = reasons[:3]

    # ---------- RECOMMENDATION ----------
    if label == "Scam":
        recommendation = "Do not click links or share personal information."
    elif label == "Suspicious":
        recommendation = "Proceed with caution. Verify before taking action."
    else:
        recommendation = "This message appears safe."

    # ---------- FINAL MESSAGE ----------
    response = f"{title}\n\n"

    if label != "Safe":
        response += "This message shows signs of potential fraud.\n\n"

    if reasons:
        response += "Reasons:\n" + "\n".join(reasons) + "\n\n"

    response += f"Confidence: {int(confidence * 100)}%\n\n"
    response += f"Recommendation:\n{recommendation}"

    return response