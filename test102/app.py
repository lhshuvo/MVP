from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import pandas as pd
import requests
import requests.exceptions
from werkzeug.utils import secure_filename
import os
import random
from fake_useragent import UserAgent
from retry import retry

#Initialize a Flask application
app = Flask("Test101")

#Set the location of the folder where uploaded files will be saved
app.config['UPLOAD_FOLDER'] = './'

#Function to check if the file being uploaded is in the allowed file types
def allowed_file(filename):
    # Return true if the file extension is in the allowed file types
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xlsx', 'xls']

#Route for the form submission
@app.route('/', methods = ['GET', 'POST'])
def myform():
    if request.method == 'POST':
        # Check if the form field 'x' (file input) is not present in the submitted form
        if 'x' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['x']
        # Check if no file was selected for upload
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # Check if the file being uploaded is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Save the uploaded file to the specified folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            responsess = []
            mail_validation = []
            ua = UserAgent()
        @retry(exceptions=requests.exceptions.ConnectTimeout, tries=3, delay=2) #we can modify tries and delay the defualt was tries=3,delay=2
        def is_email_present(email,url):
            headers = {'User-Agent': ua.random}
            response = requests.get(url, headers=headers)
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
#Route to download the output file
@app.route('/download')
def download_file():
     return send_from_directory(app.config['UPLOAD_FOLDER'], 'Outputfile.xlsx', as_attachment=True)

app.run(port=1234, debug=True)
'''if __name__ == '__main__':
    app.config['SERVER_NAME'] = 'example.com' #default = 'example.com'
    app.run(host='127.0.0.1', port=1234, debug=False)''' 
           
