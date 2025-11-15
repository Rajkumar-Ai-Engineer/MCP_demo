from src.logger.logger import logging
from src.exception.exception import MCP_AGENT_Exception
import sys

from src.config.mail_config import Sender_mail, Sender_password

import smtplib
from email.mime.text import MIMEText

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Mail")


@mcp.tool()
def send_email(recipient_email:str,subject:str,body:str):
    try:
        logging.info(f"Preparing to send email to {recipient_email} with subject '{subject}'")
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = Sender_mail
        msg['To'] = recipient_email
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(Sender_mail, Sender_password)
            server.sendmail(Sender_mail, [recipient_email], msg.as_string())
        logging.info(f"Email sent successfully to {recipient_email}")
        return f"Email sent successfully to {recipient_email}"
    except Exception as e:
        logging.error(f"Error creating email message: {e}")
        raise MCP_AGENT_Exception(e, sys)
    
if __name__ == "__main__":
    mcp.run(transport="stdio")