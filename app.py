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


@app.route('/submit',methods = ['POST','GET'])
def submit():
    print('-------------------------------->>>>>>>>>>>> INSITE SUBMIT')
    if request.method == 'POST':
        name = request.form['name']
        father_name = request.form['fatherName']
        age = int(request.form['age'])
        university = request.form['university']
        prior_experience = int(request.form['priorExperience'])
        skills = request.form.getlist('skill[]')

        response_data = {
            "name": name,
            "father_name": father_name,
            "age": age,
            "university": university,
            "prior_experience": prior_experience,
            "skill & experience": skills    }

        final_dic = {
            'user_details':response_data
        }
        s_e = response_data['skill & experience']
        for i in s_e:
            skill , experience = i.split(',')
            gpt_qs(skill,experience)

        question_list = generated_qs()
        
        final_dic['questions'] = question_list
        
    return jsonify(final_dic)


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
        evaluation_responses.append(get_answer(i['question'],i['answer']).replace('\n', ''))
    return jsonify(evaluation_responses)


if __name__ == '__main__':
    app.run(debug=True)

