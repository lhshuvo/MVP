from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import requests
import os
from werkzeug.utils import secure_filename

# Create a Flask application object
app = Flask("Test101")

# Set the upload folder for the application
app.config['UPLOAD_FOLDER'] = 'static'

# Set the allowed file extensions for the application
ALLOWED_EXTENSIONS = {'xlsx'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the form page
@app.route('/', methods = ['GET', 'POST'])
def myform():
    return render_template('index.html')

# Route for the 'auto.jpg' image
@app.route('/auto.jpg')
def auto_jpg():
    return send_from_directory('static', 'auto.jpg')

# Route for the 'favicon.ico' image
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

# Route for the output page
@app.route('/output', methods = ['GET', 'POST'])
def output():
    # Check if the request method is 'POST'
    if request.method == 'POST':
        # Check if the 'x' key is present in the request files
        if 'x' not in request.files:
            print('No file part')
            return
        # Get the file from the request
        file = request.files['x']
        # Check if a file was selected
        if file.filename == '':
            print('No selected file')
            return
        # Check if the file extension is allowed
        if file and allowed_file(file.filename):
            # Secure the filename
            filename = secure_filename(file.filename)
            # Save the file to the upload folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("Saved file: ", filename)
            print("Saved path: ", os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                # Read the excel file
                df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except Exception as e:
                print(f'Error: {e}')
                return 'Error processing the file'
            responsess = []
            mail_validation = []
            # Function to check if the email is present in the website
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
        #Append the direct email and direct phone to their respective lists
                 mail_address.append(df['DirectEmail'][i])
            phone.append(df['DirectPhone'][i])
            # Append the source url to the link list
            link.append(df['Source'][i])
        # Iterate through the dataframe to check if email is present in the website
        for i in range(len(df)):   
            is_email_present(mail_address[i], link[i])

        # Add the mail validation and response status to the dataframe
        df["valid_email"] = mail_validation
        df["response_type"] = responsess

        # Set the output filename
        filename1 = 'C:/Users/Employee/Desktop/Work Folder/Leads Database Platform/MVP/Outputfile.xlsx'

        # Write the dataframe to excel
        df.to_excel(filename1)

        # Render the output template
        return render_template('output.html')
# Return 'Invalid request method' if the request method is not 'POST'
    return 'Invalid request method'

app.run(port=1234, debug=True)