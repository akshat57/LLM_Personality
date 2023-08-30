import json
import os
import numpy as np
import re
import math
from collections import Counter


def most_common_element(lst):
    counter = Counter(lst)
    most_common = counter.most_common(1)
    
    if most_common:
        return most_common[0][0]
    else:
        return None



def get_score(model_name, prompt_type, data):
    score_map = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1, '1':5, '2':4, '3':3, '4':2, '5':1}
    invert_score = {5:1, 4:2, 3:3, 2:4, 1:5}


    score_list = {'O':[], 'C':[], 'E':[], 'A':[], 'N':[]}
    option_list = {'O':[], 'C':[], 'E':[], 'A':[], 'N':[]}

    if prompt_type in ['mpi-gpt35.json', 'mpi-gpt35-reverse.json']:
        if model_name in ['Llama-2-7b-chat-hf', 'Llama-2-13b-chat-hf', 'gpt-3.5-turbo', 'falcon-7b-instruct']:
            
            for response in data['responses']:
                if model_name == 'gpt-3.5-turbo':
                    label, key, answer = response['label'], response['key'], response['response']    
                else:
                    label, key, answer = response['label'], response['key'], response['processed_response']

                pattern = r"\((\w)\)"
                match = re.search(pattern, answer)

                if match:
                    score_index = match.group(1)
                    option_list[label].append(score_index)

                    if score_index in score_map:
                        score = score_map[score_index]
                        if prompt_type.find('reverse') != -1:
                            score = invert_score[score]

                        if key == -1:
                            score = invert_score[score]
                    
                        score_list[label].append(score)

    if prompt_type == 'whoisgpt.json' and model_name == 'gpt-3.5-turbo':
        for response in data['responses']:
            label, key, answer = response['label'], response['key'], response['response']    
            score_index = answer.split('=')[0].strip()
            option_list[label].append(score_index)

            if score_index in score_map:
                score = score_map[score_index]
                if key == -1:
                    score = invert_score[score]
            
                score_list[label].append(score)


    if (prompt_type == 'chatgpt-an-enfj.json' and model_name == 'gpt-3.5-turbo') or (prompt_type == 'whoisgpt.json' and model_name == 'falcon-7b-instruct'):
        for response in data['responses']:
            if model_name == 'gpt-3.5-turbo':
                label, key, answer = response['label'], response['key'], response['response']    
            else:
                label, key, answer = response['label'], response['key'], response['processed_response']

            score_index = answer.strip()
            option_list[label].append(score_index)

            if score_index in score_map:
                score = score_map[score_index]
                if key == -1:
                    score = invert_score[score]
            
                score_list[label].append(score)




    return score_list, option_list



if __name__ == '__main__':
    location = 'Data/Outputs/'



    for model_name in os.listdir(location):
        file_location = location + model_name + '/'

        for prompt_type in os.listdir(file_location):
            filename = file_location + prompt_type

            with open(filename, 'r') as json_file:
                data = json.load(json_file)

            score_list, option_list = get_score(model_name, prompt_type, data)

            if sum([len(scores) for scores in score_list.values()]):
                for trait in score_list:
                    mean_score = round(np.mean(np.array(score_list[trait])), 2)
                    std = round(np.std(np.array(score_list[trait])), 2)
                    most_common_score = most_common_element(option_list[trait])
                    print(model_name, prompt_type.replace('.json', ''), trait, mean_score, std, 'MOST COMMON:', most_common_score)





        '''score_list = {'O':[], 'C':[], 'E':[], 'A':[], 'N':[]}
        for response in data['responses']:
            label = response['label']
            key = response['key']
            answer = response['response']

            #calculate score
            if 'mpi' in filename:
                answer = answer.split('.')[0].replace('(', '').replace(')', '')
            elif 'whoisgpt' in filename:
                answer = answer.split('=')[0].strip()

            if answer in score_map:
                score = score_map[answer]
  
                if key == -1:
                    score = invert_score[score]
            
                score_list[label].append(score)


        print(file)
        for trait in score_list:
            mean_score = round(np.mean(np.array(score_list[trait])), 2)
            std = round(np.std(np.array(score_list[trait])), 2)
            print(trait, mean_score, std )

        print()'''
