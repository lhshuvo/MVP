from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import pandas as pd
import requests
import requests.exceptions
from werkzeug.utils import secure_filename
import os
import re
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from email_validator import validate_email, EmailNotValidError
import fitz
from tqdm import tqdm

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xlsx', 'xls']

def extract_text_from_pdf(url):
    # download the PDF from the URL and extract text using PyMuPDF
    try:
        headers = {'User-Agent': UserAgent().random}
        r = requests.get(url, headers=headers)
        with fitz.open(stream=r.content, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
    except:
        return ""

def process_row(row):
    email = str(row['DirectEmail'])
    link = row['Source']
    if pd.isna(email) or pd.isna(link):
        return pd.Series({'valid_email': 0, 'Response_Type': ''})
    try:
        response = ''
        if link.endswith('.pdf'):
            text = extract_text_from_pdf(link)
            response = 'PDF'
        else:
            headers = {'User-Agent': UserAgent().random}
            response = requests.get(link, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        valid = False
        for e in emails:
            try:
                valid = validate_email(e.strip(), check_deliverability=True)
                break
            except EmailNotValidError:
                pass
        if valid:
            return pd.Series({'valid_email': 1, 'Response_Type': response})
        else:
            return pd.Series({'valid_email': 0, 'Response_Type': response})
    except requests.exceptions.RequestException:
        return pd.Series({'valid_email': -1, 'Response_Type': 'Request Error'})

@app.route('/', methods=['GET', 'POST'])
def myform():
    if request.method == 'POST':
        if 'x' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['x']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            results = []
            with tqdm(total=len(df)) as pbar:
                for index, row in df.iterrows():
                    results.append(process_row(row))
                    pbar.update(1)
            df[['valid_email', 'Response_Type']] = pd.DataFrame(results, columns=['valid_email', 'Response_Type'])
            filename1 = 'Outputfile.xlsx'
            df.to_excel(filename1)
            summary = {
                "total": len(df),
                "valid_emails": len(df.loc[df['valid_email'] == 1]),
                "invalid_emails": len(df.loc[df['valid_email'] == 0]),
                "request_errors": len(df.loc[df['valid_email'] == -1]),
            }
            return render_template('summary.html', summary=summary)
    return render_template('index.html')

@app.route('/download')
def download_file():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Outputfile.xlsx', as_attachment=True)
if __name__ == '__main__':
    app.run(port=1234, debug=True)
