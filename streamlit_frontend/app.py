import streamlit as st
import requests
import os

# ---------------------------
# Correct service URLs for Docker networking
# ---------------------------
FLASK_URL = os.getenv("FLASK_URL", "http://flask:5001")
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi:8000")

st.title("Interview System - Streamlit Frontend")

st.sidebar.header("Actions")
action = st.sidebar.selectbox("Choose Action", [
    "Create Candidate",
    "Create Interview",
    "Get Questions",
    "Submit Answer",
    "Complete Interview",
    "Get Interview Dashboard"
])


# ---------------------------------------
# Helper to display API responses safely
# ---------------------------------------
def show_response(resp):
    st.write("Status:", resp.status_code)
    try:
        st.json(resp.json())
    except:
        st.error("Non-JSON Response:")
        st.code(resp.text)


# ---------------------------------------
# Create Candidate
# ---------------------------------------
if action == "Create Candidate":
    st.subheader("Create a new candidate")

    name = st.text_input("Name")
    email = st.text_input("Email")
    resume = st.file_uploader("Upload Resume (optional)")

    if st.button("Create Candidate"):
        data = {"name": name, "email": email}
        files = {}

        if resume:
            files["resume"] = (resume.name, resume.getvalue())

        resp = requests.post(f"{FLASK_URL}/candidates/create",
                             data=data,
                             files=files if files else None)

        show_response(resp)


# ---------------------------------------
# Create Interview
# ---------------------------------------
if action == "Create Interview":
    st.subheader("Create interview")

    candidate_id = st.text_input("Candidate ID")
    skill = st.text_input("Skill")

    if st.button("Create Interview"):
        payload = {"candidate_id": candidate_id, "skill": skill}
        resp = requests.post(f"{FLASK_URL}/interviews/create", json=payload)
        show_response(resp)


# ---------------------------------------
# Get Questions
# ---------------------------------------
if action == "Get Questions":
    st.subheader("Fetch questions for interview")

    interview_id = st.text_input("Interview ID")

    if st.button("Get Questions"):
        resp = requests.get(f"{FLASK_URL}/interviews/{interview_id}/questions")
        show_response(resp)


# ---------------------------------------
# Submit Answer
# ---------------------------------------
if action == "Submit Answer":
    st.subheader("Submit answer for a question")

    interview_id = st.text_input("Interview ID")
    question_id = st.text_input("Question ID")
    answer_text = st.text_area("Answer Text")
    upload_file = st.file_uploader("Upload supporting file (optional)")

    if st.button("Submit Answer"):
        # MULTIPART FORM when a file is uploaded
        if upload_file:
            files = {"file": (upload_file.name, upload_file.getvalue())}
            data = {
                "interview_id": interview_id,
                "question_id": question_id,
                "answer_text": answer_text
            }
            resp = requests.post(f"{FLASK_URL}/answers/create",
                                 data=data,
                                 files=files)
        else:
            # JSON when no file is uploaded
            payload = {
                "interview_id": interview_id,
                "question_id": question_id,
                "answer_text": answer_text
            }
            resp = requests.post(f"{FLASK_URL}/answers/create", json=payload)

        show_response(resp)


# ---------------------------------------
# Complete Interview (trigger evaluation)
# ---------------------------------------
if action == "Complete Interview":
    st.subheader("Complete interview and trigger evaluator")

    interview_id = st.text_input("Interview ID")

    if st.button("Complete & Evaluate"):
        resp = requests.put(f"{FLASK_URL}/interviews/{interview_id}/complete")

        show_response(resp)

        st.info("Fetching evaluation results from FastAPI...")
        r = requests.get(f"{FASTAPI_URL}/results/{interview_id}")
        show_response(r)


# ---------------------------------------
# Interview Dashboard
# ---------------------------------------
if action == "Get Interview Dashboard":
    st.subheader("View full interview dashboard")

    interview_id = st.text_input("Interview ID")

    if st.button("Get Dashboard"):
        resp = requests.get(f"{FLASK_URL}/interviews/{interview_id}")
        show_response(resp)
