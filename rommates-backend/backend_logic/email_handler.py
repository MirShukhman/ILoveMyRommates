import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from jinja2 import Environment, FileSystemLoader

from log.logger import Logger

# 20.05.24
# EmailHandler class will handle creation and sending of all email messages to users
# Each use is logged in Logger

logger = Logger()

class EmailHandler:
    def __init__(self):
        pass
    
    def _send_email(self,email_receiver,subject,message):
        output=True
        try:
            load_dotenv()
            # Email configuration
            email_sender = 'iheartmyroommates@gmail.com'
            email_receiver = f'{email_receiver}'
            password = os.environ.get('EMAIL_PASSWORD')

            # Create message
            html_message = message
            msg = MIMEMultipart()
            msg['From'] = email_sender
            msg['To'] = email_receiver
            msg['Subject'] = f'{subject}'
            msg.attach(MIMEText(html_message, 'html'))

            # Send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_sender, password)
                smtp.send_message(msg)
                
            return True
                
        except Exception as e:
            output=str(e)
            return False
            
        finally:
            logger.log('email_handler','send_email',(email_receiver,subject),output)       
                
        
    def _create_verification_message(self,verification_code):
        output=True
        try:
            # Create environment and load the template
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('verify_template.html')

            # Render the template with the provided param
            rendered_content = template.render(code=verification_code)
            return rendered_content
        
        except Exception as e:
            output=str(e)
            return False
            
        finally:
            logger.log('email_handler','_create_verification_message',verification_code,output)      
            
    
    def _create_invitation_message(self, home_id):
        output=True
        try:
            # Create environment and load the template
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('invitation_template.html')

            # Render the template with the provided param
            rendered_content = template.render(home_id=home_id)
            return rendered_content
        
        except Exception as e:
            output=str(e)
            return False
            
        finally:
            logger.log('email_handler','_create_invitation_message',home_id,output)     
    
    
    def _create_notification_message(self, notification):
        output=True
        try:
            # Create environment and load the template
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('notification_template.html')

            # Render the template with the provided param
            rendered_content = template.render(notification=notification)
            return rendered_content
        
        except Exception as e:
            output=str(e)
            return False
            
        finally:
            logger.log('email_handler','_create_notification_message',notification,output)       
    
    
    def send_verification_email(self, email_receiver, verification_code):
        try:
            message= self._create_verification_message(verification_code)
            send_email=self._send_email(email_receiver,'Your Verification Code',message)
            output = send_email
            return send_email
            
        except Exception as e:
            output=str(e)
            return False
            
        finally:
            logger.log('email_handler','send_verification_email',(email_receiver,verification_code),output)      
            
            
    def send_invitation_email(self, email_receiver, home_id):
        try:
            message= self._create_invitation_message(home_id)
            send_email=self._send_email(email_receiver,'Invitation To Join a Home',message)
            output = send_email
            return send_email
            
        except Exception as e:
            output=str(e)
            return False
            
        finally:
            logger.log('email_handler','send_invitation_email',(email_receiver,home_id),output)      
            
            
    def send_notification_email(self, email_receiver, notification):
        try:
            message= self._create_notification_message(notification)
            send_email=self._send_email(email_receiver,'New Notification',message)
            output = send_email
            return send_email
            
        except Exception as e:
            output=str(e)
            return False
            
        finally:
            logger.log('email_handler','send_notification_email',(email_receiver,notification),output)      