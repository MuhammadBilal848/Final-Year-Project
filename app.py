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

    # template_content = render_template('page 1.html',result = output)
    # time.sleep(20)

    # final_content = f"{template_content}<script>setTimeout(function() {{ window.location.href = '{'/interview'}'; }}, {1 * 10});</script>"
    # final_content = f"{template_content}<script>window.location.href = '{'/interview'}';</script>"
    print('REDIRECTINGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG')
    return redirect(url_for('interview'))

@app.route('/interview/')
def interview():
    question_list = generated_qs()

    # question_data = []
    # for q in question_list:
    #     spoken_question = speak_qs(q)
    #     question_data.append({'question': q, 'spoken_question': spoken_question})
        
    
    return render_template('interview.html', question_list=question_list)


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
        response_data = json.dumps(response_data)
    return redirect(url_for('questions',output = response_data))

if __name__ == '__main__':
    app.run(debug=True)

# Jinja is a web template engine for the Python programming language
# '''
# {%...%} for statements
# {{...}} for expressions
# {#...#} for comments
# '''
