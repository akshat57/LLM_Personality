import csv
import json
import openai
import time
import os
import requests
from chat_prompts import chat_prompts



def get_question_text(prompt_type, question):
    #writing an if condition for each prompt so that the correct prompt is used everytime

    if prompt_type in ['mpi-gpt35', 'mpi-gpt35-reverse']:
        question_text = 'I ' + question['text_first_person'].lower()
    elif prompt_type in ['whoisgpt', 'whoisgpt-reverse']:
        question_text = 'I ' +  question['text_first_person'].lower()
    elif prompt_type in ['chatgpt-an-enfj', 'chatgpt-an-enfj-reverse']:
        question_text = 'I ' +  question['text_first_person'].lower()

    return question_text

def read_ocean(filename):

    ocean_data = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for r, row in enumerate(csvreader):
            if r > 0:
                text_first_person, text_second_person, label, key = row[4], row[5], row[7], row[9]
                ocean_data.append({'text_first_person':text_first_person, 'text_second_person':text_second_person, 'label':label, 'key':key})

    return ocean_data


if __name__ == '__main__':
    #Read ipip questions 
    filename = 'Data/Tests/ocean_120_corrected.csv'
    ocean_data = read_ocean(filename)

    #Model definitions
    model_name = 'MPT-7b-chat-hf-float32'
    temperature = 0.01
    top_p = 1
    max_tokens = 120

    #Prepare model and output directories
    output_directory = 'Data/Outputs/' + model_name.replace('/', '-') + '/'
    os.makedirs(output_directory, exist_ok=True)

    #START EXPERIMENTS
    for prompt_type in chat_prompts.keys():
        output_filename = output_directory + prompt_type + '.json'

        system_message = chat_prompts[prompt_type]['system_message']
        user_message = chat_prompts[prompt_type]['user_message']

        output_dict = {}
        output_dict['system_prompt'] = system_message
        output_dict['user_prompt'] = user_message
        output_dict['responses'] = []


        ## MPT Prompt
        input_message = '<|im_start|>system\n' + system_message  + '<|im_end|>\n'
        input_message += '<|im_start|>user\n' + user_message + '<|im_end|>\n'
        input_message += '<|im_start|>assistant\n'


        for q, question in enumerate(ocean_data):
            start_time = time.time()
            
            #create input
            question_text = get_question_text(prompt_type, question)
            input_prompt = input_message.replace('{item}', question_text)

            input_dict = {
                "prompt": input_prompt,
                "temperature": temperature,
                "top_p": top_p,
                "max_tokens": max_tokens
            }

            #get model response
            url = "http://localhost:8000/generate"
            response = requests.post(url, json=input_dict)
            response = json.loads(response.text)["text"][0]
            
            processed_response = response.replace(input_prompt, '')

            #store question and response
            question['input_prompt'] = input_prompt
            question['response'] = response
            question['processed_response'] = processed_response
            output_dict['responses'].append(question)

            json_data = json.dumps(output_dict)
            with open(output_filename, "w") as file:
                file.write(json_data)

            #print
            end_time = time.time()
            print(model_name, prompt_type, q, 'TIME:', (end_time - start_time)/60)