import os
import sys
import ssl
import smtplib
import csv
import copy
from dotenv import load_dotenv # DELETE ME
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import datetime


#CONVERT ’ to ' for all messages!

def to_multiline_string(normal_string):
    return f"""{normal_string}"""
    

def getFromCSV():
    diocesesSheets = os.listdir('./../dioceses')
    # parish_names = []
    # secretary_emails = []
    # youth_minister_names = []
    # youth_minister_emails = []
    bulletin_emails = []
    bulletin_parishes = []
    for dioceses in diocesesSheets:
        diocesesPath = os.path.join('./../dioceses', dioceses)
        
        with open(diocesesPath, newline='') as sheet:
            
            firstRow = True
            csvReader = csv.reader(sheet)
            for row in csvReader:
                if(not firstRow):
                    # if row[7].find('@') != -1 and row[2]:
                    #     parish_names.append(row[2])
                    #     secretary_emails.append(row[7])
                    # if row[11].find('@') != -1 and row[10]:
                    #     youth_minister_names.append(row[10])
                    #     youth_minister_emails.append(row[11])
                    if row[8].find('@') and row[2]:
                        bulletin_emails.append(row[8])
                        bulletin_parishes.append(row[2])
                firstRow = False
    return bulletin_emails, bulletin_parishes

def load_configuration():
    load_dotenv() # DELETE ME
    sender = 'davidhigpenscholarship@gmail.com' # UPDATE ME
    password = os.environ.get('PASSWORD') # UPDATE ME
    bulletin_emails, bulletin_parishes = getFromCSV()
    return sender, password, bulletin_emails, bulletin_parishes

def load_messages(file_path, insertIntoHotword, hotword):
    with open(file_path, 'r') as file:
        text = file.read()
        messages = [to_multiline_string(text.replace(hotword, replacement)) for replacement in insertIntoHotword]
    return messages

def send_emails(sender, password, emails, receiver_names, messages, created_emails = None):
    print("creating emails")
    if created_emails == None:
        created_emails = make_emails(sender, emails, receiver_names, messages)
        
    print("sending emails")
    
    BCC_list = ["davidhiggins@tamu.edu", "davidhigpen@gmail.com", "davidislearninghowtosendemails@gmail.com", "emailslotso@gmail.com"] # UPDATE ME
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password) # UNCOMMENT ME
        for i, em in enumerate(created_emails):
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                # smtp.sendmail(sender, em['To'], em.as_string()) # UNCOMMENT ME
                # em['Bcc'] = ", ".join(BCC_list)
                smtp.sendmail(sender, BCC_list, em.as_string()) # UNCOMMENT ME
            except smtplib.SMTPRecipientsRefused as e:
                print(f"ERROR email did not send to {receiver_names[i]} at {em['To']}")
                with open('./../logs/sentFails.txt', 'a') as file:
                    file.write(f"Email not sent to {receiver_names[i]} at {em['To']} at {current_time}\n")
            except smtplib.SMTPServerDisconnected:
                print("Server disconnected, ending program")
                exit()
            except KeyboardInterrupt:
                print("Keyboard interrupt detected. Logging out...")
                smtp.quit()
            else:
                print(f"Email sent to {receiver_names[i]}")
                with open('./../logs/sentReceipts.txt', 'a') as file:
                    file.write(f"Email sent to {receiver_names[i]} at {em['To']} at {current_time}\n")
            
        
        
def make_emails(sender, emails, receiver_names, messages):
    created_emails = []
        
    subject = 'Connect Retreat 2024'
    
    attachments = os.listdir('./../attachments')
    attachments = [os.path.join('./../attachments/', attachment) for attachment in attachments]
 
    with open('./../messages/gif.txt', 'r') as sig_file: # CHANGE ME back to .../signiture.txt'...
        signiture = sig_file.read()
        
    file_name = 'connectgif.gif'
    signitureLogo = './../messages/' + file_name
    
    emTemplate = MIMEMultipart()

    emTemplate['From'] = sender
    emTemplate['Subject'] = subject
    
    for f in attachments or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        emTemplate.attach(part)
    
    for _, (body, receiver_email) in enumerate(zip(messages, emails)):
        em = copy.deepcopy(emTemplate)
        em['To'] = receiver_email
    
        # emBody = MIMEText(body,x 'plain')
        # em.attach(emBody)
        
        emHTML = MIMEText(signiture % (signitureLogo), 'html')   
        em.attach(emHTML)

        with open(signitureLogo, 'rb') as fp:
            img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename=file_name)
        img.add_header('Content-ID', '<{}>'.format(signitureLogo))
        em.attach(img)
            
        created_emails.append(em)
    return created_emails
   

def main():
    sender, password, bulletin_emails, bulletin_parishes = load_configuration()
    
    # youth_minister_messages = load_messages('./youthMinister.txt', youth_minister_names, '[Youth Minister Name]')
    # send_emails(sender, password, youth_minister_emails, youth_minister_names, youth_minister_messages)
    
    bulletin_messages = load_messages('./../messages/bulletin.txt', bulletin_parishes, '[Parish Name]')
    send_emails(sender, password, bulletin_emails, bulletin_parishes, bulletin_messages)
    
    sys.exit()

if __name__ == "__main__":
    main()