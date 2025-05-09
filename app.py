from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

# Email configuration
class EmailConfig:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', '')
        self.smtp_port = os.getenv('SMTP_PORT', '587')
        self.email = os.getenv('EMAIL', '')
        self.password = os.getenv('PASSWORD', '')
        self.is_configured = bool(self.smtp_server and self.smtp_port and self.email and self.password)

    def save_config(self, smtp_server, smtp_port, email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.is_configured = True

        # Write to .env file
        with open('.env', 'w') as env_file:
            env_file.write(f'SMTP_SERVER={smtp_server}\n')
            env_file.write(f'SMTP_PORT={smtp_port}\n')
            env_file.write(f'EMAIL={email}\n')
            env_file.write(f'PASSWORD={password}\n')
            env_file.write(f'SECRET_KEY={app.secret_key}\n')
        
        return True

# Initialize email configuration
email_config = EmailConfig()

# Contact list management
CONTACTS_FILE = 'contacts.json'

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f)

# Routes
@app.route('/')
def index():
    return render_template('index.html', 
                          is_configured=email_config.is_configured,
                          email=email_config.email,
                          contacts=load_contacts())

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        smtp_server = request.form['smtp_server']
        smtp_port = request.form['smtp_port']
        email = request.form['email']
        password = request.form['password']
        
        if email_config.save_config(smtp_server, smtp_port, email, password):
            flash('Email configuration saved successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to save configuration.', 'error')
    
    return render_template('setup.html', 
                          smtp_server=email_config.smtp_server,
                          smtp_port=email_config.smtp_port,
                          email=email_config.email)

@app.route('/send_email', methods=['POST'])
def send_email():
    if not email_config.is_configured:
        flash('Please configure your email settings first.', 'error')
        return redirect(url_for('setup'))
    
    recipient = request.form['recipient']
    subject = request.form['subject']
    message = request.form['message']
    
    try:
        # Creating message
        msg = MIMEMultipart()
        msg['From'] = email_config.email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        # Setup SMTP server
        with smtplib.SMTP(email_config.smtp_server, int(email_config.smtp_port)) as server:
            server.starttls()  # Secure the connection
            server.login(email_config.email, email_config.password)
            server.send_message(msg)
        
        flash(f'Email sent successfully to {recipient}!', 'success')
    except Exception as e:
        flash(f'Failed to send email: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/contacts', methods=['GET', 'POST'])
def manage_contacts():
    contacts = load_contacts()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Simple validation
        if not name or not email:
            flash('Both name and email are required', 'error')
        else:
            contacts.append({'name': name, 'email': email})
            save_contacts(contacts)
            flash('Contact added successfully!', 'success')
            return redirect(url_for('manage_contacts'))
    
    return render_template('contacts.html', contacts=contacts)

@app.route('/delete_contact/<int:index>')
def delete_contact(index):
    contacts = load_contacts()
    if 0 <= index < len(contacts):
        deleted = contacts.pop(index)
        save_contacts(contacts)
        flash(f'Contact {deleted["name"]} deleted successfully!', 'success')
    else:
        flash('Invalid contact', 'error')
    return redirect(url_for('manage_contacts'))

# Create templates directory and files
def create_template_files():
    os.makedirs('templates', exist_ok=True)
    
    # Base template
    with open('templates/base.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Email Sender App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f7f7f7;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .navbar {
            background-color: #333;
            color: white;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .navbar a {
            color: white;
            text-decoration: none;
            margin-right: 15px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"], input[type="email"], input[type="password"], select, textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .alert {
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
        }
        .alert-error {
            background-color: #f8d7da;
            color: #721c24;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="navbar">
            <a href="/">Home</a>
            <a href="/setup">Email Setup</a>
            <a href="/contacts">Contacts</a>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>''')
    
    # Index template
    with open('templates/index.html', 'w') as f:
        f.write('''{% extends "base.html" %}

{% block content %}
    <h1>Email Sender App</h1>
    
    {% if not is_configured %}
        <div class="alert alert-error">
            Your email is not configured yet. Please <a href="/setup">setup your email</a> first.
        </div>
    {% else %}
        <div class="alert alert-success">
            Email configured: {{ email }}
        </div>
        
        <h2>Send Email</h2>
        <form action="/send_email" method="post">
            <div class="form-group">
                <label for="recipient">To:</label>
                <select name="recipient" id="recipient" required>
                    <option value="">Select a contact...</option>
                    {% for contact in contacts %}
                        <option value="{{ contact.email }}">{{ contact.name }} ({{ contact.email }})</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="subject">Subject:</label>
                <input type="text" id="subject" name="subject" required>
            </div>
            <div class="form-group">
                <label for="message">Message:</label>
                <textarea id="message" name="message" rows="6" required></textarea>
            </div>
            <button type="submit">Send Email</button>
        </form>
    {% endif %}
{% endblock %}''')
    
    # Setup template
    with open('templates/setup.html', 'w') as f:
        f.write('''{% extends "base.html" %}

{% block content %}
    <h1>Email Setup</h1>
    
    <form action="/setup" method="post">
        <div class="form-group">
            <label for="smtp_server">SMTP Server:</label>
            <input type="text" id="smtp_server" name="smtp_server" value="{{ smtp_server }}" required placeholder="e.g., smtp.gmail.com">
        </div>
        <div class="form-group">
            <label for="smtp_port">SMTP Port:</label>
            <input type="text" id="smtp_port" name="smtp_port" value="{{ smtp_port }}" required placeholder="e.g., 587">
        </div>
        <div class="form-group">
            <label for="email">Your Email:</label>
            <input type="email" id="email" name="email" value="{{ email }}" required>
        </div>
        <div class="form-group">
            <label for="password">Password/App Password:</label>
            <input type="password" id="password" name="password" required>
            <small>For Gmail, you may need to create an <a href="https://support.google.com/accounts/answer/185833" target="_blank">App Password</a>.</small>
        </div>
        <button type="submit">Save Configuration</button>
    </form>
{% endblock %}''')
    
    # Contacts template
    with open('templates/contacts.html', 'w') as f:
        f.write('''{% extends "base.html" %}

{% block content %}
    <h1>Manage Contacts</h1>
    
    <h2>Add New Contact</h2>
    <form action="/contacts" method="post">
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <button type="submit">Add Contact</button>
    </form>
    
    <h2>Contact List</h2>
    {% if contacts %}
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for contact in contacts %}
                    <tr>
                        <td>{{ contact.name }}</td>
                        <td>{{ contact.email }}</td>
                        <td><a href="/delete_contact/{{ loop.index0 }}">Delete</a></td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>No contacts found. Add your first contact above.</p>
    {% endif %}
{% endblock %}''')

if __name__ == '__main__':
    # Create template files if they don't exist
    create_template_files()
    
    # Check if .env file exists, create if not
    if not os.path.exists('.env'):
        with open('.env', 'w') as env_file:
            env_file.write('SECRET_KEY=your_secret_key_change_this\n')
            env_file.write('SMTP_SERVER=\n')
            env_file.write('SMTP_PORT=587\n')
            env_file.write('EMAIL=\n')
            env_file.write('PASSWORD=\n')
    
    # Run the app
    app.run(debug=True)