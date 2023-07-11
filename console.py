#!/usr/bin/python3
"""HBnB console"""

import cmd





class HBNBCommand(cmd.Cmd):
    """ Hbnb command interpreter"""
    prompt = '(hbnb) '

    def emptyline(self):
        """an empty line + ENTER """
        pass

    def do_quit(self, arg):
        """ quit to exit the program """
        return True

    def do_EOF(self, arg):
        """ EOF to exit program """
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
