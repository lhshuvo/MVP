# MVP (Email and Phone Number validation software)
This code is a Flask web application that allows users to upload an excel file containing contact information (DirectEmail and DirectPhone) and a source link (Source). The application then reads the excel file using the pandas library, and for each row, it checks if the email address in the DirectEmail column is present on the webpage at the link in the Source column.

The application uses the requests library to make GET requests to the webpage at the link in the Source column. It also uses the fake_useragent library to add a random User-Agent header to each request to prevent the website from blocking the requests. Additionally, the retry library is used to handle any ConnectTimeout exceptions that may occur when making the requests. This means that if a request times out, the is_email_present() function will automatically retry the request twice more with a delay of 2 seconds before giving up.

The function is_email_present() takes two arguments, email and url, where email is the email address to be searched for on the webpage at the url. It creates a headers variable with a random User-Agent header, and then makes a GET request to the url with the headers. The response of the request is stored in the variable response, and also appended to the responsess list. If the email is found in the response text, it will append 1 to the mail_validation list, otherwise it will append 0.

The for loop iterates through the rows in the excel file, and for each row, it appends the values of DirectEmail, DirectPhone, and Source to the mail_address, phone and link lists respectively. The nested for loop then iterates through the range of the length of the dataframe and calls the is_email_present() function with the email address and link of the current row.

After the loops, a new column valid_email is added to the dataframe and its value is set as the mail_validation list, and another column Response_Type is added to the dataframe and its value is set as the responsess list. Then the dataframe is saved as an excel file named 'Outputfile.xlsx'.

Finally, when the application is run, it uses the render_template function to render the index.html file when a GET request is made to the '/' route, and the output.html file when a POST request is made. It also uses the send_from_directory function to download the 'Outputfile.xlsx' file when a GET request is made to the '/download' route. The application runs on port 1234 and has the debug mode set to True.

