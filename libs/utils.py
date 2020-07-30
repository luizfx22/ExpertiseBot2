from os import system, name
import json

class Eb2Utils:
    # Simple function to clear the console...
    def clear():
        # for windows
        if name == 'nt':
            _ = system('cls')
            _ = system('TITLE Expertise Bot :: Rewrite v0.0.2')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')
