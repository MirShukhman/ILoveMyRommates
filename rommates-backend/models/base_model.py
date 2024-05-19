
from . import db

# 19.05.24
# Abstract class from whom all db models will inherit
# Holds CRUD and defines PK for each db model
# Each use is logged in Logger

class BaseModel(db.Model):
    __abstract__ = True 

    ID = db.Column(db.BigInteger, primary_key=True)
    classname = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classname = self.__class__.__name__

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
        try:
            result = cls.query.get(id)
            if result:
                return result
            return None

        except Exception as e:
            print (str(e))
            return False
    
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
        try:
            result = cls.query.all()
            if result:
                return result
            return None
            
        except Exception as e:
            print (str(e))
            return False
        
        
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
        try:
            new = cls(**kwargs)
            db.session.add(new)
            db.session.commit()
            return new
        
        except Exception as e:
            db.session.rollback()
            print (str(e))
            return False
           
           
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
        try:
            instance = cls.query.get(id)
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                db.session.commit()
                return instance
            return None
        
        except Exception as e:
            db.session.rollback()
            print (str(e))
            return False


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
        try:
            instance = cls.query.get(id)
            if instance:
                db.session.delete(instance)
                db.session.commit()
                return True
            return None
        
        except Exception as e:
            db.session.rollback()
            print (str(e))
            return False
