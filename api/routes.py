from fastapi import APIRouter
from app.schemas.request import MessageRequest
from app.core.rule_engine import rule_engine
from app.core.domain_checker import check_domain
from app.core.ml_engine import ml_predict
from app.core.llm_engine import llm_analysis
from app.core.decision_engine import final_decision

router = APIRouter()

@router.post("/detect")
async def detect_message(req: MessageRequest):
    text = req.message

    rule_score, flags, urls = rule_engine(text)

    domain_score = 0
    domain_flags = []

    for url in urls:
        score, reason = check_domain(url)
        domain_score += score
        domain_flags.append(reason)

    ml_label, ml_conf = ml_predict(text)

    result = final_decision(
        text=text,
        rule_score=rule_score,
        domain_score=domain_score,
        ml_label=ml_label,
        ml_conf=ml_conf
    )

    # LLM fallback
    if result["use_llm"]:
        result["llm"] = llm_analysis(text)

    result["flags"] = flags + domain_flags

    return result