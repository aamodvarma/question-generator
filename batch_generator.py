from openai import OpenAI
import argparse
import pathlib
import textwrap
from yaspin import yaspin
import os
import time
import random
from tqdm.notebook import tqdm
import time
import json
from datetime import datetime

def initialize_client():
    client = OpenAI(
      organization='org-MiSTdq8wllMVuvQ1Es4GrHNX',
      project='proj_rO8d3QjByeL5WcL1nApaiy5B',
    )
    return client


def get_data(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def get_json(content_id, prompt):
    sample = {"custom_id": f"{content_id}",
              "method": "POST",
              "url": "/v1/chat/completions",
              "body": {"model": "gpt-4o",
                       "messages": [{"role": "user", 
                                     "content": prompt}],
                       "max_tokens": 1500,
                       "temperature": 1,
                       "top_p": 1,
                       "frequency_penalty":0,
                       "presence_penalty":0}}
    return sample


def definitions(data):
    contents = []
    for chapter, sections in (data.items()):
        for section, section_definitions in (sections.items()):
            i = 1;
            for q in (section_definitions):
                content_id = (chapter+"|"+section+"|"+str(i))
                i+=1
                dec = random.choice(["True", "False"])
                message = fr"""I will give you a true/false multivariable calculus question. Your job is to transform this question into a new one. If it has numerical values, slightly change them but keep the accuracy correct. You must also give an explanation that is concise but includes the main concepts used. Use examples to illustrate these concepts. Use latex as required while only using the "$" delimiter. Do not ever create a newline in your output. Make sure the final output is in JSON format with three fields, "question", "answer" and "explanation". Question: {q['question'].strip()}. The answer is {q['answer'].strip()}. In your generated question the answer should be {dec}"""
    
                contents.append(get_json(content_id, message))
    return contents
def fill_in_the_blanks(data):
    contents = []
    for exam, questions in (data.items()):
        for name, q in questions.items():
            i = 1
            for a in q:
                content_id = exam+"|" + name + "|" + str(i)
                i+=1;
                message = fr"""I will give you a question and answer, your job is to create another question similar to this. The new questions should be similar but not the same. Your new question should have different values, structure etc. But all in all should test the same concept. Make sure to be more creative in how you test the concept. 
                Here is the question, Question: {a["question"]}\n Answer: {a["answer"]}. 
                Use latex as required while only using the "$" delimiter. Do not ever create a newline in your output. Make sure the final output is in JSON format with two fields, "question" and "answer."
                """
                contents.append(get_json(content_id, message))
    return contents

def create_content_file(input_file, data):
    now = datetime.now()
    unique_id = now.strftime("%Y%m%d_%H%M")
    input_file_name = input_file.split("/")[-1].split('.')[0]
    content_file = input_file_name + "_" + unique_id
    return content_file

def create_batch(client, data, content_file, generation_type):
    if (generation_type == "definitions"):
        contents = definitions(data)
    elif (generation_type == "fill"):
        contents = fill_in_the_blanks(data)
    else:
        return None
    with open(f'batches/batch_files/{content_file}.jsonl', 'w') as f:
        for record in contents:
            json_record = json.dumps(record)
            f.write(json_record + '\n')
    batch_input_file = client.files.create(
      file=open(f"batches/batch_files/{content_file}.jsonl", "rb"),
      purpose="batch"
    )
    batch_input_file_id = batch_input_file.id

    batch = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
          "description": f"{content_file}"
        }
    )
    batch_id = batch.id
    return batch_id

def poll_batch_result(client, batch_id):
    with yaspin(text="Waiting for batch completion...", color="cyan") as spinner:
        while True:
            batch = client.batches.retrieve(batch_id)
            status = batch.status
            if status == 'completed':
                spinner.ok("✔")
                return batch
            elif status == 'failed':
                spinner.fail("✖")
                raise Exception("Batch processing failed")
            time.sleep(5)

def save_generated_content(batch_id, content_file, client):
    batch = client.batches.retrieve(batch_id)
    output_file_id = batch.output_file_id
    content = client.files.content(output_file_id)
    with open(f"./batches/batch_responses/{content_file}.jsonl", "w") as f:
        f.write(content.content.decode("utf-8"))


def clean_generated_content(content_file, generation_type):
    json_question = {}
    questions = []
    with open(f"./batches/batch_responses/{content_file}.jsonl", "r") as file:
        for line in file:
            json_object = json.loads(line)
            custom_id = json_object['custom_id'].split('|')
            q = json_object['response']['body']['choices'][0]["message"]["content"]
            q = q.replace("`", "").replace("json", "").replace("\n", "")
            q = q.replace("\\\\", "\\").replace("\\", "\\\\")
            try:
                json_question = json.loads(q)
            except:
                q = q.replace("\\", "\\\\")
                print(q)
                try:
                    json_question = json.loads(q)
                except:
                    pass
            json_question['chapter'] = custom_id[0]
            json_question['section'] = custom_id[1]
            json_question['number'] = custom_id[2]
            questions.append(json_question)

    all_questions =  dict()
    for q in questions:
        chapter = q['chapter']
        section = q['section']
        if (chapter not in all_questions):
            all_questions[chapter] = dict()
        if (section not in all_questions[chapter]):
            all_questions[chapter][section] = []
        try:
            if(generation_type == "fill"):
                all_questions[chapter][section].append({"question" : q['question'], "answer" : q['answer']})
            elif (generation_type == "definitions"):
                all_questions[chapter][section].append({"question" : q['question'], "answer" : q['answer'], "explanation" : q["explanation"]})
        except:
            continue

    with open(f"./generated_files/{content_file}.json", "w") as file:
        json.dump(all_questions, file)

    print(f"Generated file saved at: ./generated_files/{content_file}.json")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Batch Generator',
                    description='Generates Questoins')
    

    parser.add_argument('--file', type=str, required=True, help="The path to input file")
    parser.add_argument('--type', type=str, required=True, choices=["fill", "definitions"], help="The type of generation")

    args = parser.parse_args()


    input_file = args.file
    generation_type = args.type

    # print(input_file)
    # print(generation_type)
    client = initialize_client()
    data = get_data(input_file)
    content_file = create_content_file(input_file, data)
    batch_id = create_batch(client, data, content_file, generation_type)
    batch = poll_batch_result(client,batch_id)
    save_generated_content(batch_id, content_file, client)
    clean_generated_content(content_file, generation_type)
