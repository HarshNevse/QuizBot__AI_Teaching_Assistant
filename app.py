from langchain_ollama import ChatOllama
import os
from docx import Document
import PyPDF2
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = ChatOllama(
            model = "llama3.1:8b",
            temperature = 0.12,
            num_predict = 1000,
            num_gpu = 2
            )


def upload_files(file_paths: list) -> str:
    '''Function to read and store multiple files uploaded by the user.
    Supports .txt, .docx, and .pdf files.
    
    Args: file_paths (list): List of file paths to be uploaded.
    
    Returns: str: All extracted content from the files, stored in a single string.
    '''

    print(f"Upload function called with file list: {file_paths}", flush = True)
    all_data = ""  # Variable to store content from all files

    for file_path in file_paths:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            # For .txt files
            if file_extension == '.txt':
                try:
                    with open(file_path, 'r', encoding='utf-8-sig') as file:  # Handle special characters in .txt
                        data = file.read()
                    all_data += f"\n--- Content from {file_path} ---\n{data}\n"
                except UnicodeDecodeError as e:
                    all_data += f"\n--- Error reading {file_path}: Encoding issue - {str(e)}\n"
            
            # For .docx files
            elif file_extension == '.docx':
                try:
                    document = Document(file_path)
                    data = "\n".join([para.text for para in document.paragraphs])
                    all_data += f"\n--- Content from {file_path} ---\n{data}\n"
                except Exception as e:
                    all_data += f"\n--- Error reading {file_path}: {str(e)}\n"
            
            # For .pdf files
            elif file_extension == '.pdf':
                try:
                    with open(file_path, 'rb') as file:
                        reader = PyPDF2.PdfReader(file)
                        data = ""
                        for page in reader.pages:
                            data += page.extract_text() or ''  # Handle missing text gracefully
                    all_data += f"\n--- Content from {file_path} ---\n{data}\n"
                except Exception as e:
                    all_data += f"\n--- Error reading {file_path}: {str(e)}\n"
            
            else:
                all_data += f"\n--- File '{file_path}' has an unsupported file type. Only .txt, .docx, and .pdf are supported.\n"

        except FileNotFoundError:
            all_data += f"\n--- Error: The file '{file_path}' does not exist.\n"
        
        except Exception as e:
            all_data += f"\n--- An error occurred with file '{file_path}': {str(e)}\n"

    print(f'Finished uploading.', flush=True)

    return all_data


def ask(data, num_quest=6, num_ops=4, num_diff=1):
    diff_level = {1:'Easy', 2: 'Medium', 3: 'Tough'}
    diff = diff_level[num_diff]
    print(f"\nAsk function called with parameters num_quest={num_quest}, num_ops={num_ops}, num_diff={num_diff} which translates to : {diff}")

    from langchain.prompts import PromptTemplate
    fact_extraction_prompt = PromptTemplate( input_variables=['text_input'], 
                                        template='''Input text: {text}\nExtract relevant information from the given text, don't create information out of nowhere and return your complete and detailed summary of the given text. MAKE SURE to give equal importance to each file data so that your summary has equal weightage of all topics in the data.''')
    
    mcq_generator_prompt = PromptTemplate( input_variables=['text_input'], 
                                        template='''Input text: {text}\n''' + f'Based on information of the input text, create {num_quest} multiple choice questions based on the text, give {num_ops} options per question. The difficulty level of the questions should be {diff} level. FORMATTING: 1] Make sure to generate the questions FIRST. AFTER generating all the questions, write all the answers. Example:\nQuestions:\n`generated questions`\nAnswers:\n`ordered and numbered answers to the questions`. Make sure the correct option number always fluctuates.') 

    chain = fact_extraction_prompt | model | mcq_generator_prompt | model

    
    r = chain.invoke(data)

    print('Agent finished processing.', flush = True)
    return r.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_mcqs', methods=['POST'])
def generate_mcqs():
    files = request.files.getlist('files')
    num_quest = int(request.form.get('num_quest'))
    num_ops = int(request.form.get('num_ops'))
    difficulty = request.form.get('difficulty')

    num_diff_map = {'easy': 1, 'medium': 2, 'hard': 3}
    num_diff = num_diff_map.get(difficulty.lower(), 1)

    saved_file_paths = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            saved_file_paths.append(file_path)

    combined_data = upload_files(saved_file_paths)
    result = ask(combined_data, num_quest, num_ops, num_diff)

    return jsonify({'mcqs': result})

if __name__ == '__main__':
    app.run(debug=True, use_reloader = False)
