import re
import pandas as pd
from docx import Document
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadCVForm
from io import BytesIO
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_bytes):
    text = ""
    reader = PdfReader(BytesIO(pdf_bytes))
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_doc(doc_path):
    text = ""
    doc = Document(doc_path)
    for para in doc.paragraphs:
        text += para.text
    return text

def extract_contact_info(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(?:\+\d{1,2}\s*)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    return emails, phones



def process_cv_file(cv_file):
    if cv_file.name.endswith('.pdf'):
        text = extract_text_from_pdf(cv_file.read())
    elif cv_file.name.endswith('.doc'):
        text = extract_text_from_doc(cv_file)
    elif cv_file.name.endswith('.docx'):
        text = extract_text_from_doc(cv_file)
    else:
        raise ValueError("Unsupported file format")
    
    emails, phones = extract_contact_info(text)
    
    max_length = max(len(emails), len(phones))
    emails += [''] * (max_length - len(emails))
    phones += [''] * (max_length - len(phones))
    
    return {'Email': emails, 'Phone': phones, 'Text': text}


def upload_cv(request):
    if request.method == 'POST':
        form = UploadCVForm(request.POST, request.FILES)
        if form.is_valid():
            cv_file = request.FILES['cv_file']
            cv_data = process_cv_file(cv_file)
            df = pd.DataFrame(cv_data)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="cv_data.xlsx"'
            df.to_excel(response, index=False)
            return response
    else:
        form = UploadCVForm()
    return render(request, 'cv_app/upload_cv.html', {'form': form})
