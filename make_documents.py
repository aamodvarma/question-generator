import os
from pylatexenc.latexencode import unicode_to_latex
import json

questions = []
with open("./batches/batch_responses/tf_multivar-del-newline.jsonl", "r") as file:
    for line in file:
        json_object = json.loads(line)
        custom_id = json_object['custom_id'].split('|')
        q = json_object['response']['body']['choices'][0]["message"]["content"]
        q = q.replace("`", "").replace("json", "").replace("\n", "").replace("\\", "\\\\")
        q = q[q.find("{"):]
        q = q.replace(",}", "}")
        try:
            json_question = json.loads(q)
        except:
            print(q)
            break
        json_question['chapter'] = custom_id[0]
        json_question['section'] = custom_id[1]
        json_question['number'] = custom_id[2]
        questions.append(json_question)

all_questions =  dict()
for q in questions:
    chapter = q['chapter']
    section = q['section']
    quest = q['question'].replace("\\\\", "\\")
    try:
        explanation = q['explanation'].replace("\\\\", "\\")
    except:
        continue;
    generated_question = f"""\\item {quest.replace("True or False:", "").strip()}
    
    \\ifnum \\Solutions=1 {{\\color{{EmphBlue}} Answer: {q['answer']} \\\\ Explanation: {explanation}}}
    \\fi"""

    if (chapter not in all_questions):
        all_questions[chapter] = dict()
    if (section not in all_questions[chapter]):
        all_questions[chapter][section] = []
    all_questions[chapter][section].append(generated_question)
        

location = "./generated_files/MultivariableCalculus/"
i = 0;
for chapter in all_questions:
    i+=1;
    # chapter_directory = location + f"Chapter {i}: " + chapter + "/"
    chapter_directory = location + f"Chapter{i}/"
    if (not os.path.exists(chapter_directory)):
        os.mkdir(chapter_directory)
    for section in all_questions[chapter]:
        path = chapter_directory + section + ".tex"
        section_title = ' '.join(section.split("-")[2:]).title()
        joined_questions = ('\n'.join(all_questions[chapter][section]))
        with open(path, "w") as f:
            latex = "\\section{" + section_title + "}" + f"""
                \\begin{{enumerate}}
                {unicode_to_latex(joined_questions, non_ascii_only=True)}
                \\end{{enumerate}}
                """
            f.write(latex)
i = 0
for a in all_questions:
    i+=1
    print("\\chapter{" + a + "}")
    for b in all_questions[a]:
        print("\\input{Chapter" + str(i) + f"/{b}" + "}")
