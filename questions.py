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









# sk_exp = [('Vector Databases',5),('Sequence Models',2),('Dockers',5),('pandas',1),('tensorflow',3)]
# for skill,experience in sk_exp:
#     response = question.run(skill_qs=skill, experience=experience)
#     with open('test.txt', 'a') as file:
#         file.write(response)
