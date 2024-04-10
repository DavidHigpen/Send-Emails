import os
import sys
import ssl
import smtplib
import csv
from dotenv import load_dotenv
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage


#CONVERT ’ to ' for all messages!

def to_multiline_string(normal_string):
    return f"""{normal_string}"""
    

def getFromCSV():
    diocesesSheets = os.listdir('./dioceses')
    parish_names = []
    secretary_emails = []
    youth_minister_names = []
    youth_minister_emails = []
    bulletin_emails = []
    bulletin_parishs = []
    for dioceses in diocesesSheets:
        diocesesPath = os.path.join('./dioceses', dioceses)
        
        with open(diocesesPath, newline='') as sheet:
            
            firstRow = True
            csvReader = csv.reader(sheet)
            for row in csvReader:
                if(not firstRow):
                    if row[7].find('@') != -1 and row[2]:
                        parish_names.append(row[2])
                        secretary_emails.append(row[7])
                    if row[11].find('@') != -1 and row[10]:
                        youth_minister_names.append(row[10])
                        youth_minister_emails.append(row[11])
                    if row[8].find('@') and row[2]:
                        bulletin_emails.append(row[8])
                        bulletin_parishs.append(row[2])
                firstRow = False
    return parish_names, secretary_emails, bulletin_emails, bulletin_parishs, youth_minister_names, youth_minister_emails

def load_configuration():
    load_dotenv()
    sender = 'davidhigpen@gmail.com' # Enter your email here
    password = os.environ.get('PASSWORD') # Update password in .env file in same dir
    parish_names, secretary_emails, bulletin_emails, bulletin_parishs, youth_minister_names, youth_minister_emails = getFromCSV()
    return sender, password, parish_names, secretary_emails, bulletin_emails, bulletin_parishs, youth_minister_names, youth_minister_emails

def load_messages(file_path, insertIntoHotword, hotword):
    with open(file_path, 'r') as file:
        text = file.read()
        messages = [to_multiline_string(text.replace(hotword, replacement)) for replacement in insertIntoHotword]
    return messages

def send_emails(sender, password, emails, receiver_names, messages):
    for index, (body, receiver_email, receiver_name) in enumerate(zip(messages, emails, receiver_names)):
        send_email(sender, password, body, receiver_email,receiver_name)
        
        
def send_email(sender, password, body, receiver_email, receiver_name):
    subject = 'Connect Retreat 2024'
    body += f"\n\nThis would have sent to {receiver_email}" # DELETE ME when sending emails
    receiver_email = 'davidislearninghowtosendemails@gmail.com' # DELETE ME to send out emails
    attachments = ["TestAttachment1.jpg", "connectLogo.png"] # Change to add relevant attachments
    
    
    with open('./signiture.txt', 'r') as sig_file:
        signiture = sig_file.read()
        
    signitureLogo = './connectLogo.png'
    
    em = MIMEMultipart()

    em['From'] = sender
    em['To'] = receiver_email
    em['Subject'] = subject
    
    emBody = MIMEText(body, 'plain')
    em.attach(emBody)
    
    emHTML = MIMEText(signiture % (signitureLogo), 'html')   
    em.attach(emHTML)   # Added, and edited the previous line

    with open(signitureLogo, 'rb') as fp:
        img = MIMEImage(fp.read())
    img.add_header('Content-Disposition', 'attachment', filename='ConnectLogo.jpg')
    img.add_header('Content-ID', '<{}>'.format(signitureLogo))
    em.attach(img)


    for f in attachments or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        em.attach(part)

    
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver_email, em.as_string())
        
    print(f"Email sent to {receiver_name}")
    return 1
    # exit() # DELETE ME
    

def main():
    sender, password, parish_names, secretary_emails, bulletin_emails, bulletin_parishes, youth_minister_names, youth_minister_emails = load_configuration()

    secretary_messages = load_messages('./parishMessage.txt', parish_names, '[NO_HOTWORD]')
    send_emails(sender, password, secretary_emails, parish_names, secretary_messages)
    
    youth_minister_messages = load_messages('./youthMinister.txt', youth_minister_names, '[Youth Minister Name]')
    send_emails(sender, password, youth_minister_emails, youth_minister_names, youth_minister_messages)
    
    bulletin_messages = load_messages('./bulletin.txt', parish_names, '[Parish Name]')
    send_emails(sender, password, bulletin_emails, bulletin_parishes, bulletin_messages)
    
    sys.exit()

if __name__ == "__main__":
    main()