import sys
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from formatting import format_msg

#environment variables
username = "jpablogomezb.development@gmail.com" #EMAIL ACCOUNT (USERNAME) here
password = "Jp.dev.23" #PASSWORD HERE

def send_mail(text='Email Body', subject='Hello World', from_email='JP Dev <jpablogomezb.development@gmail.com>', to_emails=None, html=None):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    if html != None:
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)
    msg_str = msg.as_string()
    # login to my smtp server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()

def send(name, website=None, to_email=None, verbose=False):
    assert to_email != None
    if website != None:
        msg = format_msg(name=name, website=website)
    else:
        msg = format_msg(name=name)
    if verbose:
        print(name, website, to_email)
    # send message
    try:
        send_email(text=msg, to_emails=[to_email], html=None)
        sent = True
    except:
        sent = False
    return sent
    
if __name__ == "__main__":
    #print(sys.argv)
    name = "Unknown"
    if len(sys.argv) > 1:
        name = sys.argv[1]
    email = None
    if len(sys.argv) > 2:
        email = sys.argv[2]
    response = send(name, to_email=email, verbose=True)
    print(response)

