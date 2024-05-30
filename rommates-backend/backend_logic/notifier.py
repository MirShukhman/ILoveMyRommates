
from datetime import datetime

from log.logger import Logger
from .email_handler import EmailHandler
from models.notifications import Notification
from models.users import User

logger = Logger()

# 30.05.24
# Class Notifier will handle creation and updating of notifications, 
#   as well passing them to EmailHandler class for users to be notifed by email as well.

class Notifier:
    def __init__(self):
        self.email = EmailHandler()
    
    
    def _create_notification(self, user_id, message):
        """
        30.05.24
        Adding notification to db

        Args:
            user_id (int)
            message (str)

        Returns:
            Bool
        """
        try:
            now = datetime.now()
            new_notification = Notification.add(UserID=user_id,
                                                Message=message,
                                                CreatedAt=now)
            output = new_notification
            return True if new_notification else False
            
        except Exception as e:
            output = str(e)
            return False 
        
        finally:
            logger.log('Notifier','create_notification',(user_id, message),output)
    
    
    def mark_as_read(self, notification_id):
        """
        30.05.24
        Marking notification as read == True in db

        Args:
            notification_id (int)

        Returns:
            Bool
        """
        try:
            read = Notification.update(notification_id,IsRead=1)
            output = read
            return True if read else False
            
        except Exception as e:
            output = str(e)
            return False 
        
        finally:
            logger.log('Notifier','mark_as_read',notification_id,output)
                
    
    def notify_admins(self, home_id, message):
        """
        30.05.24
        Gets all admin tenants by home id (sq), for each admin gets user id
        using tenant id (sq) and calls notify_specific_user.

        Args:
            home_id (int)
            message (str)

        Returns:
            Bool (will be marked as False on single user fail, True only if all sucsess)
        """
        try:
            admins = User.get_query('GetAdminTenantsByHomeID',home_id)
            all_successful = True
            for admin in admins:
                user = User.get_query('GetUserByTenantID', admin[4])
                
                user_id = user[6]
                notify_user = self.notify_specific_user(user_id, message)
                if not notify_user:
                    all_successful = False
                    
            return all_successful
            
        except Exception as e:
            all_successful = str(e)
            return False 
        
        finally:
            logger.log('Notifier','notify_admins',(home_id, message),all_successful)    
    
    
    def notify_all_home(self, home_id, message):
        """
        30.05.24
        Gets all tenants by home id (sq), for each admin gets user id
        using tenant id (sq) and calls notify_specific_user. If no user for tenant- skips.

        Args:
            home_id (int)
            message (str)

        Returns:
            Bool (will be marked as False on single user fail, True only if all sucsess)
        """        
        try:
            tenants = User.get_query('GetTenantsByHomeID',home_id)
            all_successful = True
            for tenant in tenants:
                user = User.get_query('GetUserByTenantID', tenant[4])
                if not user:
                    continue 
        
                user_id = user[6]
                notify_user = self.notify_specific_user(user_id, message)
                if not notify_user:
                    all_successful = False
                    
            return all_successful
            
        except Exception as e:
            all_successful = str(e)
            return False 
        
        finally:
            logger.log('Notifier','notify_all_home',(home_id, message),all_successful)    
    
    
    def notify_all_users(self,message):
        """
        30.05.24
        Gets all users, for each user calls notify_specific_user. 

        Args:
            message (str)

        Returns:
            Bool (will be marked as False on single user fail, True only if all sucsess)
        """        
        try:
            users = User.get_all()
            all_successful = True
            for user in users:
                user_id = user.ID
                notify_user = self.notify_specific_user(user_id, message)
                if not notify_user:
                    all_successful = False
                    
            return all_successful
            
        except Exception as e:
            all_successful = str(e)
            return False  
        
        finally:   
            logger.log('Notifier','notify_all_users',(message),all_successful)    
    
    
    def notify_specific_user(self, user_id,message):
        """
        30.05.24
        Send notification by user_id, calls _create_notification
        to add to db, if added also calls EmailHandler class to send email
        with the notification message.

        Args:
            user_id (int)
            message (str)

        Returns:
           Bool
        """
        try:
            add_notification = self._create_notification(user_id, message)
            if add_notification:
                user = User.get(user_id)
                email = user.Email
                send_email = self.email.send_notification_email(email,message)
                output = True if send_email else False
                return output
            
            output = False    
            return False
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
              logger.log('Notifier','notify_specific_user',(user_id,message),output)   