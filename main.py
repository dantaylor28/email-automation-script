from dotenv import load_dotenv
import imaplib
import email
import os
load_dotenv()

username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def connect_to_mail():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    return mail

def search_for_email():
    mail = connect_to_mail()
    _, search_data = mail.search(None, '(BODY "unsubscribe")')


    mail.logout()