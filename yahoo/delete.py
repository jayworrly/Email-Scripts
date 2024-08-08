import imaplib
import email
from imapclient import IMAPClient

# Define your Yahoo Mail credentials
EMAIL = 'your_yahoo_email@yahoo.com'
PASSWORD = 'your_app_password'
IMAP_SERVER = 'imap.mail.yahoo.com'
IMAP_PORT = 993

def delete_emails(keywords):
    with IMAPClient(IMAP_SERVER, use_uid=True, ssl=True) as client:
        client.login(EMAIL, PASSWORD)
        client.select_folder('INBOX')

        # Build the search query
        search_criteria = 'OR '.join([f'SUBJECT "{keyword}"' for keyword in keywords])
        messages = client.search(search_criteria)
        
        if not messages:
            print('No messages found.')
            return

        print(f'Found {len(messages)} messages matching the keywords.')

        # Delete messages that match the search criteria
        for msg_id in messages:
            client.delete_messages([msg_id])
            print(f'Deleted message ID: {msg_id}')

        # Expunge to permanently delete the messages
        client.expunge()

        print(f"Total messages deleted: {len(messages)}")

def main():
    # Specify the keywords you want to search for in the emails
    keywords = ['Southwest', 'flight', 'booking']  # Add your keywords here

    # Delete emails containing these keywords from the Inbox
    delete_emails(keywords)

if __name__ == '__main__':
    main()
