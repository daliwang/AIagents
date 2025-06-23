from openai import OpenAI 
import os

from IPython.display import Image, display, Audio, Markdown
import base64

from flask import Flask, request, render_template_string, redirect, url_for, session, send_from_directory
import re

## Set the API key and model name
MODEL_4o="gpt-4o-mini"
MODEL_35="gpt-3.5-turbo"
MODEL_4="gpt-4.0-turbo"

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

#def general35(instruction):
#    completion = client.chat.completions.create(
#      model=MODEL_35,
#      messages=[
#        {"role": "system", "content": "You are a helpful assistant."}, # <-- This is the system message that provides context to the model
#       {"role": "user", "content": f"Please follow these {instruction} to provide answers"}  # generate a response
#      ]
#    )
#
#    return (completion.choices[0].message.content)


def general4(instruction):
    completion = client.chat.completions.create(
      model=MODEL_4o,
      messages=[
        {"role": "system", "content": "You are a helpful assistant."}, # <-- This is the system message that provides context to the model
       {"role": "user", "content": f"Please follow these {instruction} to provide answers"}  # generate a response
      ]
    )

    return (completion.choices[0].message.content)


'''
def email(text):
    completion = client.chat.completions.create(
      model=MODEL_35,
      messages=[
        {"role": "system", "content": "You are a helpful assistant. \\
         Your job is to refine these sentences from user: {text} \\
        meticulously examine the grammar, and make them sound like they were written by a native \\
        speaker in a conversational tone. Kindly enumerate the particular modifications made to \\
        the original text, one by one. Please use a similar number of words."}, # <-- This is the system message that provides context to the model
       {"role": "user", "content": f"Here are these {text}"}  # generate a response
      ]
    )

    return (completion.choices[0].message.content)
'''

def email(text):
    instructions = [
        "1. Your job is to refine the sentences provided by the user meticulously.",
        "2. Examine the grammar and aim to make the text sound native and conversational.",
        "3. Enumerate the specific modifications made to the original text in detail.",
        "4. Please provide explanations in a conversational and clear manner, using a similar number of words."
    ]

    completion = client.chat.completions.create(
        model=MODEL_35,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. \
            Here are the instructions for enhancing the user's sentences:",
            "content": "\n".join(instructions)},
            {"role": "user", "content": f"Here are these {text}"}
        ]
    )

    return (completion.choices[0].message.content)

def paper(text):
    instructions = [
        "1. It is your responsibility to restructure these sentences in the text.", 
        "2. scrutinize the grammar, and refine them.",
        "3. resemble those composed by native-speaking academic researchers." ,
        "4. Kindly enumerate the precise modifications made to the original text, while maintaining a similar word count.",
        "5: If possible, please also track all the changes." 
    ]

    completion = client.chat.completions.create(
        model=MODEL_35,
        messages=[
            {"role": "system", "content": "You are a helpful researcher. \
            Here are the instructions for enhancing the user's sentences:",
            "content": "\n".join(instructions)},
            {"role": "user", "content": f"Here are these {text}"}
        ]
    )

    return (completion.choices[0].message.content)

#======= TextFromImage ========

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def Image2Text(IMAGE_PATH):
    # Preview image for context
    display(Image(IMAGE_PATH))

    base64_image = encode_image(IMAGE_PATH)

    response = client.chat.completions.create(
        model=MODEL_4o,
        messages=[
            {"role": "system", "content": "You are a helpful assistant to help me to extract text from image using OCR and keep the same format"},
            {"role": "user", "content": [
               {"type": "text", "text": "What's the text show in the picturee?"},
               {"type": "image_url", "image_url": {
                   "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )
    return (response.choices[0].message.content)

#example:
#image="/Users/7xw/Downloads/ChristyChen_ticket.jpg"
#print(ag.Image2Text(image))


def describe_slide(image_path):
    """
    Takes an image of a PowerPoint slide and returns a description of the slide.

    Parameters:
    image_path (str): The path to the image file.

    Returns:
    str: The description of the slide.
    """
    # Preview image for context
    display(Image(image_path))

    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model=MODEL_4o,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. translate the content in this image into Chinese."},
            {"role": "user", "content": [
               {"type": "text", "text": "Please describe the content of this PowerPoint slide."},
               {"type": "image_url", "image_url": {
                   "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content


# Example usage:
# image_path = "/Users/7xw/Downloads/slide.png"
# print(describe_slide(image_path))


'''

import warnings
warnings.filterwarnings('ignore')

#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    #llm_model = "gpt-4.0"
    llm_model = "gpt-4"

#from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Deal with images
import base64
import requests

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to process the image
def process_image(image_path, text):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()
    #result = response.json()
    #return response.json()['choices'][0]['message']['content']


def image2text(image_path):
    result =  process_image(image_path, "please extract the text from the image and keep the original format")
    return result['choices'][0]['message']['content']

llm = ChatOpenAI(temperature=0.0, model=llm_model)

prompt_email = ChatPromptTemplate.from_template(
"As an assistant, your job is to refine these sentences: {text} \
meticulously examine the grammar, and make them sound like they were written by a native \
speaker in a conversational tone. Kindly enumerate the particular modifications made to \
the original text, one by one. Please use a similar number of words. \
Here are the text: {text} "
)

prompt_paper = ChatPromptTemplate.from_template(
"As a researcher, it is your responsibility to restructure these sentences in the text, scrutinize the grammar, \
and refine them to resemble those composed by native-speaking \academic researchers. Kindly \
enumerate the precise modifications made to the original text, item by item, while maintaining a similar word count.\
If possible, can you also track all the changes? \
Here is the text: {text}" 
)

prompt_general = ChatPromptTemplate.from_template(
"As an assistant, please provide the answer for the instructions in {text}." 
)

prompt_code = ChatPromptTemplate.from_template(
"As a code developer, it is your responsibility to understand the purpose and algorithms descried in the text, develop \
efficient algorithm and code segment to implement these ideas. If possible, develop a unit test driver for the code and \
propose a second, less efficient implemmentation (algorithm) so that we can validate and verify the code implemenation. \
Here are the instructions and code segment:{text} "
)

prompt_coverletter = ChatPromptTemplate.from_template(
"As a job applicant, I want to write a short cover letter (200 words, two paragraphs) that shows I am a good match for the job description. \
Here are my resume and the job description and requirements:{Job_description} "
)

#prompt_imageProc = ChatPromptTemplate.from_template(
#"As an assistant, your job is to follow the instructions provided in the: {text} to process the images in the: {image_path}, and print out the #texts in instruction and image_path, and then use the {process_image} function to print out the result."
#)

email = LLMChain(llm=llm, prompt=prompt_email, verbose=False)
paper = LLMChain(llm=llm, prompt=prompt_paper, verbose=False)
code = LLMChain(llm=llm, prompt=prompt_code, verbose=False)
coverletter = LLMChain(llm=llm, prompt=prompt_coverletter)
general = LLMChain(llm=llm, prompt=prompt_general)
#imageProc = LLMChain(llm=llm, prompt=prompt_imageProc, verbose=False)

def run(*args, **kwargs):
    return general.run(*args, **kwargs)
    #return print(general.invoke(*args, **kwargs))
def email_wt(*args, **kwargs):
    return print(email.invoke(*args, **kwargs))
def paper_wt(*args, **kwargs):
    return print(paper.invoke(*args, **kwargs))
def code_wt(*args, **kwargs):
    return print(code.invoke(*args, **kwargs))
def coverletter_wt(*args, **kwargs):
    return print(coverlettter.invoke(*args, **kwargs))
#def imageProc(*args, **kwargs):
#    return print(imageProc(*args, **kwargs))

'''
'''
prompt_imageProc = ChatPromptTemplate.from_template(
"As an assistant, your job is to open and read the image, given in the {image} and process the image based on the instructions in {text}. It will need to use the built-in function 'image_process(instruction, image)', given by the user. Here are the instruction: {text} and image: {image} "
)

imageProc = LLMChain(llm=llm, prompt=prompt_imageProc, verbose=False)

def image_proc(*args, **kwargs):
    return print(imageProc.run(*args, **kwargs))



'''

#usage examples:
#instructions="Instructions: The image contains a picture of Eric when he was about 5 years one. Please look the picture and describe \
#the your impression on his ersonality"
#image_path= "/Users/7xw//Downloads/Eric4.jpg"
#result=lc.process_image(image_path, instructions)
#print(result['choices'][0]['message']['content'])

#image_path= "/Users/7xw//Downloads/question9_1.jpg"
#print(lc.image2text(image_path))

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random key in production

EMAIL_FORM = '''
<!DOCTYPE html>
<html>
<head><title>Email Grammar Refiner</title>
<style>
.copy-btn { margin-top: 5px; }
textarea[readonly] { background: #f8f8f8; }
</style>
<script>
function copyOutput() {
    var copyText = document.getElementById("output");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
}
</script>
</head>
<body>
<h2>Email Grammar Refiner</h2>
<form method="post">
<textarea name="text" rows="10" cols="80" placeholder="Paste your email here..."></textarea><br>
<input type="submit" value="Refine Email">
</form>
{% if refined %}
<h3>Refined Email:</h3>
<textarea id="output" rows="8" cols="80" readonly>{{ refined }}</textarea><br>
<button class="copy-btn" onclick="copyOutput()" type="button">Copy Refined Email</button>
{% endif %}
{% if changes %}
<h3>Change Information:</h3>
<pre>{{ changes }}</pre>
{% endif %}
<a href="/paper">Go to Paper Refiner</a>
</body>
</html>
'''

PAPER_FORM = '''
<!DOCTYPE html>
<html>
<head><title>Paper Grammar Refiner</title>
<style>
.copy-btn { margin-top: 5px; }
textarea[readonly] { background: #f8f8f8; }
</style>
<script>
function copyOutput() {
    var copyText = document.getElementById("output");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
}
</script>
</head>
<body>
<h2>Paper Grammar Refiner</h2>
<form method="post">
<textarea name="text" rows="10" cols="80" placeholder="Paste your paper text here..."></textarea><br>
<input type="submit" value="Refine Paper">
</form>
{% if refined %}
<h3>Refined Paper:</h3>
<textarea id="output" rows="8" cols="80" readonly>{{ refined }}</textarea><br>
<button class="copy-btn" onclick="copyOutput()" type="button">Copy Refined Paper</button>
{% endif %}
{% if changes %}
<h3>Change Information:</h3>
<pre>{{ changes }}</pre>
{% endif %}
<a href="/email">Go to Email Refiner</a>
</body>
</html>
'''

def split_output(output):
    # Try to split by a clear marker for changes
    marker = None
    for m in [r'(?i)modifications\s*[:\n]', r'(?i)changes\s*[:\n]', r'---CHANGES---']:
        match = re.search(m, output)
        if match:
            marker = match
            break
    if marker:
        idx = marker.start()
        refined = output[:idx].strip()
        changes = output[idx:].strip()
        return refined, changes
    # Otherwise, do not split at all
    return output.strip(), ''

@app.route('/email', methods=['GET', 'POST'])
def email_form():
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text.strip():
            output = email(text)
            refined, changes = split_output(output)
            session['email_refined'] = refined
            session['email_changes'] = changes
        else:
            session['email_refined'] = ''
            session['email_changes'] = ''
        return redirect(url_for('email_form'))
    refined = session.pop('email_refined', None)
    changes = session.pop('email_changes', None)
    return render_template_string(EMAIL_FORM, refined=refined, changes=changes)

@app.route('/paper', methods=['GET', 'POST'])
def paper_form():
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text.strip():
            output = paper(text)
            refined, changes = split_output(output)
            session['paper_refined'] = refined
            session['paper_changes'] = changes
        else:
            session['paper_refined'] = ''
            session['paper_changes'] = ''
        return redirect(url_for('paper_form'))
    refined = session.pop('paper_refined', None)
    changes = session.pop('paper_changes', None)
    return render_template_string(PAPER_FORM, refined=refined, changes=changes)

IMAGE_FORM = '''
<!DOCTYPE html>
<html>
<head><title>Image Handler</title></head>
<body>
<h2>Image Handler</h2>
<form method="post" enctype="multipart/form-data">
    <label>Upload image file: <input type="file" name="image_file"></label><br>
    <label>Or provide image path: <input type="text" name="image_path" size="60"></label><br>
    <label>Extra instruction (optional):<br>
    <textarea name="instruction" rows="2" cols="60" placeholder="e.g., Translate the text in this image to French."></textarea></label><br>
    <input type="submit" value="Process Image">
</form>
{% if result %}
<h3>Result:</h3>
<pre>{{ result }}</pre>
{% endif %}
<a href="/">Back to Home</a>
</body>
</html>
'''

@app.route('/image', methods=['GET', 'POST'])
def image_form():
    result = None
    if request.method == 'POST':
        image_path = request.form.get('image_path', '').strip()
        instruction = request.form.get('instruction', '').strip()
        image_file = request.files.get('image_file')
        temp_path = None
        try:
            if image_file and image_file.filename:
                # Save uploaded file to a temp location
                temp_path = os.path.join('temp_upload', image_file.filename)
                os.makedirs('temp_upload', exist_ok=True)
                image_file.save(temp_path)
                img_path = temp_path
            elif image_path:
                img_path = image_path
            else:
                result = 'Please upload an image or provide a valid image path.'
                return render_template_string(IMAGE_FORM, result=result)
            # Use extra instruction if provided
            if instruction:
                # Use describe_slide with custom instruction
                base64_image = encode_image(img_path)
                response = client.chat.completions.create(
                    model=MODEL_4o,
                    messages=[
                        {"role": "system", "content": instruction},
                        {"role": "user", "content": [
                            {"type": "text", "text": instruction},
                            {"type": "image_url", "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"}
                            }
                        ]}
                    ],
                    temperature=0.0,
                )
                result = response.choices[0].message.content
            else:
                # Default: describe the image
                result = describe_slide(img_path)
        except Exception as e:
            result = f"Error: {e}"
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
    return render_template_string(IMAGE_FORM, result=result)

@app.route('/')
def home():
    return '<h2>Welcome! Choose a tool:</h2><ul><li><a href="/email">Email Grammar Refiner</a></li><li><a href="/paper">Paper Grammar Refiner</a></li></ul>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)