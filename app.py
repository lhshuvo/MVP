from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import pandas as pd
import requests
import requests.exceptions
from werkzeug.utils import secure_filename
import os
import re
import random
from fake_useragent import UserAgent
from tqdm import tqdm
from bs4 import BeautifulSoup
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xlsx', 'xls']

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
            responsess = []
            mail_validation = []
            ua = UserAgent()

            for i in tqdm(range(len(df))):
                email = str(df['DirectEmail'][i])
                link = df['Source'][i]
                if pd.isna(email) or pd.isna(link):
                    continue
                try:
                    headers = {'User-Agent': ua.random}
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
                        mail_validation.append(1)
                    else:
                        mail_validation.append(0)
                    responsess.append(response)
                except requests.exceptions.RequestException:
                    responsess.append("Request Error")
                    mail_validation.append(-1)

            df["valid_email"] = mail_validation
            df["Response_Type"] = responsess
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
