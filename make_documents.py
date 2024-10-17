import os
import re
from pylatexenc.latexencode import unicode_to_latex
import json

# questions = []
# with open("./batches/batch_responses/tf_multivar-del-newline.jsonl", "r") as file: for line in file: json_object = json.loads(line)
#         custom_id = json_object['custom_id'].split('|')
#         q = json_object['response']['body']['choices'][0]["message"]["content"]
#         q = q.replace("`", "").replace("json", "").replace("\n", "")
#         q = q[q.find("{"):]
#         q = q.replace(",}", "}")
#         try:
#             json_question = json.loads(q)
#         except:
#             print(q)
#             break
#         json_question['chapter'] = custom_id[0]
#         json_question['section'] = custom_id[1]
#         json_question['number'] = custom_id[2]
#         questions.append(json_question)

# all_questions =  dict()
# for q in questions:
#     chapter = q['chapter']
#     section = q['section']
#     quest = q['question'].replace("\\\\", "\\")
#     try:
#         explanation = q['explanation'].replace("\\\\", "\\")
#     except:
#         continue;
#     generated_question = f"""\\item {quest.replace("True or False:", "").strip()}
    
#     \\ifnum \\Solutions=1 {{\\color{{EmphBlue}} Answer: {q['answer']} \\\\ Explanation: {explanation}}}
#     \\fi"""

#     if (chapter not in all_questions):
#         all_questions[chapter] = dict()
#     if (section not in all_questions[chapter]):
#         all_questions[chapter][section] = []
#     all_questions[chapter][section].append(generated_question)
        

def book():
    name = "2551_TF_Q_20240911_2257"

    with open(f"./generated_files/{name}.json") as f:
        all_questions = json.load(f)

    for c in all_questions:
        for s in all_questions[c]:
            for a in range(len(all_questions[c][s])):
                q= all_questions[c][s][a]
                text = f"""\\item {q['question'].replace("True or False:", "").strip()}
                    
                    \\ifnum \\Solutions=1 {{\\color{{EmphBlue}} Answer: {q['answer']} \\\\ Explanation: {q['explanation']}}}
                    \\fi"""
                all_questions[c][s][a] = text



    location = f"./generated_files/{name}/"
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



def exam():
    latex_commands = ['nabla', 'noindent', 'newline', 'norm', 'nonumber', 'neq', 'nexists']
    latex_commands = [x[1:] for x in latex_commands]
    name = "./generated_files/LinearFill_20240919_1028.json"
    with open(name, "r") as f:
        questions = json.load(f)

    for exam in questions:
        location = f"./generated_files/LinearFill/202408/{exam}/"
        for number in questions[exam]:
            print(number)
            q_list = []
            count = 1
            for q in questions[exam][number]:
                try:
                    pattern = r'\\n(?!' + '|'.join(latex_commands) + r')'
                    pattern_standalone = r'(?<!\\)\n(?!' + '|'.join(latex_commands) + r')'  
                    ques = re.sub(pattern, r'\\ ', q["question"])
                    # ques = re.sub(pattern_standalone, r'\\\\', ques)


                    ans = re.sub(pattern, r'\\ ', q["answer"])
                    # ans = re.sub(pattern_standalone, r'\\\\ ', ans)

                    pattern = r'(?<=[a-zA-Z])\\\\|\\\\(?=[a-zA-Z])'

                    ques = re.sub(pattern, r'\\', ques)

                    q_tex = fr"""
    \ifnum \Version={count}
        \part {ques.replace("\\part", "").strip()}

        \ifnum \Solutions=1 {{\color{{DarkBlue}} \textit{{Solutions:}} 

        {ans.replace("\\part", "").strip()}

        }}
        \else
        \fi        
    \fi"""
                        
                    count+=1;
                    print(q_tex)
                    q_list.append(q_tex)
                except:
                    print('E')
                    continue
            with open(location+number, "w") as f:

                f.write("\n\n".join(q_list))





if __name__ == "__main__":
    exam()
