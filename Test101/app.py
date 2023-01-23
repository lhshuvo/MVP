from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import requests
from werkzeug.utils import secure_filename
import os

app = Flask("Test101")
app.config['UPLOAD_FOLDER'] = './'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xlsx', 'xls']

@app.route('/', methods = ['GET', 'POST'])
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
            def is_email_present(email,url):
                response = requests.get(url)
                responsess.append(response)
                if email in response.text:
                    mail_validation.append(1)
                else:
                    mail_validation.append(0)
            mail_address = [] 
            link = []
            phone = []
            print(len(df))
            for i in range(len(df)):
                mail_address.append(df['DirectEmail'][i])
                phone.append(df['DirectPhone'][i])
                link.append(df['Source'][i])
            for i in range(len(df)):
                is_email_present(mail_address[i], link[i])
            df["valid_email"] = mail_validation
            df["Response_Type"] = responsess
            filename1 = 'Outputfile.xlsx'
            df.to_excel(filename1)
            return render_template('output.html')
    return render_template('index.html')

app.run(port=1234, debug=True)
