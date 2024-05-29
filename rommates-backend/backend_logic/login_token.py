import jwt
from app import create_app
from app import bcrypt
from datetime import datetime, timedelta
from models.tokens import Token
from log.logger import Logger

logger = Logger()

# 23.05.24
# LoginToken class will handle all token-related activity: creation of token 
#   and saving to db, retriving from db and deletion.
# Each use is logged in Logger

class LoginToken:
    def __init__(self):
        pass
    
    def generate_token(self, user_id, tenant_id, 
                       home_id, name, premmisson):
        """
        23.05.24
        Create Token, hash token for db, check if old token 
        for user id exists if so delete, save hashed token to db,
        return front_end_token.

        Args:
            user_id (int)
            tenant_id (int)
            home_id (int)
            name (str)
            premmisson (int): 0 or 1 (bool)

        Returns:
            front_end_token/ False
        """
        output = True
        try:
            token = jwt.encode(
                {'user_id': user_id,
                'tenant_id': tenant_id,
                'home_id': home_id,
                'name': name,
                'is_admin_tennant': premmisson},
                create_app().config['SECRET_KEY'],
                algorithm='HS256'
            )
            
            hashed_token = bcrypt.generate_password_hash(token).decode('utf-8')
            
            # add hashed token to db 
            now = datetime.now()
            three_hours_later = now + timedelta(hours=3)
            
            # check if old token exists, if so delete
            existing_token = Token.get_query('GetTokenByUserID',user_id)
            if existing_token:
                Token.delete(existing_token[0][0])
                
            add_to_db = Token.add(UserID=user_id, Token=hashed_token, 
                                CreatedAt=now, ExpiresAt=three_hours_later)
            if add_to_db:
                # return token to be saved in frontend
                return token
            
            output = False
            return False
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('LoginToken','generate_token',(user_id, name, premmisson),output)
    
    
    def get_token(self, user_id):
        """
        23.05.24
        Find db token by user id

        Args:
            user_id (int)

        Returns:
            db token/ False
        """
        try:
            token = Token.get_query('GetTokenByUserID',user_id)
            output = token
            if token:
                return token
                
            return None
            
        except Exception as e:
            output = str(e)
            return None
        
        finally:
            logger.log('LoginToken','get_token',user_id,output)
    
    
    def delete_token(self, user_id):
        """
        23.05.24
        Delete token using user_id

        Args:
            user_id (int)

        Returns:
            True/ False
        """
        try:
            token = Token.get_query('GetTokenByUserID',user_id)
            token_id=token[0][0]
            delete = Token.delete(token_id)
            output = delete
            return delete
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('LoginToken','delete_token',user_id,output)