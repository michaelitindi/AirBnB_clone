#!/usr/bin/python3
"""HBnB console"""
import cmd
import json
from models.base_model import BaseModel
from models import storage
import models
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.city import City

class HBNBCommand(cmd.Cmd):
    """ Hbnb command interpreter"""
    prompt = '(hbnb) '
    classes = {"BaseModel",
               "User",
               "Place",
               "Amenity",
               "Review",
               "State",
               "City"}

    def emptyline(self):
        """an empty line + ENTER """
        pass

    def do_quit(self, arg):
        """ quit to exit the program """
        return True

    def do_EOF(self, arg):
        """ EOF to exit program """
        print() #print new line b4 exit
        return True
    
    def default(self, line):
        """Handles default behavior for unknown commands"""
        parts = line.split('.')
        if len(parts) == 2:
            class_name = parts[0]
            method, args = parts[1].split('(')
            args = args.strip(')')
            if class_name in self.classes:
                if method == 'all':
                    instances = [str(obj) for obj in storage.all().values() if obj.__class__.__name__ == class_name]
                    print(instances)
                elif method == 'count':
                    count = sum(1 for obj in storage.all().values() if obj.__class__.__name__ == class_name)
                    print(count)
                elif method == 'show':
                    if args.startswith('"') and args.endswith('"'):
                        instance_id = args.strip('"')
                        key = class_name + '.' + instance_id
                        if key in storage.all():
                            print(storage.all()[key])
                        else:
                            print("** no instance found **")
                    else:
                        instances = [str(obj) for obj in storage.all().values() if obj.__class__.__name__ == class_name]
                        filtered_instances = [instance for instance in instances if instance.lower().find(args.lower()) != -1]
                        if filtered_instances:
                            print(filtered_instances)
                        else:
                            print("** no instance found **")
                elif method == 'destroy' and args:
                    instance_id = args.strip('"')
                    key = class_name + '.' + instance_id
                    if key in storage.all():
                        storage.all().pop(key)
                        storage.save()
                    else:
                        print("** no instance found **")
                elif method == 'update' and args:
                    instance_id = args.split(',')[0].strip().strip('"')
                    dictionary_str = args.split(',', 1)[1].strip()
                    try:
                        dictionary = json.loads(dictionary_str)
                        key = class_name + '.' + instance_id
                        if key in storage.all():
                            obj = storage.all()[key]
                            for attr, value in dictionary.items():
                                setattr(obj, attr, value)
                            obj.save()
                        else:
                            print("** no instance found **")
                    except json.JSONDecodeError:
                        print("** Invalid dictionary representation **")
                else:
                    print(f"** Unknown method: {method} **")
            else:
                print(f"** Unknown class: {class_name} **")
        else:
            print(f"*** Unknown syntax: {line} ***")

    def do_create(self, arg):
        """Create a new instance of BaseModel, saves it, and prints the id"""
        if not arg:
            print("** class name missing **")
        elif arg not in self.classes:
            print("** class doesn't exist **")
        else:
            class_name = arg
            new_obj = eval(class_name)()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, arg):
        """print the string repof an instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """delete an instance based on class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key in storage.all():
                storage.all().pop(key)
                storage.save()
            else:
                print("** no instance found **")

    def do_count(self, arg):
        """Retrieve the number of instances of a class"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            count = sum(1 for obj in storage.all().values() if obj.__class__.__name__ == args[0])
            print(count)

    def do_all(self, arg):
        """print all string rep of instances"""
        objs = storage.all().values()
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
        else:
            print([str(obj) for obj in objs])

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in models.storage.all():
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return

        obj = models.storage.all()[key]
        attribute_name = args[2]
        attribute_value = args[3]

        # Handle the case where the attribute does not exist in the class
        if attribute_name not in obj.__dict__:
            print("** attribute doesn't exist **")
            return

        # Update the attribute value
        setattr(obj, attribute_name, type(getattr(obj, attribute_name))(attribute_value))
        obj.save()



if __name__ == '__main__':
    HBNBCommand().cmdloop()
