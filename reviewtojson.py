import pathlib
import os
import time
from tqdm.notebook import tqdm
import json
from datetime import datetime
import re



file_location = "/home/ajrv/Projects/MathCurDev/question-generator/data/reviewed/Multi/MultivariableCalculus/"



questions = {}


for chapter in os.scandir(file_location):
    chapter_name = chapter.name
    chapter_location = file_location + chapter_name + "/"
    questions[chapter_name] = {}
    for section in os.scandir(chapter_location):
        section_name = (section.name);
        section_location = chapter_location + section_name + "/"
        questions[chapter_name][section_name] = []

        q = len([f for f in os.scandir(section_location)])
        for i in range(q):
            question_location = section_location + str(i + 1) + ".tex"
            with open(question_location, "r") as f:
                latex = f.read();
                question = re.search(r"\\item\s+(.*?)(?=\\ifnum)", latex, re.DOTALL).group(1).strip()
                answer = re.search(r"Answer: (.*?)(?= )", latex, re.DOTALL).group(1).strip()
                explanation = re.search(r"Explanation: (.*?)(?=}\s+\\fi)", latex, re.DOTALL).group(1).strip()
                grouped = {"question":question, "answer":answer, "explanation":explanation}
                questions[chapter_name][section_name].append(grouped)

with open("reviewed.json", "w") as f:
    json.dump(questions, f, indent=4);
