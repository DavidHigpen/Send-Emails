from multiprocessing import Process, Semaphore
from sendEmails import send_email, load_messages, load_configuration

def send_email_with_semaphore(semaphore, sender, password, message, email, name):
    semaphore.acquire() 
    try:
        send_email(sender, password, message, email, name)
    finally:
        semaphore.release()
    

def main():
    max_requests = 8
    semaphore = Semaphore(max_requests)
    worker_pool = []
        
    sender, password, parish_names, secretary_emails, bulletin_emails, bulletin_parishs, youth_minister_names, youth_minister_emails = load_configuration()

    secretary_messages = load_messages('./parishMessage.txt', parish_names, '[NO_HOTWORD]')
    youth_minister_messages = load_messages('./youthMinister.txt', youth_minister_names, '[Youth Minister Name]')
    bulletin_messages = load_messages('./bulletin.txt', bulletin_parishs, '[Parish Name]')
    
    email_queue = secretary_emails + youth_minister_emails + bulletin_emails
    name_queue = parish_names + youth_minister_names + bulletin_parishs
    message_queue = secretary_messages + youth_minister_messages + bulletin_messages
    category_queue = [' (secretary)'] * len(secretary_emails) + [' (youth minister)'] * len(youth_minister_emails) + [' (bulletin)'] * len(bulletin_emails)
    
    # print(email_queue)
    # print(name_queue)
    print(len(message_queue))
    
        
    for _ in range(len(email_queue)):
        email = email_queue.pop(0)
        name = name_queue.pop(0)
        message = message_queue.pop(0)
        category = category_queue.pop(0)
        
        p = Process(target=send_email_with_semaphore, args=(semaphore, sender, password, message, email, name + category))
        p.start()
        worker_pool.append(p)
    for p in worker_pool:
        p.join()  # Wait for all of the workers to finish.

    print("Finished")  
    
if __name__ == '__main__':
    main()