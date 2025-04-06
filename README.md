# QuizBot
QuizBot is an Assistant to the teacher. Just upload your teaching material and it creates customizable question sets based on teacher-selected difficulty, number of questions, and options.

## Knowledge
* **LLMChain** : Chain to run queries against an LLM.​
* **Prompt templates** : help to translate user input and parameters into instructions for a language model. This can be used to guide a model's response, helping it understand the context and generate relevant and coherent language-based output.​
* Prompt Templates take as input a dictionary, where each key represents a variable in the prompt template to fill in.​

## Workflow

* File Upload
  
  Teacher uploads study material. Set parameters for number of questions, options and difficulty level.
* ![Screenshot 2025-04-06 210755](https://github.com/user-attachments/assets/4dc6255e-3f4e-4a26-bb9b-11bd6d59c54e)
  
  Tells the LLM to summarize the entire content to make reasoning easier and avoid Context Length crashes.
* ![Screenshot 2025-04-06 210957](https://github.com/user-attachments/assets/78529f70-5fce-4123-a79c-c056095bab91)

  Tells the LLM to generate MCQ's based on the summary and keeping in mind the parameters set by the teachers.

* Chain Visualization

  ![Editor _ Mermaid Chart-2025-04-06-155428](https://github.com/user-attachments/assets/6992f253-1644-4eed-963f-a284c3a49f94)


## Features

- Upload multiple files (`.txt`, `.pdf`, `.docx`)
- Automatically summarizes uploaded content
- Generates MCQs based on:
  - Number of questions
  - Number of options per question
  - Difficulty level (Easy, Medium, Hard)
- Uses LangChain prompt chaining with LLM
- Clean frontend interface:
  - Markdown-rendered output
  - Separate output sections for Questions and Answers
  - Copy-to-clipboard functionality for both sections
 
## Video Demo

[screen-capture.webm](https://github.com/user-attachments/assets/956ccb62-4ec6-44f3-8f20-df752cfa8ef9)


## Requirements

Install the required Python packages:

```bash
pip install flask python-docx PyPDF2 langchain langchain_community
```
You must also have `Ollama` installed and running a compatible local model (such as llama3.1:8b)

## Technologies Used
* `LangChain`
* `Ollama` LLM (e.g., llama3)
* `Flask`
* `marked.js` for Markdown rendering in the frontend

## Author
Developed by Harsh, AI/ML Enthusiast.
