#!/usr/bin/python3
"""this module holds a class that defines a mysql db storage"""

from os import environ
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# maps class names to corresponding model classes
all_clss = {
    'BaseModel': BaseModel,
    'User': User, 'City': City,
    'State': State, 'Place': Place,
    'Amenity': Amenity, 'Review': Review
    }


class DBstorage:
    """defines Mysql database storage"""

    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the DBStorage instance.
        -----------------------------------
        Sets up the SQLAlchemy engine & session based on environment variables.
        Drops all tables if environment variable HBNB_ENV is equal to 'test'.
        """
        db = environ['HBNB_MYSQL_DB']
        user = environ['HBNB_MYSQL_USER']
        host = environ['HBNB_MYSQL_HOST']
        paswd = environ['HBNB_MYSQL_PWD']

        db_url = f"mysql+mysqldb://{user}:{paswd}@{host}/{db}"

        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if environ['HBNB_ENV'] == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query all objects from the database session.
        Args:
            cls (str): Optional class name to filter results.
        """
        obj_dict = {}

        if cls:
            the_cls = all_clss[cls]
            quried_cls = self.__session.query(the_cls).all()
            for obj_val in quried_cls:
                obj_key = f"{type(obj_val).__name__}.{obj_val.id}"
                obj_dict[obj_key] = obj_val
            return obj_dict
        else:
            for clss in all_clss.values():
                cls_queried = self.__session.query(clss).all()
                for obj_v in cls_queried:
                    obj_dict[f'{type(obj_v).__name__}.{obj_v.id}'] = obj_v
            return obj_dict

    def new(self, obj):
        """Add an object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session."""
        if obj:
            self.__session.delete(obj)
 
    def reload(self):
        """Reload the database setup and create a new session."""
        engine = Base.metadata.create_all(self.__engine)
        ss_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(ss_factory)
        self.__session = Session()
