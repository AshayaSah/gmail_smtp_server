# Email Sender App - Setup & Usage Guide

This Python Flask application provides a simple UI for setting up and sending emails to contacts. The application uses Flask for the web interface and Python's standard email and smtplib libraries for handling email operations.

## Features

- Email configuration setup with SMTP server details
- Contact management (add, view, delete)
- Send emails to contacts with subject and message
- Simple and intuitive web interface
- Secure password handling (stored in .env file, not exposed)

## Installation

1. **Clone/download the code** to your local machine
2. **Install the dependencies**:

### i. Create a new virtual environment

```bash
python -m venv venv
```

### ii. Activate the new environment

```bash
venv\Scripts\activate
```

### iii. Install the dependencies from requirement.txt

```bash
pip install -r requirements.txt
```

## Getting Started

1. **Run the application**:

```bash
python app.py
```

2. The application will create necessary template files and start a local development server.
3. Open your browser and navigate to `http://127.0.0.1:5000/`

## Configuration Steps

### 1. Email Setup

Before you can send emails, you need to configure your email settings:

1. Click on "Email Setup" in the navigation bar
2. Enter your SMTP server details:
   - SMTP Server (e.g., `smtp.gmail.com` for Gmail)
   - SMTP Port (typically `587` for TLS)
   - Your email address
   - Your password or app password (for Gmail, you'll need an App Password)

**Note for Gmail users**: You'll need to create an [App Password](https://support.google.com/accounts/answer/185833) since Google blocks less secure apps.

### 2. Managing Contacts

To add and manage contacts:

1. Click on "Contacts" in the navigation bar
2. Fill in the contact form with:
   - Contact name
   - Contact email address
3. Click "Add Contact" to save
4. View all contacts in the table below
5. Delete contacts using the "Delete" link in the table

### 3. Sending Emails

Once you've set up your email and added contacts:

1. Go to the Home page
2. Select a recipient from the dropdown
3. Enter a subject for your email
4. Type your message in the text area
5. Click "Send Email"

## Troubleshooting

If you encounter issues sending emails:

1. **Check your SMTP settings** - Make sure server, port, username, and password are correct
2. **Gmail specific issues** - Ensure you're using an App Password and have less secure app access enabled
3. **Check your internet connection** - Make sure you can reach the SMTP server
4. **Firewall issues** - Some networks might block SMTP ports

## Security Note

This application stores your email credentials in a `.env` file which is not encrypted. For production use, consider implementing more secure credential management.

## Customization

You can customize the app by:

1. Modifying the templates in the `templates` folder to change the UI
2. Adding more functionality like email templates, scheduled emails, etc.
3. Implementing user authentication for multi-user support
