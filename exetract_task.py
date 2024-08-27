import ocrmypdf
import PyPDF2
import pandas as pd
import re

# Perform OCR on the PDF file
input_pdf = "D:/riyaz_file1/riyaz_task/rpage4.pdf"
output_pdf = "D:/riyaz_file1/riyaz_task/output.pdf"
ocrmypdf.ocr(input_pdf, output_pdf)

# Path to the OCR'd PDF
pdf_path = output_pdf

# Initialize PDF reader
with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)  # Use PdfReader for newer versions
    ocr_extracted_data = []
    
    # Extract text from each page
    for page in pdf_reader.pages:
        ocr_extracted_data.append(page.extract_text())

# Define regex patterns for questions and options
question_start = re.compile(r'^\d+[.,)]')
option_pattern = re.compile(r'^\([A-E]\)')

# Parse the extracted text
parsed_data = []
for page_text in ocr_extracted_data:
    lines = page_text.splitlines()
    question = ""
    options = []
    
    for line in lines:
        line = line.strip()
        
        # Check if the line is the start of a new question
        if question_start.match(line):
            if question:  # Save the previous question data
                parsed_data.append({
                    "Question": question,
                    "Options": ", ".join(options)
                })
            question = line
            options = []
        
        # Check if the line contains an option
        elif option_pattern.match(line):
            options.append(line)
    
    # Append the last question if it exists
    if question:
        parsed_data.append({
            "Question": question,
            "Options": ", ".join(options)
        })

# Convert parsed data to DataFrame and save to CSV
df = pd.DataFrame(parsed_data)
csv_path = "D:/riyaz_file1/riyaz_task/extracted_questions.csv"
df.to_csv(csv_path, index=False)

print("Extraction completed. Data saved to 'extracted_questions.csv'.")
