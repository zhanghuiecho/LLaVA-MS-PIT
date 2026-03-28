import os
from openai import OpenAI
import json
import base64

verbs= ['floating','leading','cheering','restraining','mourning','tugging','signing','weighing','sleeping','falling','gambling','pricking', 'bulldozing','rowing', 'taxiing', 'frisking', 'fetching', 'boarding', 'tackling', 'unpacking', 'calling', 'loading', 'flaming', 'discussing', 'socializing', 'deflecting', 'ramming', 'congregating', 'lifting', 'handcuffing', 'arresting', 'butting', 'unloading', 'ejecting', 'scolding', 'towing', 'writing', 'slapping', 'punching', 'disembarking', 'boating', 'skidding', 'destroying', 'carrying', 'detaining', 'subduing', 'talking', 'burying', 'hauling', 'buying', 'paying', 'hitting', 'shooting', 'shaking', 'crashing', 'attacking', 'aiming', 'dragging', 'landing', 'wheeling', 'chasing', 'gathering', 'marching', 'launching', 'rafting', 'striking', 'steering', 'catching', 'communicating', 'saluting', 'burning', 'telephoning', 'parading', 'colliding', 'confronting', 'phoning', 'apprehending', 'erupting', 'protesting', 'piloting']
verbs = list(set(verbs))
def extract_filename_prefix(file_path):
    filename = os.path.basename(file_path)       
    name_without_ext = os.path.splitext(filename)[0] 
    return name_without_ext.split('_')[0]       


def get_all_files_recursive(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)
    return file_paths

# 使用示例
folder = r"D:\mmee_project-new\data\swig_event\picture"  
all_files = get_all_files_recursive(folder)
print("找到", len(all_files), "个文件：")

all_files_new = []
for f in all_files:  # 只显示前5个示例
    verb_i = extract_filename_prefix(f)
    if verb_i in verbs:
        all_files_new.append(f)
len(all_files_new)


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

client = OpenAI(
    base_url='xxxx',
    api_key='sk-xxxxx'
)
prompt= """Determine if this image belongs to one of the following event types. If it does, select the event type that most closely matches the information expressed in the image. Otherwise, simply output 'No Event'. Do not produce any additional text unrelated to the task. The event types and their definitions are as follows:
{
    "Movement.Transport": "A TransportEvent occurs whenever an Artifact (Weapon or Vehicle) or a Person is moved from one Place(GPE, Facility, Location) to another.",
    "Conflict.Attack": "An ATTACK Event is defined as a violent physical act causing harm or damage. Attack Events include any\nsuch Event not covered by the Injure or Die subtypes, including Events where there is no stated agent.",
    "Conflict.Demonstrate": "A DEMONSTRATE Event occurs whenever a large number of people come together in a public area to protest or demand some sort of official action. Demonstrate Events include, but are not limited to, protests, sit-ins, strikes, and riots.",
    "Justice.Arrest-Jail": "A JAIL Event occurs whenever the movement of a PERSON is constrained by a state actor (a GPE, its ORGANIZATION subparts, or its PERSON representatives).",
    "Contact.Phone-Write": "A PHONE-WRITE Event occurs when two or more people directly engage in discussion which does not take place ‘face-to-face’.",
    "Contact.Meet": "A MEET Event occurs whenever two or more Entities come together at a single location and interact with one another face-to-face.",
    "Life.Die": "A DIE Event occurs whenever the life of a Person Entity ends. Die Events can be accidental, intentional or self-inflicted",
    "Transaction.Transfer-Money": "TRANSFER-MONEY Events refer to the giving, receiving, borrowing, or lending money when it is not in the context of purchasing something.",
}
"""

new_swig = {}
with open(f'new_swig_{n}.txt', 'w', encoding='utf-8') as file:
    for i in all_files_new[1632:]:
        n=n+1
        base64_image = image_to_base64(i)
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
        i_name = os.path.basename(i)
        new_swig[i_name] = content
        dict_i = {}
        dict_i[i_name] = content
        
        line_data = {i_name: content}
            
        file.write(f'第{n}个图像处理完成    ' + str(line_data) + '\n')
        