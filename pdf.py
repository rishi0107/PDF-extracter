from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI()
loader = PyPDFLoader('Website-Advt.-DC-South-West-Driver.pdf')
pages = loader.load_and_split()
# Define the query to extract information from the PDF
query = "Extract information and answer in this format only - --!1)Organization name !2) Name of post !3)Total number of posts !4) Essential/Desired Qualificatios !5) Experience !6) Job description !7) Wages !8) Agelimit If there are multiple jobs then put it in the same index and give the answer, don't give headings just givethe answer for the point, I want to save it in the excel file."
# Load the question answering chain
from langchain.chains.question_answering import load_qa_chain
chain=load_qa_chain(llm, chain_type="stuff")
# Extract information from the PDF using the query
answer=chain.run(input_documents=pages, question=query)
# Split the text by newline characters and remove any empty lines
lines=[line.strip() for line in answer.split('\n') if line.strip()]
# Extract the data from the lines
organization=lines[0][2:]
posts=lines[1][2:]
num_posts=lines[2][2:]
qualifications=lines[3][2:]
experience=lines[4][2:]
descript=lines[5][2:]
salaries=lines[6][2:]
agelim=lines[7][2:]
# Create a list of dictionaries with the extracted data
data=[]
data.append({
    'organization': organization,
    'posts': posts,
    'No of posts': num_posts,
    'qualifications': qualifications,
    'experience': experience,
    'job description': descript,
    'salary': salaries,
    'age limit': agelim,

})
# Write the data to a CSV file
import csv
with open('data1.csv', 'w', newline='') as csvfile:
 fieldnames=['organization', 'posts', 'No of posts', 'qualifications', 'experience', 'job description', 'salary', 'age limit']
 writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
 writer.writeheader()
 for row in data:
    writer.writerow(row)
