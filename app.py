from flask import Flask , redirect , url_for , render_template,request,jsonify
import json
from questions import gpt_qs
from response_read import generated_qs , speak_qs , correct_or_not , clear_text_file , sophisticated_response , get_answer_from_gpt
from qdrant.qdrant_module import upload_embd_get_similarity
from flask_cors import CORS  # Import the CORS class
import time
import random


app = Flask(__name__)
CORS(app)
  

@app.route('/api/reset',methods=['GET'])
def reset():
    return "Reset Successfull", 200


@app.route('/api/submit-details', methods=['POST', 'GET'])
def submitDetails():
    if request.method == 'POST':
        try:
            clear_text_file('questions.txt')
            data = request.get_json()

            required_fields = ['name', 'email', 'phone_number','father_name', 'age', 'university', 'position_applied_for','prior_experience', 'skill_and_experience']
            for field in required_fields:
                if field not in data:
                    return jsonify(error=f"{field} is missing in the payload"), 400

            name = data['name']
            email = data['email']
            phone_number = data['phone_number']
            father_name = data['father_name']
            age = int(data['age'])
            university = data['university']
            position_applied_for = data['position_applied_for']
            prior_experience = int(data['prior_experience'])
            skills = data['skill_and_experience']

            if not isinstance(skills, list) or not all(isinstance(skill, dict) and 'skill' in skill and 'experience' in skill for skill in skills):
                return jsonify(error="Invalid skill_and_experience format. It should be an array of objects with 'skill' and 'experience' keys"), 400

            response_data = {
                "name": name,
                "email": email,
                "phone_number": phone_number,
                "father_name": father_name,
                "age": age,
                "university": university,
                "position_applied_for": position_applied_for,
                "prior_experience": prior_experience,
                "skill_and_experience": skills
            }

            final_dic = {'user_details': response_data}

            for skill_experience in skills:
                gpt_qs(skill_experience['skill'], skill_experience['experience'])

            question_list = generated_qs()
            final_dic['questions'] = question_list

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

        for question_data in data:
            question = question_data.get('question')
            answer = question_data.get('user_answer')
            if question and answer:
                evaluation_responses.append(upload_embd_get_similarity(answer , get_answer_from_gpt(question).replace('\n', ''))*100)
            else:
                evaluation_responses.append({'error': 'Missing question or answer'})
        sop_res = sophisticated_response(evaluation_responses)
        return jsonify(sop_res)
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)
