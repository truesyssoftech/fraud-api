from fastapi import APIRouter
from app.schemas.request import MessageRequest
from app.core.rule_engine import rule_engine
from app.core.domain_checker import check_domain
from app.core.ml_engine import ml_predict
from app.core.llm_engine import llm_analysis
from app.core.fraud_engine import fraud_engine
from app.utils.response_generator import generate_user_response

router = APIRouter()


@router.post("/detect")
async def detect_message(req: MessageRequest):
    text = req.message

    # ---------- RULE ENGINE ----------
    rule_score, flags, urls = rule_engine(text)

    # ---------- DOMAIN CHECK ----------
    domain_score = 0
    domain_flags = []

    for url in urls:
        score, reason = check_domain(url)
        domain_score += score
        domain_flags.append(reason)

    # Combine all flags
    all_flags = flags + domain_flags

    # ---------- ML ----------
    ml_label, ml_conf = ml_predict(text)

    # ---------- LLM (OPTIONAL BUT ALWAYS SAFE) ----------
    llm_result = llm_analysis(text)

    # ---------- FINAL FRAUD ENGINE ----------
    fraud_result = fraud_engine(
        ml_conf=ml_conf,
        flags=all_flags,
        llm_output=llm_result
    )

    # ---------- FINAL RESPONSE ----------
    return {
        "final": fraud_result,
        "ml": {
            "label": ml_label,
            "confidence": ml_conf
        },
        "flags": all_flags,
        "llm": llm_result
    }

    @router.post("/detect-readable")
    async def detect_message_readable(req: MessageRequest):
    text = req.message

    # ---------- RULE ENGINE ----------
    rule_score, flags, urls = rule_engine(text)

    # ---------- DOMAIN CHECK ----------
    domain_score = 0
    domain_flags = []

    for url in urls:
        score, reason = check_domain(url)
        domain_score += score
        domain_flags.append(reason)

    all_flags = flags + domain_flags

    # ---------- ML ----------
    ml_label, ml_conf = ml_predict(text)

    # ---------- LLM ----------
    llm_result = llm_analysis(text)

    # ---------- FINAL ENGINE ----------
    fraud_result = fraud_engine(
        ml_conf=ml_conf,
        flags=all_flags,
        llm_output=llm_result
    )

    # ---------- HUMAN RESPONSE ----------
    user_message = generate_user_response(
        final_result=fraud_result,
        flags=all_flags
    )

    return {
        "message": user_message,
        "final_label": fraud_result["final_label"],
        "confidence": fraud_result["confidence"]
    }