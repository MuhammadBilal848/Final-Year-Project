from flask import Flask , redirect , url_for , render_template,request,jsonify
import json
from questions import gpt_qs
from response_read import generated_qs , speak_qs , get_answer , clear_text_file
import time

app = Flask(__name__)


@app.route('/')
def home():
    print(' -------------------------------->>>>>>>>>>>> inside home')
    return render_template('index.html')

# API ROUTE FOR SUBMITTING DETAILS
@app.route('/api/submit-details', methods=['POST', 'GET'])
def submitDetails():
    if request.method == 'POST':
        try:
            data = request.get_json()  # Parse JSON data from request body
            
            name = data['name']
            father_name = data['fatherName']
            age = int(data['age'])
            university = data['university']
            prior_experience = int(data['priorExperience'])
            skills = data.get('skill[]', [])  # Use a default empty list if 'skill' is missing

            response_data = {
                "name": name,
                "father_name": father_name,
                "age": age,
                "university": university,
                "prior_experience": prior_experience,
                "skill & experience": skills
            }

            final_dic = {
                'user_details': response_data
            }

            s_e = response_data['skill & experience']
            for i in s_e:
                skill, experience = i.split(',')
                gpt_qs(skill, experience)

            question_list = generated_qs()

            final_dic['questions'] = question_list

            return jsonify(final_dic)
        except Exception as e:
            return jsonify(error=str(e)), 400
    else:
        return "This route only accepts POST requests."


@app.route('/submit',methods = ['POST','GET'])
def submit():
    print('-------------------------------->>>>>>>>>>>> INSITE SUBMIT')
    if request.method == 'POST':
        try:
            data = request.get_json()  # Parse JSON data from request body
            
            name = data['name']
            father_name = data['fatherName']
            age = int(data['age'])
            university = data['university']
            prior_experience = int(data['priorExperience'])
            skills = data.get('skill[]', [])  # Use a default empty list if 'skill' is missing

            response_data = {
                "name": name,
                "father_name": father_name,
                "age": age,
                "university": university,
                "prior_experience": prior_experience,
                "skill & experience": skills
            }

            final_dic = {
                'user_details': response_data
            }

            s_e = response_data['skill & experience']
            for i in s_e:
                skill, experience = i.split(',')
                gpt_qs(skill, experience)

            question_list = generated_qs()

            final_dic['questions'] = question_list

            return jsonify(final_dic)
        except Exception as e:
            return jsonify(error=str(e)), 400
    else:
        return "This route only accepts POST requests."


# View Route
@app.route('/interview/')
def interview():
    print(' -------------------------------->>>>>>>>>>>> inside interview')
    question_list = generated_qs()

    return render_template('interview.html', question_list=question_list)


list_of_questions = []
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    q_a = {}
    print(' -------------------------------->>>>>>>>>>>> inside submit_answer')
    if request.method == 'POST':
        data = request.json
        question = data.get('question')
        user_answer = data.get('userAnswer')
        q_a['question'] = question
        q_a['answer'] = user_answer  
        list_of_questions.append(q_a)
        message = {"Message": "Answer received successfully"}
        return jsonify(message)  # Return a JSON response
    else:
        return '', 204  # Return a No Content response


@app.route('/all_qs_ans', methods=['GET'])
def all_qs_ans():
    print(list_of_questions)
    print(' -------------------------------->>>>>>>>>>>> INSIDE ALL QS ANS')
    return jsonify(list_of_questions)


@app.route('/evaluate', methods=['GET'])
def evaluate():
    evaluation_responses = []
    print(' -------------------------------->>>>>>>>>>>> INSIDE EVALUTE')
    dic = list_of_questions
    for i in dic:
        evaluation_responses.append(get_answer(i['question'],i['answer']))
    return jsonify(evaluation_responses)

#Evaluation API ROUTE
@app.route('/api/evaluate-answers', methods=['POST'])
def evaluateAnswers():
    try:
        data = request.get_json()  # Parse JSON data from request body
        if not isinstance(data, list):
            return jsonify(error="Invalid JSON data, expected a list"), 400
        
        evaluation_responses = []
        
        for question_data in data:
            question = question_data.get('question')
            answer = question_data.get('answer')
            
            if question and answer:
                evaluation_responses.append(get_answer(question, answer))
            else:
                evaluation_responses.append({'error': 'Missing question or answer'})
        
        return jsonify(evaluation_responses)
    except Exception as e:
        return jsonify(error=str(e)), 500



if __name__ == '__main__':
    app.run(debug=True)

