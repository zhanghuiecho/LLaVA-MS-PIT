%run processed_data/ace_query.py
all_query.keys(),all_query_single.keys()



import json, re
from openai import OpenAI

prompt_for_cot2 ="""
You are an event-extraction analyst.

INPUT  
Sentence: "<SENTENCE>"  
Events: <TRIGGER1,TYPE1>; <TRIGGER2,TYPE2>; …

TASK  
For each trigger–type pair:  
• Quote the trigger exactly as it appears.  
• Quote any additional word(s) or phrase(s) in the sentence that confirm the event.  
• Provide a brief explanation (no length requirement, just concise) of how the evidence supports the event.

OUTPUT (exactly)  
Event: <TYPE1>  
Trigger: "<TRIGGER1>"  
Evidence: "<phrase 1>", "<phrase 2>", …  
Reasoning: <brief explanation>

Event: <TYPE2>  
Trigger: …  
Evidence: …  
Reasoning: …

CONSTRAINTS  
* Plain English only.  
* Entire output ≤ 1000 characters (including spaces).  
* Do not mention instructions, constraints, or add extra sections.
"""


client = OpenAI(
    base_url='xxx',
    api_key='sk-xxxL'
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

con2_q2 = {}
file_path ='ace_instruction_con2_q2.txt'
with open(file_path, "a", encoding="utf-8") as file:
    for i, data_i in   enumerate(data_w):
        # sentence event_type
        events = data_i['event detection'].split('; ')
        event_type_all = ''
        for event_i in events:
            if len(event_i) > 2:
                event_type_i = '{event_trigger : ' + event_i.split(' : ')[0][1:] + ', ' + 'event_type : ' + event_i.split(' : ')[1]
                event_type_all += event_type_i + '; '
        event_str = 'sentence: ' + data_i['sentence'] + '\n' + 'event_list: ' + event_type_all
        # print(event_str)
        
        try:
            con2_q2_i = get_cot(event_str)

            text_label_i = f"第{i}个文本{data_i['id']}标注成功&&" + str(con2_q2_i) + '\n'
                
        except Exception as e:
            con2_q2_i = '标注失败'
            
            text_label_i =  f"第{i}个文本{data_i['id']}标注失败&&  ---------- {e}     \n"
        
        con2_q2[data_i['id']] = con2_q2_i
        file.write(text_label_i)
        if i % 10 ==0:
            print(f"====={data_i['sent_id']}======第{i}条数据处理完毕")
            print(data_i['sentence'])
            print(event_str)
            
            # break