prompt_cot = """You are an expert in event extraction. Given a sentence and its corresponding extracted events, your task is to generate a clear, structured, and concise step-by-step chain-of-thought reasoning process for identifying and extracting events according to the provided "event_mentions".

Strict Requirements:

Limit your total output to no more than 1500 characters.

The reasoning process must be brief, clear, and strictly focused on the extraction logic.

Only describe the necessary steps to identify triggers, event types, roles, arguments, and their relationships.

Avoid all redundant, repetitive, or unnecessary analysis or commentary.

Do not provide any extra explanations, disclaimers, background, or additional information.

Ensure the logic and conclusions strictly match the provided "event_mentions".

After your step-by-step reasoning, present the final extracted events exactly as shown in "event_mentions", using the following exact phrase and format, with no added text, headers, or formatting:

"Therefore, final event extraction results:\n[Answer]: "

Here is the sentence, along with its corresponding extracted events:
"""
import json
from openai import OpenAI

client = OpenAI(
    base_url='xxxx',
    api_key='sk-xxxxx'
)
def get_cot(event_str ):
    completion = client.chat.completions.create(
      model="gpt-4o",#gpt-4  o1-mini
      messages=[
        {"role": "system", "content": "You are an helpful expert in event extraction"},#a helpful assistant."},
        {"role": "user", "content": prompt_cot+ '\n' + str(event_str)}#
      ]
    )
    return completion.choices[0].message.content

filename = r"D:\mmee_data_sft_llava\ACE05_llava\cot2_generate\data_format4generate_cot\train.json"
with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f) 
len(data)

con2_q2_new = {}
file_path ='ace_instruction_cot_0.txt'
with open(file_path, "a", encoding="utf-8") as file:
    for i, data_i in   enumerate(data_w):
        events = data_i['event_mentions']#.split('; ')
        event_str = 'sentence: ' + data_i['sentence'] + '\n' + 'event_list: ' + events
        try:
            con2_q2_i = get_cot(event_str)
            text_label_i = f"第{i}个文本{data_i['id']}标注成功&&" + str(con2_q2_i) + '\n'

        except Exception as e:
            con2_q2_i = '标注失败'
            text_label_i =  f"第{i}个文本{data_i['id']}标注失败&&  ---------- {e}     \n"

        con2_q2_new[data_i['id']] = con2_q2_i
        file.write(text_label_i)
        if i % 30 ==0:
            print(text_label_i)
            print(data_i['sentence'])
            print(event_str)

            # break