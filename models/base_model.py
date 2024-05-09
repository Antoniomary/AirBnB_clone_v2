#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(
                String(60),
                nullable=False,
                primary_key=True
            )
        created_at = Column(
                DateTime,
                nullable=False,
                default=datetime.utcnow
            )
        updated_at = Column(
                DateTime,
                nullable=False,
                default=datetime.utcnow
            )

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if kwargs:
            for k, v in kwargs.items():
                if k == 'updated_at':
                    kwargs[k] = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
                elif k == 'created_at':
                    kwargs[k] = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
            if kwargs.get('__class__'):
                del kwargs['__class__']
            if not kwargs.get('created_at') and not kwargs.get('updated_at'):
                kwargs['created_at'] = datetime.now()
                kwargs['updated_at'] = datetime.now()
            if not kwargs.get('id'):
                kwargs['id'] = str(uuid.uuid4())
            self.__dict__.update(kwargs)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.to_dict())

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        if getenv("HBNB_TYPE_STORAGE") != 'db':
            dictionary.update(
                    {'__class__':
                        (str(type(self)).split('.')[-1]).split('\'')[0]}
                    )
            dictionary['created_at'] = self.created_at.isoformat()
            dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        from models import storage
        storage.delete(self)
