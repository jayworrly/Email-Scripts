import imaplib
import email
from imapclient import IMAPClient

# Define your Yahoo Mail credentials
EMAIL = 'your_yahoo_email@yahoo.com'
PASSWORD = 'your_app_password'
IMAP_SERVER = 'imap.mail.yahoo.com'
IMAP_PORT = 993

def move_emails_to_label(service, label_id, keywords):
    # Initialize variables for pagination
    next_page_token = None
    total_moved = 0
    
    # Construct the search query with the given keywords
    query = 'OR '.join([f'SUBJECT "{keyword}"' for keyword in keywords])
    
    while True:
        # Fetch a batch of messages from the inbox that match the search query
        results = service.search(query)
        
        if not results:
            print('No more messages found in Inbox matching the keywords.')
            break

        # Move matching messages to the target folder (label)
        for msg_id in results:
            service.move([msg_id], label_id)
            print(f"Moved message ID: {msg_id}")
            total_moved += 1

        # Check if there are more messages to process
        next_page_token = results.get('nextPageToken')
        if not next_page_token:
            break

    print(f"Total messages moved to label '{label_id}': {total_moved}")

def get_label_id(service, label_name):
    # Get the list of all labels
    results = service.list_folders()
    labels = [folder[2] for folder in results]

    # Find the label ID corresponding to the label name
    for label in labels:
        if label.lower() == label_name.lower():
            return label
    
    # If the label does not exist, create it
    service.create_folder(label_name)
    return label_name

def main():
    # Authenticate and get the Yahoo Mail service
    with IMAPClient(IMAP_SERVER, use_uid=True, ssl=True) as service:
        service.login(EMAIL, PASSWORD)

        # Specify the label name you want to move the emails to
        target_label_name = 'Desired label'  # Change this to your desired label
        label_id = get_label_id(service, target_label_name)

        # Specify the keywords you want to search for in the emails
        keywords = ['Keywords 1', 'Keywords 2', 'Keywords 3']  # Add your keywords here

        # Move emails containing these keywords from the Inbox to the specified label
        move_emails_to_label(service, label_id, keywords)

if __name__ == '__main__':
    main()
