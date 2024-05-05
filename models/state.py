#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'states'

        name = Column(
                String(128),
                nullable=False
            )

        cities = relationship('City', cascade='all, delete', backref='state')
    else:
        name = ""

        @property
        def cities(self):
            """returns the list of City instances with equal state_id"""
            from models import storage
            city = []
            for obj in storage.all("City").values():
                if obj.state_id == self.id:
                    city.append(obj)
            return city
