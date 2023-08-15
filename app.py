from flask import Flask , redirect , url_for , render_template,request,jsonify
import json

app = Flask(__name__)

# Jinja is a web template engine for the Python programming language
# '''
# {%...%} for statements
# {{...}} for expressions
# {#...#} for comments
# '''
    
@app.route('/')
def home():
    # we can use any html file we want using render_template(file_name), for this we must create a folder 
    # named 'templates' in the same directory as this file and create html files there.
    return render_template('index.html')

@app.route('/passed/<score>')
def passed(score):
    print(type(score))
    print(score,type(score))
    print(eval(score) , type(eval(score)))
    return render_template('result 1.html',result = eval(score))


 
@app.route('/submit',methods = ['POST','GET'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        print('name------------------>',name)
        father_name = request.form['fatherName']
        print('fatherName------------------>',father_name)
        age = int(request.form['age'])
        print('age------------------>',age)
        university = request.form['university']
        print('university------------------>',university)
        prior_experience = int(request.form['priorExperience'])
        print('priorExperience------------------>',prior_experience)
        skills = request.form.getlist('skill[]')
        print('skills------------------>',skills)

        
        # total_skill_experience = 0
        # for skill in skills:
        #     skill_name, experience = skill.split(' (')
        #     experience = int(experience[:-7])
        #     total_skill_experience += experience
        
        response_data = {
            "name": name,
            "father_name": father_name,
            "age": age,
            "university": university,
            "prior_experience": prior_experience,
            "kill_experience": skills
        }
        response_data = json.dumps(response_data)
        print(response_data , type(response_data))
    return redirect(url_for('passed',score = response_data))

    # total_score = 0
    # if request.method == 'POST':
    #     datastructure = float(request.form['datastructure']) 
    #     linearalgebra  = float(request.form['linearalgebra'])
    #     statistics = float(request.form['statistics'])      
    #     total_score = (datastructure+linearalgebra+statistics)/3
    # syntax - redirect(url_for(route_name,parameter_which_route_name_is_using = parameter_which_current_route_is_using))

if __name__ == '__main__':
    app.run(debug=True)
