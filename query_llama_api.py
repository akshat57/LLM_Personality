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


def read_ocean(filename, ipip):

    ocean_data = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for r, row in enumerate(csvreader):
            if r > 0:
                if ipip == '120':
                    text_first_person, text_second_person, label, key = row[4], row[5], row[7], row[9]
                elif ipip == '300':
                    text_first_person, text_second_person, label, key = row[4], row[5], row[6], row[8]
                ocean_data.append({'text_first_person':text_first_person, 'text_second_person':text_second_person, 'label':label, 'key':key})

    return ocean_data


if __name__ == '__main__':
    #Read ipip questions 
    ipip_dataset = '300'
    filename = 'Data/Tests/ocean_' + ipip_dataset + '_corrected.csv'
    ocean_data = read_ocean(filename, ipip_dataset)

    #Model definitions
    model_name = 'Llama-2-70b-chat-hf-api-llamaprompt-original'
    temperature = 0.01
    top_p = 1
    max_tokens = 120

    #Prepare model and output directories
    output_directory = 'Data/Outputs_' + ipip_dataset + '/' + model_name.replace('/', '-') + '/'
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

        #input_message = system_message + '\n\n' + user_message

        ## Llama prompt type 1
        '''input_message = "<<SYS>>\n"
        input_message += system_message + "\n"
        input_message += "<</SYS>>\n\n"
        input_message += "[INST] " + user_message + "\n[/INST]\n\n"'''

        ## Llama prompt type 2 - original
        input_message = "<s>[INST] <<SYS>>\n"
        input_message += system_message.strip() + "\n"
        input_message += "<</SYS>>\n\n"
        input_message += user_message.strip() + " [/INST]"


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