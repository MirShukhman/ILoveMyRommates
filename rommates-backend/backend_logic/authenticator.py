
import jwt
from app import create_app
from app import bcrypt
from .login_token import LoginToken
from log.logger import Logger

logger = Logger()

# 24.05.24
# Authenticator class will handle user authentication and premmisions
#   using login token.
# Each use is logged in Logger

class Authenticator:
    def __init__(self):
        self.lt = LoginToken()


    def _decode_frontend_token(self, front_end_token):
        """
        24.05.24
        Decode jwt encoded token to dict

        Args:
            front_end_token (str)

        Returns:
            decoded_data(dict)/ None
        """
        try:
            secret_key = create_app().config['SECRET_KEY']
            decoded_data = jwt.decode(front_end_token, secret_key, algorithms=['HS256'])
            output = decoded_data
            return decoded_data
            
        except Exception as e:
            output = str(e)
            return None
        
        finally:
            logger.log('Authenticator','_decode_frontend_token', front_end_token, output)
       
        
    def authenticate_user(self, front_end_token):
        """
        24.05.24
        Get user authetication using front_end_token
        Extracts user_id from front_end_token, gets hashed db token 
        using user_id, if match returns user_id
        
        Args:
            front_end_token (str)

        Returns:
            user_id/ False
        """
        try:
            user_id = self._get_user_id(front_end_token)
            if user_id:
                db_token = self.lt.get_token(user_id)
                if db_token:
                    authentication=bcrypt.check_password_hash(db_token, front_end_token)
                    output = authentication
                    return user_id

        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('Authenticator','authenticate_user', front_end_token, output)
        
           
    def _get_user_id(self,front_end_token):
        """
        24.05.24
        Extract user_id from front_end_token

        Args:
            front_end_token (str)

        Returns:
            user_id/ False
        """
        try:
            decoded_token= self._decode_frontend_token(front_end_token)
            if decoded_token:
                user_id = decoded_token.get('user_id', None)
                output = user_id
                return user_id
            
            output = False
            return False
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('Authenticator','get_user_id', front_end_token, output)
    

    def get_tenant_id(self,front_end_token):
        """
        24.05.24
        Extract tenant_id from front_end_token

        Args:
            front_end_token (str)

        Returns:
            tenant_id/ False
        """
        try:
            decoded_token= self._decode_frontend_token(front_end_token)
            if decoded_token:
                tenant_id = decoded_token.get('tenant_id', None)
                output = tenant_id
                return tenant_id
            
            output = False
            return False
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('Authenticator','get_tenant_id', front_end_token, output)    
    
    
    def get_home_id(self,front_end_token):
        """
        24.05.24
        Extract home_id from front_end_token

        Args:
            front_end_token (str)

        Returns:
            home_id/ False
        """
        try:
            decoded_token= self._decode_frontend_token(front_end_token)
            if decoded_token:
                home_id = decoded_token.get('home_id', None)
                output = home_id
                return home_id
            
            output = False
            return False
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('Authenticator','get_home_id', front_end_token, output)      
     
     
    def get_user_name(self,front_end_token):
        """
        24.05.24
        Extract name from front_end_token

        Args:
            front_end_token (str)

        Returns:
            name/ False
        """
        try:
            decoded_token= self._decode_frontend_token(front_end_token)
            if decoded_token:
                name = decoded_token.get('name', None)
                output = name
                return name
            
            output = False
            return False
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('Authenticator','get_user_name', front_end_token, output)        
           
           
    def get_admin_premmisions(self,front_end_token):
        """
        24.05.24
        Extract user premmisions from front_end_token

        Args:
            front_end_token (str)

        Returns:
            True (if admin)/ False (if not admin/err)
        """
        try:
            decoded_token= self._decode_frontend_token(front_end_token)
            if decoded_token:
                is_admin_tennant = decoded_token.get('is_admin_tennant', None)
                output = True if is_admin_tennant == 1 else False
                return output
            
            output = False
            return False
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('Authenticator','get_admin_premmisions', front_end_token, output)