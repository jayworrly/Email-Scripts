import os
import pickle
import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Scopes required for the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
SCOPES = ['https://mail.google.com/']

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
            creds = flow.run_local_server(port=8081)  # Change port here
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def delete_emails(service, keywords):
    # Construct the search query with the given keywords
    query = ' OR '.join([f'"{keyword}"' for keyword in keywords])
    
    # Initialize variables for pagination
    next_page_token = None
    total_deleted = 0
    
    while True:
        # Fetch a batch of messages
        results = service.users().messages().list(userId='me', q=query, maxResults=500, pageToken=next_page_token).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print('No more messages found.')
            break

        # Process each message
        for message in messages:
            msg_id = message['id']
            print(f"Deleting message ID: {msg_id}")
            service.users().messages().delete(userId='me', id=msg_id).execute()
            print(f'Deleted message with ID: {msg_id}')
            total_deleted += 1

        # Check if there are more messages to process
        next_page_token = results.get('nextPageToken')
        if not next_page_token:
            break

    print(f"Total messages deleted: {total_deleted}")


def main():
    # Authenticate and get the Gmail service
    creds = authenticate_gmail()
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)

    # Define your keywords here
    keywords = ["Doordash", "RobinHood"]  # Add your keywords here
    delete_emails(service, keywords)

if __name__ == '__main__':
    main()
