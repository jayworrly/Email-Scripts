import os
import pickle
import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Scopes required for the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CLIENT_SECRET_FILE = 'credentials.json'  # This is your downloaded credentials file
TOKEN_FILE = 'token.pickle'  # This file will store the access token

def authenticate_gmail():
    creds = None
    # Check if the token.pickle file exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials are available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8081)
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def move_emails_to_label(service, label_id, keywords):
    # Initialize variables for pagination
    next_page_token = None
    total_moved = 0
    
    # Construct the search query with the given keywords
    query = ' OR '.join([f'"{keyword}"' for keyword in keywords])
    
    while True:
        # Fetch a batch of messages from the inbox that match the search query
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=query, maxResults=500, pageToken=next_page_token).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print('No more messages found in Inbox matching the keywords.')
            break

        # Prepare batch request for modifying labels
        batch_modify_body = {
            'removeLabelIds': ['INBOX'],
            'addLabelIds': [label_id]
        }

        for message in messages:
            msg_id = message['id']
            service.users().messages().modify(userId='me', id=msg_id, body=batch_modify_body).execute()
            print(f"Moved message ID: {msg_id}")
            total_moved += 1

        # Check if there are more messages to process
        next_page_token = results.get('nextPageToken')
        if not next_page_token:
            break

    print(f"Total messages moved to label '{label_id}': {total_moved}")


def get_label_id(service, label_name):
    # Get the list of all labels
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    # Find the label ID corresponding to the label name
    for label in labels:
        if label['name'].lower() == label_name.lower():
            return label['id']
    
    # If the label does not exist, create it
    label_body = {
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }
    created_label = service.users().labels().create(userId='me', body=label_body).execute()
    return created_label['id']

def main():
    # Authenticate and get the Gmail service
    creds = authenticate_gmail()
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)

    # Specify the label name you want to move the emails to
    target_label_name = 'Southwest'  # Change this to your desired label
    label_id = get_label_id(service, target_label_name)

    # Specify the keywords you want to search for in the emails
    keywords = ['Southwest', 'flight', 'booking']  # Add your keywords here
    
    # Move emails containing these keywords from the Inbox to the specified label
    move_emails_to_label(service, label_id, keywords)

if __name__ == '__main__':
    main()
