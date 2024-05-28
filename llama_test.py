import ollama
import json

definition = "The dot product of vectors u=〈u1,u2,u3〉u=〈u1,u2,u3〉 and v=〈v1,v2,v3〉v=〈v1,v2,v3〉 is given by the sum of the products of the components\nu·v=u1v1+u2v2+u3v3.u·v=u1v1+u2v2+u3v3.\n(2.3)"


prompt_question = f"""
    You are a professional math curriculum developer now. Your goal is to develop true and false questions for multivariable calculus. To do this you will take a given definition and convert that into a true and false question.
    
    Definition:
    {definition}
    
    Your goal is to convert this definition into a conceptual true or false question without the answer.

    It is important to make sure that the quesiton is a conceptual question.

    Make sure to use LaTeX for the individual terms you want to represent, make sure that you only use the following delimiters, $ $ or \\( \\). 

    Your final output should just be the true or false question and nothing else."""


response = ollama.chat(model='llama3:text', messages=[
  {
    'role': 'user',
    'content': prompt_question,
  },
])
question = (response['message']['content'])

