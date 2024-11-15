import os
import argparse
import re
from pylatexenc.latexencode import unicode_to_latex
import json

        

def book(file):
    with open(file) as f:
        all_questions = json.load(f)

    name = file.split('/')[-1].split(".")[0]
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
        # print("\\chapter{" + a + "}")
        for b in all_questions[a]:
            print("\\input{Chapter" + str(i) + f"/{b}" + "}")



def exam(name):
    latex_commands = ['nabla', 'noindent', 'newline', 'norm', 'nonumber', 'neq', 'nexists']
    latex_commands = [x[1:] for x in latex_commands]
    # name = "./generated_files/DiffEqFill_20241110_1727.json"
    with open(name, "r") as f:
        questions = json.load(f)

    for exam in questions:
        location = f"./generated_files/DiffEqFill/CurrentSemester/{exam}/"
        for number in questions[exam]:
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

                    # replace "char\\char" with "char\char"
                    pattern = r'(?<=[a-zA-Z])\\\\|\\\\(?=[a-zA-Z])'
                    ques = re.sub(pattern, r'\\', ques)
                    ans = re.sub(pattern, r'\\', ans)

                    # replace numbner/number with number // number
                    ques = re.sub(r'(\d+)\\(\d+)', r'\1 \\\\ \2', ques)
                    ans = re.sub(r'(\d+)\\(\d+)', r'\1 \\\\ \2', ans)

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
                    # print(q_tex)
                    q_list.append(q_tex)
                except:
                    continue
            with open(location+number, "w") as f:
                f.write("\n\n".join(q_list))





if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Batch Generator',
                    description='Generates Questoins')
    parser.add_argument('--type', type=str, required=True, choices=["book", "exam"], help="The type of generation")
    parser.add_argument('--file', type=str, required=True, help="File location")
    args = parser.parse_args()
    if (args.type == "book"):
        book(args.file);
    elif(args.type == "exam"):
        exam(args.file)

