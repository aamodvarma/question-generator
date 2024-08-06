import pathlib
import textwrap
import os
import time
import requests
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup
from IPython.display import display
from IPython.display import Markdown
all_urls = dict();
def extract_chapters(url):
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
