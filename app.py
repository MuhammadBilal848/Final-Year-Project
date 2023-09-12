from flask import Flask, redirect, url_for, render_template, request, jsonify
import requests
import json
from questions import gpt_qs
from response_read import (
    generated_qs,
    speak_qs,
    correct_or_not,
    clear_text_file,
    sophisticated_response,
    get_answer_from_gpt,
)
from qdrant.qdrant_module import upload_embd_get_similarity
from flask_cors import CORS  # Import the CORS class
import time
import random
from db.db import db
from db.models.user import User
from peewee import IntegrityError, DataError
from db.models.evaluation import Evaluation
import datetime

app = Flask(__name__)
CORS(app)

app.config.from_pyfile("db/config.py")
db.connect()

# // Uncomment these lines ---> agar tables nh bni huin (also create database manually in MySQL client that you use)
# db.create_tables([Evaluation], safe=True)
# db.create_tables([User], safe=True)


@app.route("/api/users", methods=["POST"])
def createUser():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")

        if not username or not email:
            return jsonify({"error": "Username and email are required"}), 400

        if (
            User.select()
            .where((User.username == username) | (User.email == email))
            .exists()
        ):
            return (
                jsonify(
                    {"error": "User with the same username or email already exists"}
                ),
                409,
            )

        user = User.create(username=username, email=email)

        return (
            jsonify({"message": "User created successfully", "user": user.to_dict()}),
            201,
        )

    except (IntegrityError, DataError) as e:
        return (
            jsonify(
                {"error": "Failed to create user. Invalid data or database error."}
            ),
            500,
        )


@app.route("/api/users", methods=["GET"])
def getUsers():
    users = User.select()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app.route("/api/get-one/users", methods=["POST"])
def getUserByEmail():
    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "Email is required"}), 400

        user = User.select().where(User.email == email).first()

        if user:
            user_data = {
                "message": "User get successfully",
                "user": {"id": user.id, "username": user.username, "email": user.email},
            }
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return (
            jsonify({"error": "Failed to retrieve user. Internal server error."}),
            500,
        )


@app.route("/api/user/evaluations", methods=["GET"])
def getEvaluationsByUser():
    try:
        user_id = int(request.args.get("user_id"))

        if user_id is None:
            return jsonify(error="Missing 'user_id' in query parameters"), 400

        evaluations = (
            Evaluation.select()
            .where(Evaluation.user_id == user_id)
            .order_by(Evaluation.evaluation_date.desc())
        )  # Optional: Sort by evaluation date in descending order

        evaluation_list = [evaluation.to_dict() for evaluation in evaluations]

        return jsonify(evaluation_list)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/api/reset", methods=["GET"])
def reset():
    return "Reset Successfull", 200


@app.route("/api/submit-details", methods=["POST", "GET"])
def submitDetails():
    if request.method == "POST":
        try:
            clear_text_file("questions.txt")
            data = request.get_json()

            required_fields = [
                "name",
                "email",
                "phone_number",
                "father_name",
                "age",
                "university",
                "position_applied_for",
                "prior_experience",
                "skill_and_experience",
            ]
            for field in required_fields:
                if field not in data:
                    return jsonify(error=f"{field} is missing in the payload"), 400

            name = data["name"]
            email = data["email"]
            phone_number = data["phone_number"]
            father_name = data["father_name"]
            age = int(data["age"])
            university = data["university"]
            position_applied_for = data["position_applied_for"]
            prior_experience = int(data["prior_experience"])
            skills = data["skill_and_experience"]

            if not isinstance(skills, list) or not all(
                isinstance(skill, dict) and "skill" in skill and "experience" in skill
                for skill in skills
            ):
                return (
                    jsonify(
                        error="Invalid skill_and_experience format. It should be an array of objects with 'skill' and 'experience' keys"
                    ),
                    400,
                )

            response_data = {
                "name": name,
                "email": email,
                "phone_number": phone_number,
                "father_name": father_name,
                "age": age,
                "university": university,
                "position_applied_for": position_applied_for,
                "prior_experience": prior_experience,
                "skill_and_experience": skills,
            }

            final_dic = {"user_details": response_data}


            gpt_qs(skills,position_applied_for)


            question_list = generated_qs()
            final_dic["questions"] = question_list

            return jsonify(final_dic)
        except Exception as e:
            return jsonify(error=str(e)), 400
    else:
        return "This route only accepts POST requests."


@app.route('/api/evaluate-answers', methods=['POST'])
def evaluateAnswers():
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify(error="Invalid JSON data, expected a list"), 400
        evaluation_responses = []

        user_id = request.args.get("user_id")

        if user_id is None:
            return jsonify(error="Missing 'user_id' in query parameters"), 400

        evaluation_date = datetime.date.today().strftime("%Y-%m-%d")

        for question_data in data:
            question = question_data.get("question")
            answer = question_data.get("user_answer")
            if question and answer:
                evaluation_responses.append(
                    upload_embd_get_similarity(
                        answer, get_answer_from_gpt(question).replace("\n", "")
                    )
                    * 100
                )
            else:
                evaluation_responses.append({"error": "Missing question or answer"})
        sop_res = sophisticated_response(evaluation_responses)

        evaluation_id = Evaluation.create(
            user_id=user_id,
            evaluation=sop_res["evaluation"],
            evaluation_message=sop_res["evaluation_message"],
            evaluation_date=evaluation_date,
        )

        sop_res["user_id"] = str(user_id)
        sop_res["evaluation_id"] = str(evaluation_id)
        sop_res["evaluation_date"] = str(evaluation_date)

        return jsonify(sop_res)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/api/job-listings", methods=["GET"])
def getJobListings():
    try:
        headers = {
            "Authorization": "Token 8d3ad9286fc3a3bc5d2528cef807c96be2a8ffb6",
            "Content-Type": "application/json",
        }

        search = request.args.get("search")

        if search:
            external_api_url = (
                f"https://findwork.dev/api/jobs?search={search}&sort_by=relevance"
            )
        else:
            external_api_url = f"https://findwork.dev/api/jobs"

        response = requests.get(external_api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data), 200
        else:
            return jsonify({"error": "Failed to fetch data"}), response.status_code
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)
