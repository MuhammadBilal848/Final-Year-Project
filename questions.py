import os
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from constant import openai_key

os.environ['OPENAI_API_KEY'] = openai_key



def gpt_qs(skill,experience):
    ''' The function takes skill and experience as params & generates questions '''
    # tempratture param controls how balance the reponse should be
    llm = OpenAI(temperature=0.8)

    first_question = PromptTemplate(
        input_variables = ['skill_qs','experience'] ,
        template = 'Write 2 difficult questions about {skill_qs} skill for a person having {experience} years of experience')

    question = LLMChain(llm=llm , prompt=first_question,verbose=True) 
    response = question.run(skill_qs=skill, experience=experience)
    with open('questions.txt', 'a') as file:
        file.write(response)



def t(desired_role,previous_job_tile,total_experience,employment_duration,job_responsibilities,skill_experience):
    llm = OpenAI(temperature=0.6)

    questions = PromptTemplate(
        input_variables = ['desired_role','previous_job_tile','total_experience','employment_duration','job_responsibilities','skill_experience'] ,
        template = '''I want you to write 10 technical interview questions for an interview candidate with total experience of {total_experience} Year who 
        is applying for the role of {desired_role} 
        and had a recent job role of {previous_job_tile} for {employment_duration} and had following responsibilites:
        {job_responsibilities}. 
        The interview candidate has different years of experience in different skills:{skill_experience}.
        Make sure to not ask question related to previous work, just ask technical questions. Make sure to not include anything other 
        than questions.''')

    question = LLMChain(llm=llm , prompt=questions,verbose=True) 
    response = question.run(desired_role = desired_role ,previous_job_tile = previous_job_tile,total_experience=total_experience,employment_duration = employment_duration,
                            job_responsibilities = job_responsibilities,skill_experience = skill_experience)
    print(response)

t('Machine Learning Engineer','Machine Learning Intern',4,'6 Months','["Data Collection","Model Selection","Feature Engineering","EDA","Research"]',
'["Python","Machine Learning Models","Scikit Learn","Matplotlib","Selenium","Anaconda","Tensorflow"]')

# t('Full Stack Developer','Javascript Intern','6','1 Year','["Design and develop web applications","Work with front-end and back-end technologies","Write clean and efficient code","Troubleshoot and debug applications","Work with a team to deliver projects on time and within budget"]',
# '["JavaScript", "HTML", "CSS", "React", "Node.js"]')
# t('Machine Learning Engineer','Machine Learning Intern','6 Months',
#   "Research","Tensorflow,2")
