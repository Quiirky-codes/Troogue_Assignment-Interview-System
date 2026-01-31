from flask import Flask, jsonify
import os
from dotenv import load_dotenv

from .models import create_tables, SessionLocal, InterviewQuestion
from .routes import bp

load_dotenv()

app = Flask(__name__)
app.register_blueprint(bp)

# initialize DB tables
create_tables()

# seed questions only once
def seed_questions():
    db = SessionLocal()
    existing = db.query(InterviewQuestion).count()
    if existing == 0:
        qs = [
            InterviewQuestion(skill="python",
                text="Explain list comprehensions and give an example.",
                expected_keywords="list comprehension,for,in"),
            InterviewQuestion(skill="python",
                text="What are decorators and when do you use them?",
                expected_keywords="decorator,function,wrap"),
            InterviewQuestion(skill="ml",
                text="What is overfitting and how to prevent it?",
                expected_keywords="overfitting,regularization,validation"),
            InterviewQuestion(skill="sql",
                text="Explain INNER JOIN vs LEFT JOIN.",
                expected_keywords="inner join,left join,rows"),
        ]
        db.add_all(qs)
        db.commit()
    db.close()

seed_questions()

@app.get("/")
def home():
    return jsonify({"status": "ok", "service": "flask_interview_service"})

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5001"))
    app.run(host=host, port=port, debug=True)
