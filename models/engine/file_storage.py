#!/usr/bin/python3

"""Define FileStorage class
"""

import json
from models.base_model import BaseModel
from models.user import User
class FileStorage:
    """Serialize instances to JSON file and deserialize JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """return dict __objects"""
        return self.__objects

    def new(self, obj):
        """set in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """serialize __objects to JSON file"""
        json_dict = {}
        for key, obj in self.__objects.items():
            json_dict[key] = obj.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(json_dict, file)

    def reload(self):
        """Deserialize the JSOn file to __objects"""
        try:
            with open(self.__file_path, 'r') as file:
                json_dict = json.load(file)
                for key, value in json_dict.items():
                    cls_name, obj_id = key.split('.')
                    obj_dict = value
                    obj_dict['__class__'] = cls_name
                    obj = eval(cls_name)(**obj_dict)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def classes(self):
        """Return dict for serialization/deserialization"""
        return{
            'BaseModel': BaseModel,
            'User': User,
        }
