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
        for response in data['responses']:
            label, key, answer = response['label'], response['key'], response['processed_response']

            pattern = r'\((A|B|C|D|E)\)|(A|B|C|D|E)\.'
            compiled_pattern = re.compile(pattern)
            match = compiled_pattern.findall(answer)

            score_index = None
            if len(match) == 1:

                if len(match[0][0]):
                    score_index = match[0][0]
                else:
                    score_index = match[0][1]
            else:
                collected_match = []
                for m in match:
                    if len(m[0]):
                        collected_match.append(m[0])
                    else:
                        collected_match.append(m[1])

                if len(set(collected_match)) == 1:
                    score_index = collected_match[0]

            if score_index:
                option_list[label].append(score_index)
                if score_index in score_map:
                    score = score_map[score_index]
                    if prompt_type.find('reverse') != -1:
                        score = invert_score[score]

                    if key == -1:
                        score = invert_score[score]
                
                    score_list[label].append(score)




    if prompt_type in ['whoisgpt.json', 'whoisgpt-reverse.json']:
        for response in data['responses']:
            label, key, answer = response['label'], response['key'], response['processed_response'] 

            pattern = r'\b[1-5]\b'
            compiled_pattern = re.compile(pattern)
            match = compiled_pattern.findall(answer)
            if len(match) == 1:
                score_index = match[0]
                option_list[label].append(score_index)

                if score_index in score_map:
                    score = score_map[score_index]
                    if prompt_type.find('reverse') != -1:
                        score = invert_score[score]
                    if key == -1:
                        score = invert_score[score]
                
                    score_list[label].append(score)


    if prompt_type in ['chatgpt-an-enfj.json', 'chatgpt-an-enfj-reverse.json']:
        for response in data['responses']:
            label, key, answer = response['label'], response['key'], response['processed_response']

            score_index = answer.strip()
            if len(score_index) == 1:
                option_list[label].append(score_index)

                if score_index in score_map:
                    score = score_map[score_index]
                    if prompt_type.find('reverse') != -1:
                        score = invert_score[score]
                    if key == -1:
                        score = invert_score[score]
                
                    score_list[label].append(score)

            else:
                pattern = r'\b[1-5]\b'
                compiled_pattern = re.compile(pattern)
                match = compiled_pattern.findall(answer)
                if len(match) == 1:
                    score_index = match[0]
                    option_list[label].append(score_index)

                    if score_index in score_map:
                        score = score_map[score_index]
                        if prompt_type.find('reverse') != -1:
                            score = invert_score[score]
                        if key == -1:
                            score = invert_score[score]
                    
                        score_list[label].append(score)



    return score_list, option_list



if __name__ == '__main__':
    location = '../Data/Outputs/'

    model_name = 'Llama-2-7b-chat-hf-api-llamaprompt-original-float32'
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
                print(model_name, prompt_type.replace('.json', ''), trait, mean_score, std, 'MOST COMMON:', most_common_score, 'LEN:', len(score_list[trait]), 'A:', option_list[trait])