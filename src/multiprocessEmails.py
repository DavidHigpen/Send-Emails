from multiprocessing import Process
from sendEmails import send_emails, load_messages, load_configuration

def send_email_with_semaphore(sender, password, emails, receiver_names, messages):
    # print("process started")
    send_emails(sender, password, emails, receiver_names, messages)
    
 
def main():
    parallel_processes = 8
    worker_pool = []
        
    sender, password, bulletin_emails, bulletin_parishes = load_configuration()

    # secretary_messages = load_messages('./parishMessage.txt', parish_names, '[NO_HOTWORD]')
    # youth_minister_messages = load_messages('./youthMinister.txt', youth_minister_names, '[Youth Minister Name]')
    bulletin_messages = load_messages('./../messages/bulletin.txt', bulletin_parishes, '[Parish Name]')
    
    category_queue = [' (bulletin)'] * len(bulletin_messages) 
    
    print(len(bulletin_messages), "emails to send")

    queues = []
    for i in range(parallel_processes): # create list of queues to divide up tasks
        queues.append([])
        for j in range(3):
            queues[-1].append([])
    
    for index in range(len(bulletin_emails)): # fill in the list of queues
        queues[index % parallel_processes][0].append(bulletin_emails.pop(0))
        queues[index % parallel_processes][1].append(bulletin_parishes.pop(0) + category_queue.pop(0))
        queues[index % parallel_processes][2].append(bulletin_messages.pop(0))
        
    
    for index in range(parallel_processes): # run each queue at the same time
        p = Process(target=send_email_with_semaphore, args=(sender, password, queues[index][0], queues[index][1], queues[index][2]))
        p.start()
        worker_pool.append(p)
    for p in worker_pool:
        p.join()  # Wait for all of the workers to finish.

    print("Finished")  
    
if __name__ == '__main__':
    main()