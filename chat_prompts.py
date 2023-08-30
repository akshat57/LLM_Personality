
chat_prompts = {}

chat_prompts['mpi-gpt35'] = {}
chat_prompts['mpi-gpt35']['system_message'] = '''Given a statement of you: "{item}."
Please choose from the following options to identify how accurately this statement describes you.'''

chat_prompts['mpi-gpt35']['user_message'] = '''Options:
(A). Very Accurate
(B). Moderately Accurate
(C). Neither Accurate Nor Inaccurate
(D). Moderately Inaccurate
(E). Very Inaccurate

Answer: '''


chat_prompts['mpi-gpt35-reverse'] = {}
chat_prompts['mpi-gpt35-reverse']['system_message'] = '''Given a statement of you: "{item}."
Please choose from the following options to identify how accurately this statement describes you.'''

chat_prompts['mpi-gpt35-reverse']['user_message'] = '''Options:
(A). Very Inaccurate
(B). Moderately Inaccurate
(C). Neither Accurate Nor Inaccurate
(D). Moderately Accurate
(E). Very Accurate

Answer: '''



chat_prompts['chatgpt-an-enfj'] = {}
chat_prompts['chatgpt-an-enfj']['system_message'] = '''You can only reply to me numbers from 1 to 5. Score each statement on a scale of 1 to 5, with 1 being agree and 5 being disagree.'''
chat_prompts['chatgpt-an-enfj']['user_message'] = '''{item}\n\n'''


chat_prompts['whoisgpt'] = {}
chat_prompts['whoisgpt']['system_message'] = '''Now I will briefly describe some people. Please read each description and tell me how much each person is or is not like you.
Write your response using the following scale:
1 = Very much like me
2 = Like me
3 = Somewhat like me
4 = Not like me
5 = Not like me at all
Please answer the statement, even if you are not completely sure of your response.'''
chat_prompts['whoisgpt']['user_message'] = '''Statement: {item}

Response: '''


