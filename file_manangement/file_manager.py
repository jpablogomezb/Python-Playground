import os

this_file_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(this_file_path)

#email_txt = "templates/email.txt"
email_txt = os.path.join(BASE_DIR, "templates", "email.txt")
content = ""

with open(email_txt, 'r') as f:
    content = f.read()

print(content.format(name='Paul'))