import os
from openai import OpenAI
import base64
import json
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

client = OpenAI(
    base_url='xxxxx',
    api_key='sk-xxx'
)

def get_text_label_from(image,prompt):
    base64_image = image_to_base64(image)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        }
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    content = response.choices[0].message.content

    return content
    
prompt ="""Given the image, generate a concise visual schema structured specifically for multimodal event extraction.

Only focus on critical objects that directly contribute to or indicate the occurrence of an event. For each critical object clearly list:
- object name
- visual attributes relevant to the event (e.g., color, size, state)
- actions performed by the object (if any)
- relations with other critical objects (as [relation, object] pairs)

Do NOT include irrelevant objects or details not related to potential events.

Output format:

Image visual schema:
- object: [object name]
  attributes: [attribute1, attribute2, ...]
  actions: [action1, action2, ...]
  relations:
    - relation: [relation type], object: [related object]
  ...
Scene: [scene context]

Example:
Image visual schema:
- object: person
  attributes: [male, wearing red shirt]
  actions: [throwing]
  relations:
    - relation: holding, object: ball
    - relation: next to, object: dog
- object: dog
  attributes: [brown, small]
  actions: [jumping]
  relations:
    - relation: next to, object: person
- object: ball
  attributes: [blue]
  actions: []
  relations: []
Scene: outdoor playground
"""


all_data_path = r"xxxx\new_swig_with_text_label.json"
with open(all_data_path,'r',encoding='utf-8') as f:
    all_data_event = json.load(f)

path = r"xxx\picture"
num = 0
w_all_text_label =  []
w_all_text_label_dict = {}
with open(f'new_swig_all_processed_text_label_w_event_SG_{0}.json', 'w', encoding='utf-8') as f2:
    for image_i,image_i_info in all_data_event.items():
        
        if '{' in image_i_info['image_event_mention']:
            w_all_text_label_dict_i = {}
            
            image_i_path = os.path.join(path,image_i)

            try:
                sentence = get_text_label_from(image_i_path,prompt)
                text_label_i = f'第{num}个图像{image_i}标注成功&&' + str(sentence) + '\n'
                
            except Exception as e:
                text_label_i =  f'第{num}个图像{image_i}标注失败&&  ---------- {e}     \n'

            w_all_text_label.append(text_label_i)
            w_all_text_label_dict[image_i] = text_label_i
            w_all_text_label_dict_i[image_i] = text_label_i
            json.dump(w_all_text_label_dict_i,f2,indent=4,ensure_ascii=False)
            if num % 10 == 0:
                
                print(text_label_i,)#'-->',image_i_info['image_event_mention'])
            num += 1