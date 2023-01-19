# MVP (Email and Phone Number validation software)
This program is a Flask application that allows users to upload an excel file with a specific format and then performs some operations on the data in the file before returning the output in an excel file.

The program first imports the necessary libraries: Flask, render_template, request, send_from_directory, pandas, requests, and os. Then it creates a Flask application object and sets the upload folder and allowed file extensions for the application.

It also defines a function "allowed_file" to check if the file extension is allowed and then defines three routes: the first route '/' is for the form page, the second route '/auto.jpg' is for an image, and the third route '/favicon.ico' is for another image.

The fourth route '/output' is used to handle the uploaded file, check its extension, secure the filename, save the file to the upload folder, read the excel file, and perform a check to see if the email address is present in the website. The result of the check is added to the dataframe and then the dataframe is saved to an output excel file. Finally, the output template is rendered.

If the request method is not 'POST', the program returns 'Invalid request method'.


