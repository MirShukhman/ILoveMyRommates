
from app import bcrypt
from datetime import datetime

from .unlogged import Unlogged
from backend_logic.authenticator import Authenticator
from backend_logic.bookkeeper import Bookkeeper
from models.users import User
from models.tenants import Tenant
from models.homes import Home

# 29.05.24
# Class AllTenants Facade will hold funcs avilable to every user.
# Inherits from Ulogged Class to acess some of its functionality.

class AllTenants(Unlogged):
    def __init__(self):
        super().__init__()
        self.authenticator = Authenticator()
        self.bookkeeper = Bookkeeper()  
    
      
    def _get_authentication(self,front_end_token):
        user_id = self.authenticator.authenticate_user(str(front_end_token))
        self.logger.log('Tenant','get_authentication',front_end_token,user_id)
        return user_id        
        
    
    def _get_users_home_id(self,front_end_token):
        home_id = self.authenticator.get_home_id(str(front_end_token))
        self.logger.log('Tenant','_get_users_home_id',front_end_token,home_id)
        return home_id
    
    
    def _get_users_tenant_id(self,front_end_token):
        tenant_id = self.authenticator.get_tenant_id(str(front_end_token))
        self.logger.log('Tenant','_get_users_tenant_id',front_end_token,tenant_id)
        return tenant_id
    
    
    def get_users_name(self,front_end_token):
        name = self.authenticator.get_user_name(str(front_end_token))
        if name:
            return name

    
    def get_user(self,user_id):
        user = User.get(user_id)
        self.logger.log('Tenant','get_user',user_id,user)
        return user 
    
    
    def logout(self,front_end_token):
        """
        27.05.24
        Logout authentictes user and deletes token from db.

        Args:
            front_end_token (str)

        Returns:
            True/False
        """
        try:
            user_id = self._get_authentication(front_end_token)
            if not user_id:
                output = False
                return False
            
            logout = self.login_token.delete_token(user_id)
            output = True if logout else False
            return output
            
        except Exception as e:
            output = str(e)
            return False
            
        finally:
            self.logger.log('Tenant','logout',front_end_token,output)
            
            
    def update_profile(self, front_end_token, password, username,
                       phone, pic, name):
        """
        28.05.24
        Update users personal data, requres users password
        for update. Checks pass, updates user and tenant in db accordingly.

        Args:
            front_end_token (str)
            password (str)
            username (str)
            phone (int)
            pic (bytes)
            name (str)

        Returns:
           True/False, err(None/str)
        """
        err = None
        try:
            user_id = self._get_authentication(front_end_token)
            if user_id:
                db_pass = User.get(user_id).PasswordHash
                ok = self._check_password(db_pass, password)
                if not ok:
                    err, output = 'Wrong Password'
                    return False, err
                
                update_user = User.update(Username=username, PhoneNum =phone,
                                          ProfilePic= pic)
                if name:
                    update_tennant = Tenant.update(Name = name)
                    if update_user and update_tennant:
                        output = True
                        return True, err
                    
                if update_user:
                    output = True
                    return True, err
                
            err, output = "Internal Error. Please Try Again Later."
            return False, err
     
        except Exception as e:
            err = "Internal Error. Please Try Again Later."
            output = str(e)
            return False, err
            
        finally:
            self.logger.log('Tenant','update_profile',(front_end_token,username,phone,name),output)
    
    
    def update_email(self, front_end_token, password, new_email):
        err = None
        try:
            user_id = self._get_authentication(front_end_token)
            if user_id:
                db_pass = User.get(user_id).PasswordHash
                ok = self._check_password(db_pass, password)
                if not ok:
                    err, output = 'Wrong Password'
                    return False, err
                
                existing_user = User.get_query('GetUserByEmail',str(new_email))
                if existing_user:
                    err , output= 'User with given Email already exist. Please pick different credentials.'
                    return False, err
                
                code = self._generate_confirmation_code()
                send_email = self.email_handler.send_verification_email(str(new_email),code)
                update_user = User.update(Email=new_email)
                    
                if update_user and send_email:
                    output = True
                    return True, err
                
            err, output = "Internal Error. Please Try Again Later."
            return False, err
     
        except Exception as e:
            err = "Internal Error. Please Try Again Later."
            output = str(e)
            return False, err
            
        finally:
            self.logger.log('Tenant','update_email',(front_end_token,new_email),output)
    
    
    def update_password(self, front_end_token, old_password, new_password):
        err = None
        try:
            user_id = self._get_authentication(front_end_token)
            if user_id:
                db_pass = User.get(user_id).PasswordHash
                ok = self._check_password(db_pass, old_password)
                if not ok:
                    err, output = 'Wrong Password'
                    return False, err
                
                hashed_new_pass = bcrypt.generate_password_hash(str(new_password)).decode('utf-8')
                update_user = User.update(PasswordHash=hashed_new_pass)
                    
                if update_user:
                    output = True
                    return True, err
                
            err, output = "Internal Error. Please Try Again Later."
            return False, err
     
        except Exception as e:
            err = "Internal Error. Please Try Again Later."
            output = str(e)
            return False, err
            
        finally:
            self.logger.log('Tenant','update_password',(front_end_token),output)    
    
    
    def add_self_as_first_tenant(self,front_end_token):
        pass
    
    
    def add_home(self, front_end_token, home_name, billing_date):
        err = None
        try:
            user_id = self._get_authentication(front_end_token)
            if user_id:
                now = datetime.now()
                add_home = Home.add(HomeName=home_name, CreatedAt=now,
                                    BillingDate = billing_date, IsActive=True)
                
                if add_home:
                        output = True
                        return True, err
            
            err, output = "Internal Error. Please Try Again Later."
            return False, err
        
        except Exception as e:
            err = "Internal Error. Please Try Again Later."
            output = str(e)
            return False, err    
            
        finally:
           self.logger.log('Tenant','add_home',(front_end_token,home_name,billing_date),output)  
    
    
    def leave_home(self,front_end_token):
        err = None
        try:
            user_id = self._get_authentication(front_end_token)
            home_id = self._get_users_home_id(front_end_token)
            tenant_id = self._get_users_tenant_id(front_end_token)
            if user_id and home_id and tenant_id:
                now = datetime.now()
                new_json = {"HomeID": home_id,
                            "TenantID": tenant_id,
                            "LeftAt": now}
                leave_home = User.update(OldHomes=new_json, TenantID=None)
                if leave_home:
                    recalculate = self.bookkeeper.recalculate_payment_part_after_tenant_leaving(home_id,tenant_id)
                    if recalculate:
                        output = True
                        return True, err
            
            err, output = "Internal Error. Please Try Again Later."
            return False, err
        
        except Exception as e:
            err = "Internal Error. Please Try Again Later."
            output = str(e)
            return False, err    
            
        finally:
           self.logger.log('Tenant','leave_home',(front_end_token),output)  
               
    
    def find_home_by_id(self, home_id):
        pass
    
    
    def ask_to_join_home(self,front_end_token,home_id):
        pass
    
    
    def view_old_homes(self, front_end_token):
        pass
    
    
    def view_all_bills(self, front_end_token):
        pass
    
    
    def view_bill_by_date(self, front_end_token, start_date, end_date):
        pass
    
    
    def view_set_bills(self, front_end_token):
        pass
    
    
    def view_all_home_payments(self, front_end_token):
        pass
    
    
    def view_home_payments_by_date(self, front_end_token, start_date, end_date):
        pass
    
    
    def add_payment(self, front_end_token, paid_to,
                    bill_id, sum, image, external_id):
        pass
    
    
    def update_my_payment(self, front_end_token, payment_id, paid_to,
                        bill_id, sum, image, external_id):
        pass
    
    
    def delete_my_payment(self, front_end_token, payment_id):
        pass
    
    
    def approve_payment(self, front_end_token, payment_id):
        pass
    
    
            
