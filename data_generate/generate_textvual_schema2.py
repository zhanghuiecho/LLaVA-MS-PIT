%run processed_data/ace_query.py
all_query.keys(),all_query_single.keys()


import json, re
from openai import OpenAI

prompt_for_cot2 ="""
Based on the given sentence and event, explain the reasoning for why a specific event argument plays the specified role in the event. Clarify the concrete significance of this argument for the sentence and the event. Requirements: Keep your answer concise, logically clear, and within 1000 characters. Only include content directly relevant to the reasoning and explanation; do not output any unrelated text.

Input format:
Sentence: [sentence content]
Event Trigger AND Event Type : {event trigger1 : event type1}; {event trigger2 : event type2}; ...
Argument AND Role : {argument role11 : text11, argument role12 : text12, ...}; {argument role21 : text21, argument role22 : text22, ...}; ...


Output format:
Reasoning: [brief reasoning for why the argument plays this role in the event]
Significance: [explain the specific significance of the argument to the sentence and the event]
"""


client = OpenAI(
    base_url='xxxx',
    api_key='sk-xxxx'
)
def get_cot(event_str ):
    completion = client.chat.completions.create(
      model="gpt-4o",#gpt-4  o1-mini
      messages=[
        {"role": "system", "content": "You are an helpful expert in event extraction"},#a helpful assistant."},
        {"role": "user", "content": prompt_for_cot2+ '\n' + str(event_str)}#
      ]
    )
    return completion.choices[0].message.content

filename = r"xxxx\train.json"
with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f) 
len(data)

con2_q3 = {}
file_path ='ace_instruction_con2_q3.txt'
with open(file_path, "a", encoding="utf-8") as file:
    for i, data_i in   enumerate(data_w):
        if data_i['sent_id'] not in null_data:
            continue
        # sentence event_type
        events = data_i['event detection'].split('; ')
        event_type_all = ''
        for event_i in events:
            if len(event_i) > 2:
                event_type_i = '{event_trigger : ' + event_i.split(' : ')[0][1:] + ', ' + 'event_type : ' + event_i.split(' : ')[1]
                event_type_all += event_type_i + '; '
        event_str = 'sentence: ' + data_i['sentence'] + '\n' + 'Event Trigger AND Event Type : ' + event_type_all + '\nArgument AND Role : ' + data_i['event_mentions']
        
        try:
            con2_q3_i = get_cot(event_str)

            text_label_i = f"第{i}个文本{data_i['sent_id']}标注成功&&" + str(con2_q3_i) + '\n'
                
        except Exception as e:
            con2_q3_i = '标注失败'           
            text_label_i =  f"第{i}个文本{data_i['sent_id']}标注失败&&  ---------- {e}     \n"
        
        con2_q3[data_i['id']] = con2_q3_i
        file.write(text_label_i)
        if i % 1 ==0:
            print(text_label_i)
            