from dotenv import load_dotenv
import imaplib
import email
import os
from bs4 import BeautifulSoup
load_dotenv()

username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def connect_to_mail():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    return mail

def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    links = [link["href"] for link in soup.find_all("a", href=True) if "unsubscribe" in link["href"].lower()]
    return links

def search_for_email():
    mail = connect_to_mail()
    _, search_data = mail.search(None, '(BODY "unsubscribe")')
    data = search_data[0].split()

    for num in data:
        _, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset()
                    try:
                        html_content = payload.decode(charset or 'utf-8')
                    except UnicodeDecodeError:
                        html_content = payload.decode('latin-1')  # fallback
                    print(html_content)
        else:
            content_type = msg.get_content_type()
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset()
            try:
                content = payload.decode(charset or 'utf-8')
            except UnicodeDecodeError:
                content = payload.decode('latin-1')
            if content_type == "text/html":
                print(content)

    mail.logout()


search_for_email()