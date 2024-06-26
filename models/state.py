#!/usr/bin/python3
""" State Module for HBNB project """

import os
import models
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        cities = relationship('City', backref="state", cascade="all, delete")
    else:
        @property
        def cities(self):
            """returns the list of City instances with state_id equals to
            the current State.id"""
            cities = models.storage.all(City).values()
            city_objs = [city for city in cities if self.id == city.state_id]
            return city_objs
