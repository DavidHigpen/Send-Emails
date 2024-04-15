from multiprocessing import Process
from sendEmails import send_emails, load_messages, load_configuration

def send_email_with_semaphore(sender, password, emails, receiver_names, messages):
    send_emails(sender, password, emails, receiver_names, messages)
    
 
def main():
    parallel_processes = 4
    worker_pool = []
        
    sender, password, parish_names, secretary_emails, youth_minister_names, youth_minister_emails = load_configuration()

    secretary_messages = load_messages('./parishMessage.txt', parish_names, '[NO_HOTWORD]')
    youth_minister_messages = load_messages('./youthMinister.txt', youth_minister_names, '[Youth Minister Name]')
    # bulletin_messages = load_messages('./bulletin.txt', bulletin_parishs, '[Parish Name]')
    
    email_queue = secretary_emails + youth_minister_emails
    name_queue = parish_names + youth_minister_names
    message_queue = secretary_messages + youth_minister_messages
    category_queue = [' (secretary)'] * len(secretary_emails) + [' (youth minister)'] * len(youth_minister_emails)
    
    print(len(message_queue), "emails to send")
    
    queues = []
    for i in range(parallel_processes): # create list of queues to divide up tasks
        queues.append([])
        for j in range(3):
            queues[-1].append([])
    
    for index in range(len(email_queue)): # fill in the list of queues
        queues[index % parallel_processes][0].append(email_queue.pop(0))
        queues[index % parallel_processes][1].append(name_queue.pop(0) + category_queue.pop(0))
        queues[index % parallel_processes][2].append(message_queue.pop(0))
        
    
    for index in range(parallel_processes): # run each queue at the same time
        p = Process(target=send_email_with_semaphore, args=(sender, password, queues[index][0], queues[index][1], queues[index][2]))
        p.start()
        worker_pool.append(p)
    for p in worker_pool:
        p.join()  # Wait for all of the workers to finish.

    print("Finished")  
    
if __name__ == '__main__':
    main()