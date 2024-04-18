#!/usr/bin/python3
"""ontains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

model_classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
                 "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects_dict = {}

    def all_objects(self, cls=None):
        """returns the dictionary __objects_dict"""
        if cls is not None:
            filtered_dict = {}
            for key, value in self.__objects_dict.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    filtered_dict[key] = value
            return filtered_dict
        return self.__objects_dict

    def add_new_object(self, obj):
        """sets in __objects_dict the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects_dict[key] = obj

    def save_objects(self):
        """serializes __objects_dict to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects_dict:
            json_objects[key] = self.__objects_dict[key].to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(json_objects, file)

    def reload_objects(self):
        """deserializes the JSON file to __objects_dict"""
        try:
            with open(self.__file_path, 'r') as file:
                json_objects = json.load(file)
            for key in json_objects:
                self.__objects_dict[key] = model_classes[json_objects[key]["__class__"]](**json_objects[key])
        except:
            pass

    def delete_object(self, obj=None):
        """delete obj from __objects_dict if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects_dict:
                del self.__objects_dict[key]

    def close_storage(self):
        """call reload_objects() method for deserializing the JSON file to objects"""
        self.reload_objects()

