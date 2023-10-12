import csv
import json
import time
import os
import google.generativeai as palm
from chat_prompts_palm import chat_prompts

def ask_palm_chat(sys_prompt, user_prompt, temperature = 0, top_p = 1):
    palm.configure(api_key=os.environ['PALM_API_KEY'])

    response = palm.chat(context=sys_prompt, 
                messages=user_prompt,
                temperature=temperature,
                top_p=top_p)
    
    content = response.messages[1]['content']

    return content


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
    ipip_dataset = '120'
    filename = 'Data/Tests/ocean_' + ipip_dataset + '_corrected.csv'
    ocean_data = read_ocean(filename, ipip_dataset)

    #Model definitions
    model_name = 'palm'
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

        for q, question in enumerate(ocean_data):
            print(prompt_type, q)

            question_text = get_question_text(prompt_type, question)
            system_prompt = system_message.replace('{item}', question_text)
            user_prompt = user_message.replace('{item}', question_text)

            response = None
            while not response:
                response = ask_palm_chat(system_prompt, user_prompt, temperature, top_p)

            #store question and response
            question['input_prompt_system'] = system_prompt
            question['input_prompt_user'] = user_prompt
            question['processed_response'] = response

            output_dict['responses'].append(question)

            json_data = json.dumps(output_dict)
            with open(output_filename, "w") as file:
                file.write(json_data)

            break