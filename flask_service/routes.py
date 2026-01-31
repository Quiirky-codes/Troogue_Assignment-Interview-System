from flask import Blueprint, jsonify, request
from datetime import datetime
import os
import requests

from .models import (
    SessionLocal, create_tables,
    Candidate, Interview,
    InterviewQuestion, InterviewAnswer,
    InterviewResult
)
from .utils import save_file

bp = Blueprint("api", __name__)

# CREATE CANDIDATE
@bp.route("/candidates/create", methods=["POST"])
def create_candidate():
    db = SessionLocal()

    data = request.form.to_dict() if request.form else request.json
    name = data.get("name")
    email = data.get("email")

    resume_path = None
    if "resume" in request.files:
        resume_path = save_file(request.files["resume"])

    if not name or not email:
        return jsonify({"error": "name and email required"}), 400

    cand = Candidate(name=name, email=email, resume_path=resume_path)
    db.add(cand)
    db.commit()
    db.refresh(cand)
    db.close()

    return jsonify({"id": cand.id, "name": cand.name, "email": cand.email})


# CREATE INTERVIEW
@bp.route("/interviews/create", methods=["POST"])
def create_interview():
    db = SessionLocal()
    data = request.json or request.form.to_dict()

    candidate_id = data.get("candidate_id")
    skill = data.get("skill")

    if not candidate_id or not skill:
        return jsonify({"error": "candidate_id and skill required"}), 400

    iv = Interview(candidate_id=int(candidate_id), skill=skill)
    db.add(iv)
    db.commit()
    db.refresh(iv)
    db.close()

    return jsonify({"id": iv.id, "candidate_id": iv.candidate_id, "skill": iv.skill})


# GET QUESTIONS FOR INTERVIEW
@bp.route("/interviews/<int:interview_id>/questions", methods=["GET"])
def get_questions(interview_id):
    db = SessionLocal()

    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        db.close()
        return jsonify({"error": "Interview not found"}), 404

    questions = db.query(InterviewQuestion).filter(
        InterviewQuestion.skill == interview.skill
    ).all()

    result = [{"id": q.id, "text": q.text} for q in questions]

    db.close()
    return jsonify({"interview_id": interview_id, "questions": result})


# SAVE ANSWER
@bp.route("/answers/create", methods=["POST"])
def save_answer():
    db = SessionLocal()

    if request.content_type.startswith("multipart/form-data"):
        interview_id = request.form.get("interview_id")
        question_id = request.form.get("question_id")
        answer_text = request.form.get("answer_text")
        file_path = None
        if "file" in request.files:
            file_path = save_file(request.files["file"])
    else:
        data = request.json
        interview_id = data.get("interview_id")
        question_id = data.get("question_id")
        answer_text = data.get("answer_text")
        file_path = None

    ans = InterviewAnswer(
        interview_id=interview_id,
        question_id=question_id,
        answer_text=answer_text,
        uploaded_file_path=file_path
    )

    db.add(ans)
    db.commit()
    db.refresh(ans)
    db.close()

    return jsonify({"id": ans.id})


# COMPLETE INTERVIEW & TRIGGER FASTAPI EVALUATION
@bp.route("/interviews/<int:interview_id>/complete", methods=["PUT"])
def complete_interview(interview_id):
    db = SessionLocal()
    iv = db.query(Interview).filter(Interview.id == interview_id).first()

    if not iv:
        db.close()
        return jsonify({"error": "Interview not found"}), 404

    iv.status = "completed"
    iv.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(iv)
    db.close()

    FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi:8000")

    try:
        r = requests.post(f"{FASTAPI_URL}/evaluate/interview/{interview_id}", timeout=20)
        r.raise_for_status()
    except Exception as e:
        return jsonify({"status": "completed", "evaluation": "failed", "error": str(e)}), 500

    return jsonify({"status": "completed", "evaluation": "started"})


# DASHBOARD
@bp.route("/interviews/<int:interview_id>", methods=["GET"])
def dashboard(interview_id):
    db = SessionLocal()

    iv = db.query(Interview).filter(Interview.id == interview_id).first()
    if not iv:
        return jsonify({"error": "Interview not found"}), 404

    cand = db.query(Candidate).filter(Candidate.id == iv.candidate_id).first()
    answers = db.query(InterviewAnswer).filter(
        InterviewAnswer.interview_id == interview_id
    ).all()
    result = db.query(InterviewResult).filter(
        InterviewResult.interview_id == interview_id
    ).first()

    answer_list = [{
        "answer_id": a.id,
        "question_id": a.question_id,
        "answer_text": a.answer_text,
        "file": a.uploaded_file_path,
        "score": a.score,
        "scored": a.scored
    } for a in answers]

    dashboard = {
        "interview": {
            "id": iv.id,
            "skill": iv.skill,
            "status": iv.status
        },
        "candidate": {
            "id": cand.id,
            "name": cand.name,
            "email": cand.email
        },
        "answers": answer_list,
        "result": {
            "total_score": result.total_score,
            "verdict": result.verdict,
            "details": result.details
        } if result else None
    }

    return jsonify(dashboard)
