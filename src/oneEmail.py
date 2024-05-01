from sendEmails import send_emails, load_messages, load_configuration
import sys



def main():
    sender, password, bulletin_emails, bulletin_parishes = load_configuration()
    
    # bulletin_messages = load_messages('./../messages/bulletin.txt', bulletin_parishes, '[Parish Name]')
    # send_emails(sender, password, bulletin_emails, bulletin_parishes, bulletin_messages)
    
    messages = load_messages('./../messages/test.txt', ["David"], '[None]')
    send_emails(sender, password, ['davidhigpen@gmail.com'], ["David"], messages)
    
    sys.exit()

    
if __name__ == '__main__':
    main()