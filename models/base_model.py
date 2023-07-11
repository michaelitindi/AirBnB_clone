#!/usr/bin/python3
"""
Define the BaseModel class
"""

import uuid
from datetime import datetime
import models

class BaseModel:
    """
    Define common attributes and methods for other classes
    """
    def __init__(self, *args, **kwargs):
        """initialize a new instance of BaseModel"""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                elif key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())

        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at =datetime.now()
            #from models import storage
            models.storage.new(self)

    def save(self):
        """update attribute updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """return dict rep. of the object"""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict

    def __str__(self):
        """Return a string rep of the object"""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def __repr__(self):
        """ Return string representation of an object """
        return str(self)
