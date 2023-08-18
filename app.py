from flask import Flask , redirect , url_for , render_template,request,jsonify
import json
from questions import gpt_qs
from response_read import generated_qs , speak_qs , get_answer , clear_text_file
import time


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questions/<output>')
def questions(output):
    output = eval(output)
    s_e = output['skill & experience']
    for i in s_e:
        skill , experience = i.split(',')
        gpt_qs(skill,experience)
    return redirect(url_for('interview'))



@app.route('/interview/',methods = ['POST','GET'])
def interview():
    question_list = generated_qs()

    return render_template('interview.html', question_list=question_list)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if request.method == 'POST':
        data = request.json
        question = data.get('question')
        user_answer = data.get('userAnswer')
        print('Question ------------->', question)
        print('Answer ---------------->', user_answer)
        
        # Process the data as needed
        response = get_answer(question,user_answer)
        print('first question')
        print(response)
        print('first response')
        response_data = {"message": "Answer received successfully"}
        return jsonify(response_data)  # Return a JSON response
    else:
        return '', 204  # Return a No Content response


@app.route('/submit',methods = ['POST','GET'])
def submit():
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
            "skill & experience": skills
        }

    return return jsonify(response_data)



if __name__ == '__main__':
    app.run(debug=True)


########################################################### OLD CODE ##################################################################

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/questions/<output>')
# def questions(output):
#     output = eval(output)
#     s_e = output['skill & experience']
#     for i in s_e:
#         skill , experience = i.split(',')
#         gpt_qs(skill,experience)
#     return redirect(url_for('interview'))



# @app.route('/interview/',methods = ['POST','GET'])
# def interview():
#     question_list = generated_qs()

#     return render_template('interview.html', question_list=question_list)

# @app.route('/submit_answer', methods=['POST'])
# def submit_answer():
#     if request.method == 'POST':
#         data = request.json
#         question = data.get('question')
#         user_answer = data.get('userAnswer')
#         print('Question ------------->', question)
#         print('Answer ---------------->', user_answer)
        
#         # Process the data as needed
#         response = get_answer(question,user_answer)
#         print('first question')
#         print(response)
#         print('first response')
#         response_data = {"message": "Answer received successfully"}
#         return jsonify(response_data)  # Return a JSON response
#     else:
#         return '', 204  # Return a No Content response


# @app.route('/submit',methods = ['POST','GET'])
# def submit():
#     if request.method == 'POST':
#         name = request.form['name']
#         father_name = request.form['fatherName']
#         age = int(request.form['age'])
#         university = request.form['university']
#         prior_experience = int(request.form['priorExperience'])
#         skills = request.form.getlist('skill[]')

#         response_data = {
#             "name": name,
#             "father_name": father_name,
#             "age": age,
#             "university": university,
#             "prior_experience": prior_experience,
#             "skill & experience": skills
#         }
#         print('BEOFRE JSON',response_data)
#         response_data = json.dumps(response_data)
#         print('AFTER JSON',response_data)

#     return redirect(url_for('questions',output = response_data))



# if __name__ == '__main__':
#     app.run(debug=True)
