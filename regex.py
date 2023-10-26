import docx2txt
from PyPDF2 import PdfReader
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop = stopwords.words('english')
import spacy
import pandas as pd
import en_core_web_sm
from spacy.matcher import Matcher

# Load pre-trained model
nlp = en_core_web_sm.load()

# Initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

# Extract text from DOCX
def doctotext(m):
    temp = docx2txt.process(m)
    resume_text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    text = ' '.join(resume_text)
    return text

# Extract text from PDF
def pdftotext(m):
    # Open the PDF file
    pdfFileObj = open(m, 'rb')

    # Create a PdfFileReader object
    pdfReader = PdfReader(pdfFileObj)

    # Number of pages in the PDF
    num_pages = len(pdfReader.pages)

    currentPageNumber = 0
    text = ''

    # Loop through all the pages in the PDF
    while currentPageNumber < num_pages:
        # Get the specified PDF page object
        pdfPage = pdfReader.pages[currentPageNumber]

        # Extract text from the PDF page
        text += pdfPage.extract_text()

        # Move to the next page
        currentPageNumber += 1

    # Close the PDF file
    pdfFileObj.close()

    return text
def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    
    person_names = []
    
    for ent in nlp_text.ents:
        if ent.label_ == 'PERSON':
            person_names.append(ent.text)
    
    if person_names:
        return person_names[0]  # Return the first recognized person's name
    
    return None 

STOPWORDS = set(stopwords.words('english'))
def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    edu = {}
    nlp_sents = list(nlp_text.sents)  # Convert generator to list for length checking
    for index, sent in enumerate(nlp_sents):
        for tex in word_tokenize(sent.text):  # Use word_tokenize to split text
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                if index + 1 < len(nlp_sents):
                    edu[tex] = sent.text + nlp_sents[index + 1].text

    education = []
    for key in edu.keys():
        year = re.search(r'(((20|19)(\d{})))', edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education
def extract_college(resume_text):
    nlp_text = nlp(resume_text)
    
    college_names = []
    
    for ent in nlp_text.ents:
        if ent.label_ == 'ORG':
            college_names.append(ent.text)
    
    if college_names:
        return college_names[0]  # Return the first recognized college or university name
    
    return None

# Define the set of education degrees
EDUCATION = [
    'BE', 'B.E.', 'B.E', 'BS', 'B.S', 
    'ME', 'M.E', 'M.E.', 'M.B.A', 'MBA', 'MS', 'M.S', 
    'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
    'SSLC', 'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
]

# Extract skills from the resume
def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # Removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    colnames = ['skill']


    # Extract values
    skills = ["general programming", "python" ,"django" ,"no sql", "machine learning", "data science","nlp", "cloud computing" ,"sql", "nodejs" ,"html" ,"css" ,"ms office"]
    skillset = []

    # Check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)

    return [i.capitalize() for i in set([i.lower() for i in skillset])]

# Extract mobile number from the resume
def extract_mobile_number(resume_text):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), resume_text)
    
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return number
        else:
            return number

# Extract email addresses from the resume
def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)
if __name__ == '__main__':
    FilePath = 'AI.pdf'
    FilePath.lower().endswith(('.png', '.docx'))
    if FilePath.endswith('.docx'):
        textinput = doctotext(FilePath) 
    elif FilePath.endswith('.pdf'):
        textinput = pdftotext(FilePath)
    else:
        print("File not supported")

    print('Name: ',extract_name(textinput) )
    print('Qualification: ', extract_education(textinput))
    print('College or university: ', extract_college(textinput))
    print('Skills:', extract_skills(textinput))
    print('Mobile Number: ', extract_mobile_number(textinput))
    print('Mail id: ', extract_email_addresses(textinput))
