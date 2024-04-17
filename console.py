#!/usr/bin/python3
"""My console """

import cmd
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex 

model_classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
                 "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def parse_key_value_pairs(self, args):
        """creates a dictionary from a list of strings"""
        key_value_dict = {}
        for arg in args:
            if "=" in arg:
                key_value_pair = arg.split('=', 1)
                key = key_value_pair[0]
                value = key_value_pair[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                key_value_dict[key] = value
        return key_value_dict

    def do_create(self, arg):
        """Creates a new instance of a class"""
        arguments = arg.split()
        if len(arguments) == 0:
            print("** class name missing **")
            return False
        if arguments[0] in model_classes:
            new_dict = self.parse_key_value_pairs(arguments[1:])
            instance = model_classes[arguments[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        arguments = shlex.split(arg)
        if len(arguments) == 0:
            print("** class name missing **")
            return False
        if arguments[0] in model_classes:
            if len(arguments) > 1:
                key = arguments[0] + "." + arguments[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        arguments = shlex.split(arg)
        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] in model_classes:
            if len(arguments) > 1:
                key = arguments[0] + "." + arguments[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        arguments = shlex.split(arg)
        object_list = []
        if len(arguments) == 0:
            object_dict = models.storage.all()
        elif arguments[0] in model_classes:
            object_dict = models.storage.all(model_classes[arguments[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in object_dict:
            object_list.append(str(object_dict[key]))
        print("[", end="")
        print(", ".join(object_list), end="")
        print("]")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        arguments = shlex.split(arg)
        integer_attributes = ["number_rooms", "number_bathrooms", "max_guest",
                              "price_by_night"]
        float_attributes = ["latitude", "longitude"]
        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] in model_classes:
            if len(arguments) > 1:
                key = arguments[0] + "." + arguments[1]
                if key in models.storage.all():
                    if len(arguments) > 2:
                        if len(arguments) > 3:
                            if arguments[0] == "Place":
                                if arguments[2] in integer_attributes:
                                    try:
                                        arguments[3] = int(arguments[3])
                                    except:
                                        arguments[3] = 0
                                elif arguments[2] in float_attributes:
                                    try:
                                        arguments[3] = float(arguments[3])
                                    except:
                                        arguments[3] = 0.0
                            setattr(models.storage.all()[key], arguments[2], arguments[3])
                            models.storage.all()[key].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()

