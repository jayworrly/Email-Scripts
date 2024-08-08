Step-by-Step Guide
1. Create a Project in Google Cloud Console
Go to the Google Cloud Console.
Create a New Project:
Click on the project dropdown on the top left.
Select “New Project” and give your project a name.
Enable the Gmail API:
In the left-hand menu, go to “APIs & Services” > “Library”.
Search for “Gmail API” and click on it.
Click “Enable”.
2. Create OAuth 2.0 Credentials
Create Credentials:
Go to “APIs & Services” > “Credentials”.
Click “Create Credentials” and select “OAuth Client ID”.
Configure the consent screen if prompted (you can set this to internal if only you are using it).
Configure OAuth Consent Screen:
Fill out the required fields and save.
Create OAuth Client ID:
Application type: Select “Desktop app”.
Name: Give it a name.
Click “Create”.
Download the credentials.json file and save it in the same directory as your Python script.

python delete_gmail_messages.py

python move_emails.py
