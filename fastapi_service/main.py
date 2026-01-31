# fastapi_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import SessionLocal, InterviewAnswer, InterviewQuestion, InterviewResult, Interview
from typing import Optional
from datetime import datetime
import json

app = FastAPI(title="Evaluator Service")

# Simple scoring heuristic:
# - If expected_keywords exists, score = fraction of keywords present * 70
# - Plus a length bonus (answer length normalized) up to 30 points
# final score in [0,100]

def score_answer_text(answer_text: str, expected_keywords: Optional[str]):
    if not answer_text:
        return 0.0, "Empty answer"
    score = 0.0
    notes = []
    # keyword match
    if expected_keywords:
        expected = [k.strip().lower() for k in expected_keywords.split(",") if k.strip()]
        matched = 0
        ans_lower = answer_text.lower()
        for k in expected:
            if k and k in ans_lower:
                matched += 1
        if expected:
            kw_score = (matched / len(expected)) * 70.0
            notes.append(f"{matched}/{len(expected)} keywords matched")
        else:
            kw_score = 0.0
    else:
        kw_score = 0.0

    # length bonus: normalize to 0..30 (answers > 200 chars get full)
    length = len(answer_text)
    length_bonus = min(30.0, (length / 200.0) * 30.0)
    score = kw_score + length_bonus
    notes.append(f"length_bonus={round(length_bonus,2)}")
    return round(score,2), "; ".join(notes)

@app.post("/evaluate/answer")
def evaluate_answer(answer_id: int):
    db = SessionLocal()
    ans = db.query(InterviewAnswer).filter(InterviewAnswer.id==answer_id).first()
    if not ans:
        db.close()
        raise HTTPException(status_code=404, detail="Answer not found")
    # fetch question expected_keywords
    q = db.query(InterviewQuestion).filter(InterviewQuestion.id==ans.question_id).first()
    expected_keywords = q.expected_keywords if q else None
    score, notes = score_answer_text(ans.answer_text or "", expected_keywords)
    ans.score = score
    ans.scored = True
    ans.evaluator_notes = notes
    db.add(ans)
    db.commit()
    db.refresh(ans)
    db.close()
    return {"answer_id": ans.id, "score": ans.score, "notes": notes}

@app.post("/evaluate/interview/{interview_id}")
def evaluate_interview(interview_id: int):
    db = SessionLocal()
    interview = db.query(Interview).filter(Interview.id==interview_id).first()
    if not interview:
        db.close()
        raise HTTPException(status_code=404, detail="Interview not found")
    answers = db.query(InterviewAnswer).filter(InterviewAnswer.interview_id==interview_id).all()
    if not answers:
        db.close()
        raise HTTPException(status_code=400, detail="No answers submitted for this interview")

    per_answer_results = []
    total = 0.0
    for a in answers:
        # fetch question to get expected keywords
        q = db.query(InterviewQuestion).filter(InterviewQuestion.id==a.question_id).first()
        expected = q.expected_keywords if q else None
        score, notes = score_answer_text(a.answer_text or "", expected)
        a.score = score
        a.scored = True
        a.evaluator_notes = notes
        total += score
        per_answer_results.append({"answer_id": a.id, "question_id": a.question_id, "score": score, "notes": notes})
        db.add(a)
    # average score across answers, normalise to 100 (max per question we gave 100)
    avg_score = round(total / max(len(answers),1), 2)
    # simple verdict rules
    if avg_score >= 75:
        verdict = "pass"
    elif avg_score >= 50:
        verdict = "consider"
    else:
        verdict = "fail"
    details = json.dumps(per_answer_results)
    # write interview_results (update if exists)
    existing = db.query(InterviewResult).filter(InterviewResult.interview_id==interview_id).first()
    if existing:
        existing.total_score = avg_score
        existing.verdict = verdict
        existing.details = details
        existing.created_at = datetime.utcnow()
        db.add(existing)
    else:
        res = InterviewResult(
            interview_id=interview_id,
            total_score=avg_score,
            verdict=verdict,
            details=details,
            created_at=datetime.utcnow()
        )
        db.add(res)
    # mark interview status to done
    interview.status = "done"
    db.add(interview)
    db.commit()
    # read the final result to return
    result = db.query(InterviewResult).filter(InterviewResult.interview_id==interview_id).first()
    db.close()
    return {"interview_id": interview_id, "total_score": result.total_score, "verdict": result.verdict, "details": json.loads(result.details)}

@app.get("/results/{interview_id}")
def get_results(interview_id: int):
    db = SessionLocal()
    res = db.query(InterviewResult).filter(InterviewResult.interview_id==interview_id).first()
    db.close()
    if not res:
        raise HTTPException(status_code=404, detail="Result not found")
    import json
    try:
        details = json.loads(res.details)
    except:
        details = res.details
    return {"interview_id": res.interview_id, "total_score": res.total_score, "verdict": res.verdict, "details": details, "created_at": res.created_at.isoformat()}
