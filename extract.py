import pathlib
import json
import re
import textwrap
import os
import time
import requests
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup
from IPython.display import display
from IPython.display import Markdown

def extract_chapters(url):
    all_urls = dict();
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = soup.find_all('li', attrs={'data-type': 'chapter'})
    for url in urls:
        chapter_name = url.find_all('span', class_='os-text')[0].text.strip()
        chapter_links = [];
        links = url.find_all('ol')[0].find_all('li')
        for a in (links):
            subtitle = a.find_all('a')[0].get("href")
            if ('1' <= subtitle[2] <= '9'):
                chapter_links.append('https://openstax.org/books/calculus-volume-3/pages/'+ subtitle)
        all_urls[chapter_name] = chapter_links
    return all_urls

def extract_openstax():
    all_urls = dict();
    all_urls = extract_chapters('https://openstax.org/books/calculus-volume-3/pages/1-introduction')
    all_chapter_definitions = dict()
    for name, urls in tqdm(all_urls.items()):
        subsection_dict = dict()

        for url in tqdm(urls):
            subsection_name = url[51:]
            subsection_definitions = []

            response = requests.get(url)
            response.raise_for_status()  
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            definition_difs = soup.find_all('div', class_='ui-has-child-title')
            for element in definition_difs:
                if (len(element) == 2):
                    header_name = element.find_all()[0].text.strip()
                    if (header_name != "Definition" and header_name.find("Theorem") != 0):
                        continue;
                    definition = element.find_all('div', class_='os-note-body')
                    subsection_definitions.append(definition[0].text.strip())
            subsection_dict[subsection_name] = subsection_definitions
        all_chapter_definitions[name] = subsection_dict
    import json
    json_data = json.dumps(all_chapter_definitions, indent=4, ensure_ascii=False);
    with open('all_chapter_definitions.json', 'w') as file:
        file.write(json_data)
    count = 0
    for a,b in all_chapter_definitions.items():
        for x,y in b.items():
            print(x + "=>"+ str(len(y)))
            count+= len(y)
    print(count)

def linear_exam():
    all_questions = {}
    folder = "./data/LinearFill/202408/"
    exams = [x for x in os.listdir(folder) if x[0:4] == "Exam"]
    for exam in exams:
        all_questions[exam] = {}
        files = [x for x in os.listdir(folder + exam) if x.find("Q") != -1]
        for file in files:
            all_questions[exam][file] = []
            file_location = folder + exam + "/"+ file
            with open(file_location) as f:
                text = f.read()
                pattern = r'\\ifnum.*?\\fi'
                matches = re.findall(pattern, text, re.DOTALL)
                for match in matches:
                    # print(match)
                    pattern = r'\\Version=.(.*?)\\ifnum'
                    question_matches = re.findall(pattern, match, re.DOTALL)
                    try:
                        question = question_matches[0].strip()
                    except:
                        continue;
                    pattern = r'\\textit{Solutions.}(.*?)\\fi'
                    answer_matches = re.findall(pattern, match, re.DOTALL)
                    try:
                        answer = (answer_matches[0].strip())
                    except:
                        continue;
                    q = {"question" : question, "answer" : answer}
                    all_questions[exam][file].append(q);
    with open("./data/LinearFill.json", "w") as f:
        json.dump(all_questions, f, indent=4)


def MVCExam():
    all_questions = {}
    folder = "./data/MVCFill/202402/"
    exams = [x for x in os.listdir(folder) if x[0:4] == "Exam"]
    for exam in exams:
        all_questions[exam] = {}
        files = [x for x in os.listdir(folder + exam) if x.find("Fill") != -1]
        for file in files:
            all_questions[exam][file] = []
            file_location = folder + exam + "/"+ file
            with open(file_location) as f:
                text = f.read()
                pattern = r'\\ifnum.*?\\fi'
                matches = re.findall(pattern, text, re.DOTALL)
                for match in matches:
                    # print(match)
                    pattern = r'\\Version=.(.*?)\\ifnum'
                    question_matches = re.findall(pattern, match, re.DOTALL)
                    try:
                        question = question_matches[0].strip()
                    except:
                        continue;
                    pattern = r'\\textit{Solutions.}(.*?)\\fi'
                    answer_matches = re.findall(pattern, match, re.DOTALL)
                    try:
                        answer = (answer_matches[0].strip())
                    except:
                        continue;
                    q = {"question" : question, "answer" : answer}
                    all_questions[exam][file].append(q);
    with open("./data/MultiFill.json", "w") as f:
        json.dump(all_questions, f, indent=4)

if __name__ == "__main__":
    MVCExam()
