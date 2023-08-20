import os
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import time
import pyttsx3 as sp
from constant import openai_key
os.environ['OPENAI_API_KEY'] = openai_key


# def initialize_voice_prompt_templtate():
#     ''' Initializes llm temperature , prompt template and llm chain '''
#     global llm , first_ans , correct_per
#     llm = OpenAI(temperature=0.8)

#     first_ans = PromptTemplate(
#         input_variables = ['qs','ans'] ,
#         template='Given the question "\{qs}"\, how accurate do you believe this answer "\{ans}"\ is on a percentage scale?')

#     correct_per = LLMChain(llm=llm , prompt=first_ans,verbose=True) 


def generated_qs():
    ''' Returns already written questions in form of a python list '''
    global cleaned_contents
    with open('questions.txt', 'r') as file:
        file_contents = file.readlines()

    cleaned_contents = [line[3:].rstrip('\n') for line in file_contents if line != '\n']
    return cleaned_contents

def speak_qs(content):
    ''' Speaks question that is given as a parameter '''
    tts = sp.init()
    tts.setProperty('rate', 150)
    voices = tts.getProperty('voices')
    tts.setProperty('voice', voices[0].id) # 0 for male and 1 for female
    tts.say(content)
    tts.runAndWait()

def get_answer(content,answer):
    ''' Accepts question and answer as parameters and returns whether answer is correct or not wrt to the question '''
    llm = OpenAI(temperature=0.8)

    first_ans = PromptTemplate(
        input_variables = ['qs','ans'] ,
        template='Given the question "\{qs}"\, how accurate do you believe this answer "\{ans}"\ is on a percentage scale, make sure to only return percentage and nothing else?')

    correct_per = LLMChain(llm=llm , prompt=first_ans,verbose=True) 
    response = correct_per.run(qs=content , ans = answer)
    return response

def clear_text_file(file_path):
    try:
        with open(file_path, 'w') as file:
            file.truncate(0)
        print(f"Content of {file_path} has been cleared.")
    except Exception as e:
        print(f"An error occurred: {e}")


