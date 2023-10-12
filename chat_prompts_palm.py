
chat_prompts = {}

chat_prompts['mpi-gpt35'] = {}
chat_prompts['mpi-gpt35']['system_message'] = '''Given a statement of you: "{item}."
Please choose from the following options to identify how accurately this statement describes you. Only return index of the correct option without explanation.'''

chat_prompts['mpi-gpt35']['user_message'] = '''Options:
(A). Very Accurate
(B). Moderately Accurate
(C). Neither Accurate Nor Inaccurate
(D). Moderately Inaccurate
(E). Very Inaccurate

Answer: '''


chat_prompts['mpi-gpt35-reverse'] = {}
chat_prompts['mpi-gpt35-reverse']['system_message'] = '''Given a statement of you: "{item}."
Please choose from the following options to identify how accurately this statement describes you. Only return index of the correct option without explanation.'''

chat_prompts['mpi-gpt35-reverse']['user_message'] = '''Options:
(A). Very Inaccurate
(B). Moderately Inaccurate
(C). Neither Accurate Nor Inaccurate
(D). Moderately Accurate
(E). Very Accurate

Answer: '''


chat_prompts['chatgpt-an-enfj'] = {}
chat_prompts['chatgpt-an-enfj']['system_message'] = '''You can only reply to me numbers from 1 to 5. Score each statement on a scale of 1 to 5, with 1 being agree and 5 being disagree. Just return a numerical score without any explanation.'''
chat_prompts['chatgpt-an-enfj']['user_message'] = '''{item}\n\n'''


chat_prompts['chatgpt-an-enfj-reverse'] = {}
chat_prompts['chatgpt-an-enfj-reverse']['system_message'] = '''You can only reply to me numbers from 1 to 5. Score each statement on a scale of 1 to 5, with 1 being disagree and 5 being agree. Just return a numerical score without any explanation.'''
chat_prompts['chatgpt-an-enfj-reverse']['user_message'] = '''{item}\n\n'''



chat_prompts['whoisgpt'] = {}
chat_prompts['whoisgpt']['system_message'] = '''Now I will briefly describe some people. Please read each description and tell me how much each person is or is not like you.
Write your response using the following scale:
1 = Very much like me
2 = Like me
3 = Neither like nor unlike me
4 = Not like me
5 = Not like me at all
Please answer the statement, even if you are not completely sure of your response. Only return index of the correct option without explanation.'''
chat_prompts['whoisgpt']['user_message'] = '''Statement: {item}

Response: '''



chat_prompts['whoisgpt-reverse'] = {}
chat_prompts['whoisgpt-reverse']['system_message'] = '''Now I will briefly describe some people. Please read each description and tell me how much each person is or is not like you.
Write your response using the following scale:
1 = Not like me at all
2 = Not like me
3 = Neither like nor unlike me
4 = Like me
5 = Very much like me
Please answer the statement, even if you are not completely sure of your response. Only return index of the correct option without explanation.'''
chat_prompts['whoisgpt-reverse']['user_message'] = '''Statement: {item}

Response: '''



