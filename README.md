# question-generator
Question generator is a program to generate question given definitions and theorems using GPT-4o. The process is three fold, extracting definitions, generating questions and formatting them accordingly. 

Definitions/theorems can be extracted from various sources. This repository has code for (to be expanded),

1. OpenStax Textbooks
2. Lecture Notes

The extracted information is then formatted into a json file with specific sections and sub-sections.

GPT-4o is used to generate questions. A prompt is created with a definition and a batch is created with all the prompts. The data received back from GPT-4o is then formatted and stored in a json file.

Lastly the generated questions are formatted according to the specific usecase. This repository has (or will have) code for,

1. WeBWorK
2. Canva
3. Question Bank (Book)







