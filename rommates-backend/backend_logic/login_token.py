import jwt
from app import create_app
from app import bcrypt
from datetime import datetime, timedelta
from models.tokens import Token
from log.logger import Logger

logger = Logger()

# 23.05.24
# LoginToken class will handle all token-related activity- creation of token and saving to db, 
#   retriving from db and deletion.
# Each use is logged in Logger

class LoginToken:
    def __init__(self):
        pass
    
    def generate_token(self, user_id, tenant_id, 
                       home_id, name, premmisson):
        """
        23.05.24
        Create Token, hash front_end_token, 
        save token to db, return front_end_token and db token id.

        Args:
            user_id (int)
            tenant_id (int)
            home_id (int)
            name (str)
            premmisson (int): 0 or 1 (bool)

        Returns:
            token_id and front_end_token/ False
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
            
            # create hashed frontend token 
            front_end_token = bcrypt.generate_password_hash(token).decode('utf-8')
            
            # add token to db 
            now = datetime.now()
            three_hours_later = now + timedelta(hours=3)
            add_to_db = Token.add(UserID=user_id, Token=token, 
                                CreatedAt=now, ExpiresAt=three_hours_later)
            if add_to_db:
                return add_to_db.ID, front_end_token
            
            output = False
            return False
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('LoginToken','generate_token',(user_id, name, premmisson),output)
    
    
    def get_token(self, token_id):
        """
        23.05.24
        Find token by id

        Args:
            token_id (int)

        Returns:
            token/ False
        """
        try:
            token = Token.get(token_id)
            output = token
            if token:
                return token.Token
                
            return None
            
        except Exception as e:
            output = str(e)
            return None
        
        finally:
            logger.log('LoginToken','get_token',(token_id),output)
    
    
    def delete_token(self, token_id):
        """
        23.05.24
        Delete token by id

        Args:
            token_id (int)

        Returns:
            True/ False
        """
        try:
            delete = Token.delete(token_id)
            output = delete
            return delete
            
        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log('LoginToken','delete_token',(token_id),output)