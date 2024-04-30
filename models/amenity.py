#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import place


class Amenity(BaseModel, Base):
    """defines the Amenity class"""
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = "amenities"

        name = Column(
                String(128),
                nullable=False
            )

        place_amenities = relationship(
                "Place",
                secondary=place.place_amenity,
                backref='amenities'
            )
    else:
        name = ""
