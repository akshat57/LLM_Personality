import csv
import json
import openai
import time
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


def read_ocean(filename):

    ocean_data = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for r, row in enumerate(csvreader):
            if r > 0:
                text, label, key = row[4], row[6], row[8]
                ocean_data.append({'text':text, 'label':label, 'key':key})


    return ocean_data

if __name__ == '__main__':
    filename = 'Data/ocean_120.csv'
    ocean_data = read_ocean(filename)

    #model_name = 'gpt-3.5-turbo'
    model_name = 'gpt-4'

    for prompt_type in chat_prompts.keys():
        output_filename = 'Data/Outputs/' + model_name + '_' + prompt_type + '.json'

        system_message = chat_prompts[prompt_type]['system_message']
        user_message = chat_prompts[prompt_type]['user_message']

        output_dict = {}
        output_dict['system_prompt'] = system_message
        output_dict['user_prompt'] = user_message
        output_dict['responses'] = []

        for q, question in enumerate(ocean_data):
            print(prompt_type, q)
            system_prompt = system_message.replace('{item}', question['text'])
            user_prompt = user_message.replace('{item}', question['text'])

            response = None
            while not response:
                response = ask_gpt_chat(model_name, system_prompt, user_prompt)

            question['response'] = response

            output_dict['responses'].append(question)

            json_data = json.dumps(output_dict)
            with open(output_filename, "w") as file:
                file.write(json_data)