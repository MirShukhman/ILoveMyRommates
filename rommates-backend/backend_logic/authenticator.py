
import jwt
from app import create_app
from app import bcrypt
from .login_token import LoginToken
from log.logger import Logger

logger = Logger()

class Authenticator:
    def __init__(self, token_id):
        self.token_id = token_id
        self.lt = LoginToken()


    def _fetch_and_decode_jwt(self):
        try:
            db_token = self.lt.get_token(self.token_id)
            if db_token:
                secret_key = create_app().config['SECRET_KEY']
                decoded_data = jwt.decode(db_token, secret_key, algorithms=['HS256'])
                output = decoded_data
                return decoded_data
            
        except Exception as e:
            output = str(e)
            return None
        
        finally:
            logger.log('Authenticator','_fetch_and_decode_jwt', self.token_id, output)
       
        
    def authenticate_user(self, front_end_token):
        try:
            db_token = self.lt.get_token(self.token_id)
            if db_token:
                authentication=bcrypt.check_password_hash(front_end_token, db_token)
                output = authentication
                return authentication

        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('Authenticator','authenticate_user', front_end_token, output)
        
           
    def get_user_id(self):
        try:
            decoded_token= self._fetch_and_decode_jwt()
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
            logger.log('Authenticator','get_user_id', self.token_id, output)
    

    def get_tenant_id(self):
        pass
    
    
    def get_uhome_id(self):
        pass
      
     
    def get_user_name(self):
        pass
        
           
    def get_admin_premmisions(self):
        pass