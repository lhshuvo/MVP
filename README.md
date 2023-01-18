# MVP
Email and Phone Number validation software
This program is used to read an excel file that contains multiple rows of email addresses, phone numbers, and source links. The program aims to read the excel file and cross-check the email and phone number according to the source link. If the email and phone number are found in the source link, the program will mark the row as found in the excel file. If the email and phone number are not found, the program will mark the row as not found. The program uses regular expressions to search for the email and phone numbers on the page, and it also uses a random sleep time between requests to avoid detection as a bot. The program also uses concurrent. Futures module to run multiple tasks at the same time using a thread pool to improve the performance of the program.


