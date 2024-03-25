#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


if getenv("HBNB_TYPE_STORAGE") == 'db':
    place_amenity = Table(
            'place_amenity',
            Base.metadata,
            Column(
                'place_id',
                String(60),
                ForeignKey('place.id'),
                nullable=False
            ),
            Column(
                'amenity_id',
                String(60),
                ForeignKey('amenity,id'),
                nullable=False
            )
        )


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = "places"

        city_id = Column(
                    String(60),
                    ForeignKey('cities.id'),
                    nullable=False
                )
        user_id = Column(
                    String(60),
                    ForeignKey('users.id'),
                    nullable=False
                )
        name = Column(
                    String(128),
                    nullable=False
                )
        description = Column(
                    String(1024)
                )
        number_rooms = Column(
                    Integer,
                    default=0
                )
        number_bathrooms = Column(
                    Integer,
                    default=0
                )
        max_guest = Column(
                    Integer,
                    default=0
                )
        price_by_night = Column(
                    Integer,
                    default=0
                )
        latitude = Column(
                    Float,
                    nullable=True
                )
        longitude = Column(
                    Float,
                    nullable=True
                )

        reviews = relationship(
                    "Review",
                    cascade="all, delete",
                    backref="place"
                )

        amenities = relationship(
                "Amenity",
                secondary=place_amenity,
                viewonly=False,
                backref='place_amenities'
            )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """returns the list of Review instances with place_id equals
                to the current Place.id
            """
            result = []
            for obj in storage.all("Review").values():
                if self.id == obj.place_id:
                    result.append(obj)
            return result

        @property
        def amenities(self):
            """returns the list of Amenity instances based on the attribute
               amenity_ids that contains all Amenity.id linked to the Place
            """
            result = []
            for amenity in storage.all(Amenity).values():
                if amenity.id in amenity_ids:
                    result.append(amenity)
            return result

        @amenities.setter
        def amenities(self, obj):
            """handles append method for adding an Amenity.id to the attribute
               amenity_ids. Only accept Amenity object
            """
            if obj and obj.__name__ == "Amenity":
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
