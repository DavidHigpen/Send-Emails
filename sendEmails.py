import os
import sys
import ssl
import smtplib
import csv
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
    diocesesSheets = os.listdir('./dioceses')
    # parish_names = []
    # secretary_emails = []
    # youth_minister_names = []
    # youth_minister_emails = []
    bulletin_emails = []
    bulletin_parishes = []
    for dioceses in diocesesSheets:
        diocesesPath = os.path.join('./dioceses', dioceses)
        
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

def send_emails(sender, password, emails, receiver_names, messages):
    created_emails = []
    print("creating emails")
    for _, (body, receiver_email) in enumerate(zip(messages, emails)):
        temp = make_email(sender, password, body, receiver_email)
        created_emails.append(temp)
        
    print("sending emails")
    
    BCC_list = ["davidhiggins@tamu.edu"] # UPDATE ME
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        # smtp.login(sender, password) # UNCOMMENT ME
        for i, em in enumerate(created_emails):
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                # smtp.sendmail(sender, em['To'], em.as_string()) # UNCOMMENT ME
                em['Bcc'] = ", ".join(BCC_list)
                # smtp.sendmail(sender, BCC_list, em.as_string()) # UNCOMMENT ME
            except:
                print(f"ERROR email did not send to {receiver_names[i]} at {em['To']}")
                with open('sentFails.txt', 'a') as file:
                    file.write(f"Email not sent to {receiver_names[i]} at {em['To']} at {current_time}\n")
            else:
                print(f"Email sent to {receiver_names[i]}")
                with open('sentReceipts.txt', 'a') as file:
                    file.write(f"Email sent to {receiver_names[i]} at {em['To']} at {current_time}\n")
            
        
        
def make_email(sender, password, body, receiver_email):
    subject = 'Connect Retreat 2024'
    body += f"\n\nThis would have sent to {receiver_email}" # DELETE ME when sending emails
    receiver_email = 'davidislearninghowtosendemails@gmail.com' # DELETE ME to send out emails
    attachments = ["Sunday Bulletin Announcement.png", "St. Mary's Flyer.pdf"] # Change to add relevant attachments
    
    
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
    em.attach(emHTML)

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
            
    return em
   

def main():
    sender, password, bulletin_emails, bulletin_parishes = load_configuration()
    
    # youth_minister_messages = load_messages('./youthMinister.txt', youth_minister_names, '[Youth Minister Name]')
    # send_emails(sender, password, youth_minister_emails, youth_minister_names, youth_minister_messages)
    
    bulletin_messages = load_messages('./bulletin.txt', bulletin_parishes, '[Parish Name]')
    send_emails(sender, password, bulletin_emails, bulletin_parishes, bulletin_messages)
    
    sys.exit()

if __name__ == "__main__":
    main()