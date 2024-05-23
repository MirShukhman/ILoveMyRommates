
from . import db
from log.logger import Logger

# 19.05.24
# Abstract class from whom all db models will inherit
# Holds CRUD and defines PK for each db model
# Each use is logged in Logger

logger = Logger()

class BaseModel(db.Model):
    __abstract__ = True 

    ID = db.Column(db.BigInteger, primary_key=True)
    classname = None

    @classmethod
    def get(cls, id):
        """
        19.05.24
        Get obj by obj ID
        Args:
            id (int)
        Returns:
            db model obj/ None if none found/ False if err
        """
        output = None
        try:
            result = cls.query.get(id)
            if result:
                output = result
                return result
            return None

        except Exception as e:
            output = str(e)
            return False
        
        finally:
            logger.log(cls.__name__,'get',id,output)
    
    @classmethod
    def get_all(cls):
        """
        19.05.24
        Get all obj in a model
        Args:
            None
        Returns:
            list of db model objects/ None if none found/ False if err
        """
        output = None
        try:
            result = cls.query.all()
            if result:
                output = result
                return result
            return None
            
        except Exception as e:
            output = str(e)
            return False

        finally:
            logger.log(cls.__name__,'get','all',output)       
        
    @classmethod
    def add(cls, **kwargs):
        """
        19.05.24
        Add obj 
        Args:
            kwargs (column_name = value)
        Returns:
            new db model obj/ False if err
        """
        output = None
        try:
            new = cls(**kwargs)
            db.session.add(new)
            db.session.commit()
            output = new
            return new
        
        except Exception as e:
            db.session.rollback()
            output = str(e)
            return False

        finally:
            logger.log(cls.__name__,'add',kwargs,output)
           
           
    @classmethod
    def update(cls, id, **kwargs):
        """
        19.05.24
        Update obj by ID
        Args:
            id (int)
            kwargs (column_name = new_value)
        Returns:
            updated db model obj/ None if none found/ False if err
        """
        output = None
        try:
            instance = cls.query.get(id)
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                db.session.commit()
                output = instance
                return instance
            return None
        
        except Exception as e:
            db.session.rollback()
            output = str(e)
            return False

        finally:
            logger.log(cls.__name__,'update',f"ID: {id}, kwargs: {kwargs}",output)


    @classmethod
    def delete(cls, id):
        """
        19.05.24
        Delete obj by ID
        Args:
            id (int)
        Returns:
            True / None if none found/ False if err
        """
        output = None
        try:
            instance = cls.query.get(id)
            if instance:
                db.session.delete(instance)
                db.session.commit()
                output = True
                return True
            return None
        
        except Exception as e:
            db.session.rollback()
            output = str(e)
            return False

        finally:
            logger.log(cls.__name__,'delete',id,output)
         
            
    @classmethod
    def get_stored_procedure(sp_name, parameters):
        output = None
        try:
            placeholders = ', '.join([':%s' % key for key in parameters.keys()])
            query = f"CALL {sp_name}({placeholders})"

            execute  = db.session.execute(query, parameters)
            result = execute.fetchall()

            if result:
                output = result
                return result
            
            return None

        except Exception as e:
            output = str(e)
            return None
        
        finally:
            logger.log('BaseModel','get_stored_procedure',(sp_name, parameters),output)
