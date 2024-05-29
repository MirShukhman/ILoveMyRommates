
from app import bcrypt
import random

from log.logger import Logger
from backend_logic.login_token import LoginToken
from backend_logic.email_handler import EmailHandler
from models.users import User
from models.tenants import Tenant

# 27.05.24
# Class Unlogged Facade will hold funcs avilable to every user before login:
#   login, signup, email confirmation: no login can be made without email confirmation, 
#   and reset password.

class Unlogged:
    def __init__(self):
        self.logger = Logger() 
        self.login_token = LoginToken()
        self.email_handler = EmailHandler()
    
    
    def _check_password(self,hashed_password,password):
        result= bcrypt.check_password_hash(hashed_password, password)
        self.logger.log('Unlogged','_check_password', hashed_password, result)
        return result
    
    
    def _generate_confirmation_code(self):
        random_code = random.randint(100000, 999999)
        return random_code
    
    
    def login(self, username, password):
        """
        27.05.24
        Login to account, finds user by username (sq), compares password
        given with hashed_bd_pass, ensures no verification_code exists for user
        (as existense of such code implies user either didnt confirm email or
        has asked for password reset), if tenant_id exists for user fetches
        tenant data, calls login_token and recives frontend_token, returns frontend_token.

        Args:
            username (str)
            password (str)

        Returns:
            True/False, err(None/str)
        """
        err = None
        try:
            user = User.get_query('GetUserByUsername',str(username))
            if user:
                db_pass = user[0][1]
                user_id = user[0][6]
                tenant_id = user[0][0]
                verification_code = user[0][8]
                ok = self._check_password(db_pass,str(password))
                if ok:
                    if verification_code:
                        err,output = 'Email Verification Requred. Please Check Your Email.'
                        return False, err
                    
                    if tenant_id:
                        tenant = Tenant.get(tenant_id)
                        home_id = tenant.HomeID
                        name = tenant.Name
                        is_admin_tennant = tenant.CanEdit
                        
                    frontend_token = self.login_token.generate_token(
                        user_id, 
                        tenant_id if tenant_id else None, 
                        home_id if tenant_id else None, 
                        name if tenant_id else None, 
                        is_admin_tennant if tenant_id else None
                    )
                    
                    if frontend_token:
                        output = frontend_token
                        return frontend_token, err
                    
                    else:
                        err, output = "Inernal Error. Please Try Again Later."
                        return False, err
                          
            else:
                err, output = "Wrong Username/Password"
                return False,err
            
        except Exception as e:
            err = "Inernal Error. Please Try Again Later."
            output = str(e)
            return False, err
            
        finally:
            self.logger.log('Unlogged','login', username, output)
    
    
    def sign_up (self, username, password, 
                 email, phone, profile_pic):
        """
        27.05.24
        Firs step of sign up process: checks if user with given email/username
        exists (sq), generates verification_code and sends to email given, creates
        User obj in db with given data + verification_code.

        Args:
            username (str)
            password (str)
            email (str)
            phone (int)
            profile_pic (bytes)

        Returns:
           True/False, err(None/str)
        """
        output = True
        err = None
        try:
            existing_user = User.get_query('CheckIfUserExists',str(username),str(email))
            if existing_user:
                err , output= 'User with given Username/Email already exist. Please pick different credentials. This is your email? Click "Forgot Passowrd" at Log In.'
                return False, err
            
            code = self._generate_confirmation_code()
            send_email = self.email_handler.send_verification_email(str(email),code)
            if send_email:
                hashed_password = bcrypt.generate_password_hash(str(password)).decode('utf-8')
                create_user = User.add(TenantID=None,
                                       PasswordHash=hashed_password,
                                       Username=str(username),
                                       Email=str(email),
                                       PhoneNum=int(phone),
                                       ProfilePic=profile_pic,
                                       OldHomes=None,
                                       VerificationCode=code)

                if create_user:
                    return True, err
                
            else:
                err , output= "Inernal Error. Please Try Again Later."
                return False, err
        
        except Exception as e:
            err = "Inernal Error. Please Try Again Later."
            output = str(e)
            return False, err
        
        finally:
           self.logger.log('Unlogged','sign_up', (username, email, phone, profile_pic), output) 
           
           
    def verify_email_address(self,email, verification_code):
        """
        27.05.24
        Email confirmation (requred after sign up)
        Find user by eamil (sq), comapre code given with db verification_code, 
        delete verification_code from db (so user will be able to login).

        Args:
            email (str)
            verification_code (int)

        Returns:
            True/False, err(None/str)
        """
        err= None
        try:
            user = User.get_query("GetUserByEmail",email)
            if user:
                db_code = user[0][8]
                user_id = user[0][6]
                if db_code == int(verification_code):
                    delete = User.update(user_id,VerificationCode=None)
                    if delete:
                        output = True
                        return True, err
                    
                    else: 
                        err, output = "Inernal Error. Please Try Again Later."
                        return False,err
                        
                else:
                    err, output = 'Wrong Code!'
                    return False,err
                
            else:
                err, output = "Inernal Error. Please Try Again Later."
                return False,err
                
        except Exception as e:
            err = "Inernal Error. Please Try Again Later."
            output = str(e)
            return False, err
        
        finally:
           self.logger.log('Unlogged','verify_email_address', (email, verification_code), output) 
           
           
    def resend_email(self,email):
        """
        27.05.24
        Resend email with verification code.

        Args:
            email (str)

        Returns:
            True/False
        """
        try:
            user = User.get_query("GetUserByEmail",email)
            if user:
                db_code = user[0][8]
                send_email = self.email_handler.send_verification_email(str(email),db_code)
                
                output = True if send_email else False
                return output
            
            output = False
            return False
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
           self.logger.log('Unlogged','resend_email', email, output)       
    
    
    def forgot_password(self,email):
        """
        27.05.24
        Forgot password finds user by email, creates verification code,
        sends email with verification code and saves verification code
        in db. Creation of verification code in db prevents user to login
        prior to verification. Deltes any login_tokens of the user if exist.

        Args:
            email (str)

        Returns:
            True/False, err(None/str)
        """
        err= None
        try:
            user = User.get_query("GetUserByEmail",email)
            if user:
                user_id = user[0][6]
                code = self._generate_confirmation_code()
                update = User.update(user_id,VerificationCode=code)
                self.login_token.delete_token(user_id)
                    
                send_email = self.email_handler.send_verification_email(str(email),code)
                if send_email and update:
                    output = True
                    return True, err
                
                err, output = "Inernal Error. Please Try Again Later."
                return False,err
            
            err, output = 'No user with Email given.'
            return False,err
            
        except Exception as e:
            err = "Inernal Error. Please Try Again Later."
            output = str(e)
            return False, err
        
        finally:
           self.logger.log('Unlogged','reset_password', email, output)
           
           
    def reset_password(self,email,verification_code,new_pass):
        """
        27.05.24
        Reset Password called after forgot password, finds user
        by email, confirms verification code, hashes new password,
        deletes verification code from db, updates the new pass in db.

        Args:
            email (str)
            verification_code (int)
            new_pass (str)

        Returns:
           True/False, err(None/str)
        """
        err = None
        try:
            user = User.get_query("GetUserByEmail",email)
            if user:
                db_code = user[0][8]
                user_id = user[0][6]
                if db_code == int(verification_code):
                    hashed_password = bcrypt.generate_password_hash(str(new_pass)).decode('utf-8')
                    update = User.update(user_id,VerificationCode=None,PasswordHash=hashed_password)
                    if update:
                        output = True
                        return True, err
                    
                    err, output = "Inernal Error. Please Try Again Later."
                    return False, err
                
                err, output = "Wrong Code!"
                return False, err
            
            err, output = "Inernal Error. Please Try Again Later."
            return False, err
        
        except Exception as e:
            err = "Inernal Error. Please Try Again Later."
            output = str(e)
            return False, err
        
        finally:
           self.logger.log('Unlogged','reset_password', (email, verification_code), output)
        