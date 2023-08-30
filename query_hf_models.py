from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
import os
from chat_prompts import chat_prompts
import csv
import json
import time 


def generate(model, tokenizer, device, message, temperature, top_p, max_tokens):
    input_text = message
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)

    gen_tokens = model.generate(input_ids, do_sample=True, temperature=temperature, max_length=max_tokens, pad_token_id=tokenizer.eos_token_id)
    
    gen_text = tokenizer.batch_decode(gen_tokens)[0]

    return gen_text 



def read_ocean(filename):

    ocean_data = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for r, row in enumerate(csvreader):
            if r > 0:
                text_first_person, text_second_person, label, key = row[4], row[5], row[7], row[9]
                ocean_data.append({'text_first_person':text_first_person, 'text_second_person':text_second_person, 'label':label, 'key':key})

    return ocean_data

def get_question_text(prompt_type, question):
    #writing an if condition for each prompt so that the correct prompt is used everytime

    if prompt_type in ['mpi-gpt35', 'mpi-gpt35-reverse']:
        question_text = 'I ' + question['text_first_person'].lower()
    elif prompt_type == 'whoisgpt':
        question_text = 'I ' +  question['text_first_person'].lower()
    elif prompt_type == 'chatgpt-an-enfj':
        question_text = 'I ' +  question['text_first_person'].lower()

    return question_text
    

            

if __name__ == '__main__':

    #Read ipip questions 
    filename = 'Data/Tests/ocean_120_corrected.csv'
    ocean_data = read_ocean(filename)

    #Model definitions
    model_dir = '/data/akshat/models/'
    #model_name = 'Llama-2-13b-chat-hf'
    model_name = 'falcon-7b-instruct'
    model_location = model_dir + model_name
    temperature = 0.01
    top_p = 1
    max_tokens = 120
    gpu_index = 10

    #Prepare model and output directories
    output_directory = 'Data/Outputs/' + model_name.replace('/', '-') + '/'
    os.makedirs(output_directory, exist_ok=True)

    device = torch.device(f"cuda:{gpu_index}" if torch.cuda.is_available() and gpu_index >= 0 and gpu_index < 8 else "cpu")
    print(device, model_name, 'Loading Model..')
    model = AutoModelForCausalLM.from_pretrained(model_location, trust_remote_code=True, token='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').to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_location)


    #START EXPERIMENTS
    for prompt_type in chat_prompts.keys():
        if prompt_type != 'mpi-gpt35-reverse':
            continue
        print(prompt_type)
        output_filename = output_directory + prompt_type + '.json'

        system_message = chat_prompts[prompt_type]['system_message']
        user_message = chat_prompts[prompt_type]['user_message']

        output_dict = {}
        output_dict['system_prompt'] = system_message
        output_dict['user_prompt'] = user_message
        output_dict['responses'] = []

        input_message = system_message + '\n\n' + user_message

        for q, question in enumerate(ocean_data):
            start_time = time.time()
            
            #create input
            question_text = get_question_text(prompt_type, question)
            input_prompt = input_message.replace('{item}', question_text)

            #get model response
            response = None
            while not response:
                response = generate(model, tokenizer, device, input_prompt, temperature, top_p, max_tokens)
            processed_response = response.replace(input_prompt, '').replace('<|endoftext|>', '')

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



    
