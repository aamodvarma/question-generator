# question-generator
This repository has code to generate questions from extracted definitions and theorems using GPT-4o. The process includes extracting definitions, generating questions, and storing them in a json file. 

Definitions/theorems can be extracted from various sources. This repository has code for (to be expanded),

1. OpenStax Textbooks
2. Lecture Notes

The extracted information is then formatted into a JSON file with specific sections and sub-sections.

GPT-4o is used to generate questions. A prompt is created with a definition and a batch is created with all the prompts. The data received back from GPT-4o is then formatted and stored in a JSON file.
