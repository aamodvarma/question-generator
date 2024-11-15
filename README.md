# question-generator

This repository has code to extract, generate and create question banks and exams.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
  - [Cloning the Repository](#cloning-the-repository)
  - [Setting Up the Conda Environment](#setting-up-the-conda-environment)
- [Usage](#usage)




## Requirements
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html): Ensure you have Conda installed. If not, you can install it by following the official instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

## Installation
### Cloning the Repository
First clone the repository
```
git clone https://github.com/aamodvarma/question-generator
cd question-generator
```
### Setting Up the Conda Environment
To setup the conda environment run, 
```
conda env create -f environment.yml
```
Run the following to activate the environment,
```
conda activate question-generator
```


## Usage
To use the scripts in here you need an OpenAI access key. Once you get your access key run,

```
export OPENAI_API_KEY="your_api_key_here"
```

There are three main things you can do,
1. Extract Questions
2. Generate Question 
3. Make Documents

### Extract Questions
You can extract questions from different sources, mainly from openstax and different exams. 

`extract.py` has two arguments, 
1. `type`: The type of our source. This could be either `openstax` or `exam`.
2. `subject`: This is the different subjects that are supported. Currently we support, `linear`, `multi` and `diffeq`.

To extract questions from openstax for linear you can run, 
```
python3 ./extract.py --type openstax --subject linear
```

### Batch Generation
Batch generation is used to generate questions according to your needs. Currently two main types of generation is supported, fill in the blanks and question bank. 

`batch_generator.py` takes in two arguments, 
1. `file`: Location to the file with the extracted questions.
2. `type`: Type of generation, either `fill` or `definitions`

For instance to generate Linear Algebra Exams you can run the following command, 

```
python3 ./batch_generator.py --file ./data/LinearFill.json --type fill
```


### Document Creation

Once the new questions are generated they are stored in the `./generated_files/` directory. Now we can use these to generate Latex files for these questions.

`make_documents.py` takes in two arguments, 

1. `type`: Type of document to generate. This could be either `book` or `exam`
2. `file`: Location to the file with the generated questions.

To generate a Linear Algebra exam from the previously generated linear fill in the blanks you can run, 
```
python3 ./make_documents.py --file ./generated_files/{generated_file}.json --type exam
```



