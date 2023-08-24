import json
import os
import numpy as np

if __name__ == '__main__':
    location = 'Data/Outputs/'

    score_map = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1, '1':5, '2':4, '3':3, '4':2, '5':1}
    invert_score = {5:1, 4:2, 3:3, 2:4, 1:5}


    for file in os.listdir(location):
        filename = location + file

        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        score_list = {'O':[], 'C':[], 'E':[], 'A':[], 'N':[]}
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

        print()
