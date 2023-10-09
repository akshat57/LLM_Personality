import csv
import json
import openai
import time
import os
from chat_prompts import chat_prompts

def ask_gpt_chat(model_name, sys_prompt, user_prompt, temperature = 0, top_p = 1):

    MAX_API_RETRY = 5
    for i in range(MAX_API_RETRY):
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature= temperature,
                top_p = top_p
            )
            content = response["choices"][0]["message"]["content"]

            return content
        except Exception as e:
            print(e)
            time.sleep(5 * i)
    print(f"Failed after {MAX_API_RETRY} retries.")

    return None


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
    model_name = 'gpt-3.5-turbo'
    temperature = 0.01
    top_p = 1
    max_tokens = 120

    #Prepare model and output directories
    output_directory = 'Data/Outputs/' + model_name.replace('/', '-') + '/'
    os.makedirs(output_directory, exist_ok=True)

    #START EXPERIMENTS
    for prompt_type in chat_prompts.keys():
        if prompt_type in ['mpi-gpt35', 'mpi-gpt35-reverse', 'chatgpt-an-enfj']:
            continue
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
                response = ask_gpt_chat(model_name, system_prompt, user_prompt)

            #store question and response
            question['input_prompt_system'] = system_prompt
            question['input_prompt_user'] = user_prompt
            question['processed_response'] = response

            output_dict['responses'].append(question)

            json_data = json.dumps(output_dict)
            with open(output_filename, "w") as file:
                file.write(json_data)