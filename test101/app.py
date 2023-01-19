from flask import Flask, render_template, request
import pandas as pd
import requests

app = Flask("Test101")

@app.route('/', methods = ['GET', 'POST'])
def myform():
    return render_template('index.html')

# @app.route('/test')
# def TestRequest(): 
#     resp = request.get_data('https://stackoverflow.com/questions/55830807/cant-access-request-in-python-flask')
#     print('Response from TestRequest: '+resp.text)

@app.route('/output', methods = ['GET', 'POST'])
def output():
    data = request.form.get('x')
    df = pd.read_excel(data)
    
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
    
    filename1 = 'D:\\testing1\\test101\\Outputfile.xlsx'
    df.to_excel(filename1)
    
    return render_template('output.html')

app.run(port=1234, debug=True)