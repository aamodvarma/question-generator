import json
from tqdm import tqdm

name = "MultiFill_20241002_2339"
with open(f"./generated_files/{name}.json") as f:
    questions = json.load(f)
formatted_questions = {}
fq = []
i = 0;
for chapter in tqdm(questions):
    for section in questions[chapter]:
        for q in questions[chapter][section]:
            formatted_response = f"""
                \\textbf {{Question: {i}}} {q['question']}
                \\textbf{{Answer:}} {q['answer']}

                \\textbf{{Explanation:}} {q['explanation']}
                \\vspace{{0.5cm}} 
            """
            fq.append(formatted_response)

fff = ''.join(fq[:])
f = open("problems/problemset.tex", "r")
p = f.read()
part = list(p.rpartition("\\vspace{1cm}"))
final = ''.join(part[0:2])
final = final + fff + part[2]
f = open(f"problems/{name}.tex", "w")
f.write(final)
f.close()
