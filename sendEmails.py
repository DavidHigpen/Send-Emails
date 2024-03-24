import os
import sys
import ssl
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

def to_multiline_string(normal_string):
    return f"""{normal_string}"""

def get_parishes():
    file_path = './parishes.txt'
    parishes = []
    emails = []
    with open(file_path, 'r') as file:
        text = file.read()
        text = text.split("\n")
        for parish in text:
            parish = parish.split(", ")
            parishes.append(parish[0])
            emails.append(parish[1])
    return parishes, emails

def load_configuration():
    load_dotenv()
    sender = 'davidhigpen@gmail.com' # Enter your email here
    password = os.environ.get('PASSWORD') # Update password in .env file in same dir
    parishes, emails = get_parishes()
    file_path = "./message.txt"
    return sender, password, emails, parishes, file_path

def load_messages(file_path, parishes):
    with open(file_path, 'r') as file:
        text = file.read()
        messages = [to_multiline_string(text.replace('[parish]', parish)) for parish in parishes]
    return messages

def send_emails(sender, password, emails, parishes, messages):
    for index, (body, receiver, parish) in enumerate(zip(messages, emails, parishes)):
        subject = f'Welcome {parish} students to Connect!'
        body += f"\n\nThis would have sent to {receiver}"
        receiver = 'davidislearninghowtosendemails@gmail.com' # DELETE ME to send out emails
        attachments = ["TestAttachment1.jpg"]

        em = EmailMessage()

        em['From'] = sender
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)
        for attachment_path in attachments:
            with open(attachment_path, "rb") as attachment:
                em.add_attachment(attachment.read(), maintype="application", subtype='octet-stream', filename=os.path.basename(attachment_path))


        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, em.as_string())
        print(f"Email sent to {parish}")

def main():
    sender, password, emails, parishes, file_path = load_configuration()
    messages = load_messages(file_path, parishes)
    send_emails(sender, password, emails, parishes, messages)
    sys.exit()

if __name__ == "__main__":
    main()
