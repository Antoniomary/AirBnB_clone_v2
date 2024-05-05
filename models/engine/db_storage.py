#!/usr/bin/python3
"""A modulde for a DBStorage"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """a DB engine class"""
    __engine = None
    __session = None

    def __init__(self):
        """create the engine"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        try:
            self.__engine = create_engine(
                    "mysql+mysqldb://{}:{}@{}/{}"
                    .format(user, pwd, host, db), pool_pre_ping=True
                )
            if getenv("HBNB_ENV") == "test":
                Base.metadata.drop_all(self.__engine)
        except Exception as e:
            print(f"Error: {e}")

    def all(self, cls=None):
        """query database session"""
        result = {}
        classes = {
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }
        if cls:
            objects = self.__session.query(classes[cls])
            for each in objects:
                result[cls + '.' + each.id] = each
        else:
            for cls in classes:
                try:
                    objects = self.__session.query(classes[cls])
                    for each in objects:
                        result[cls + '.' + each.id] = each
                except Exception:
                    pass

        return result

    def new(self, obj):
        """add the object to current db session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from the current db session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reloads date saved to db storage"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
            )
        self.__session = scoped_session(session_factory)

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
