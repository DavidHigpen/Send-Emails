# Send-Emails

This program is used for sending out a mass of emails to different parishes to advertise the Connect Retreat

## Email-Setup

1. 

## Installation

1. Clone this repo to your local machine.
```bash
git clone https://github.com/DavidHigpen/Send-Emails.git
```

2. Install libary: `python-dotenv` or change code to have Google API key not hidden.
```bash
pip install python-dotenv
```

3. If using .env, create a new file in same directory called `.env`

4. Go to https://myaccount.google.com/u/1/signinoptions/two-step-verification and sign in with sender email account 

5. Hit "App Passwords" and create a new app password and same it something relevent

6. Copy the 16 character password and in your .env file, enter PASSWORD='<your_password>'

7. Run the main program file: `python3 sendEmails.py`.
