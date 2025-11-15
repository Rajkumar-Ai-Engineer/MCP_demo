import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use environment variables for security
Sender_mail = os.getenv("GMAIL_USER", "aids23041@gmail.com")
Sender_password = os.getenv("GMAIL_APP_PASSWORD", "zchp kdzl noon bacj").replace(" ", "")

# Instructions:
# 1. Enable 2-factor authentication on your Gmail account
# 2. Generate an App Password: https://myaccount.google.com/apppasswords
# 3. Set environment variable: set GMAIL_APP_PASSWORD=your_16_char_app_password