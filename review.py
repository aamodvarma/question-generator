import pathlib
import os
import time
from tqdm.notebook import tqdm
import json
from datetime import datetime


# file = "MultiOpenStax_Definitions_20240819_1328"
file = "LinearLecNotes_Definitions_20240825_1911"
chapter_name = "LinearAlgebra"


now = datetime.now()
unique_id = now.strftime("%Y%m%d_%H%M")

with open(f'./generated_files/{file}.json', "r") as f:
    data = json.loads(f.read());

x = [['', 'Location', 'Status', 'Formatting', 'Accuracy']]

content_folder = chapter_name + "_" + unique_id
if (not os.path.exists(content_folder)):
    os.mkdir("generated_files/review/" + content_folder)

index = 1;
for chapter in data:
    print("\\chapter{" + chapter + "}")
    chapter_folder = f"generated_files/review/{content_folder}/"  + chapter
    if (not os.path.exists(chapter_folder)):
        os.mkdir(chapter_folder)

    for section in data[chapter]:
        print("\\section{" + section + "}")
        print("\\begin{enumerate}")

        section_folder = chapter_folder + '/' + section
        if (not os.path.exists(section_folder)):
            os.mkdir(section_folder)

        i = 1;
        for question in data[chapter][section]:
            print("\\input{" + f"{chapter_name}/{chapter}/{section}/{i}" + "}")


            generated_question = f"""\\item {question['question'].replace("True or False:", "").strip()}
            
            \\ifnum \\Solutions=1 {{\\color{{EmphBlue}} Answer: {question['answer']} \\\\ Explanation: {question['explanation']}}}
            \\fi"""

            question_folder = section_folder + '/' + str(i) + '.tex'
            with open(question_folder, 'w') as f:
                f.write(generated_question)

            row = [index, question_folder, '0', '0', '0']
            x.append(row)

            i+=1
            index+=1;

        print("\\end{enumerate}")

import csv
with open(f"generated_files/review/{content_folder}/review.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(x)

