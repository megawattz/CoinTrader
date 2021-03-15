# Generic Utility Functions

import os
import re
import json
import pprintpp
import inspect
import traceback

# Take a list of values, a list of keys (name) and maps the values to the keys
# in the same order into a dictionary. Current is an already existing
# dictionary to be modified or added to. If there are more values than keys,
# the extra values are stuck into a list under the single key named by the
# leftovers parameter. If leftovers is not set, excess values are
# discarded. Excess keys discarded. This is useful when composing arguments to
# functions arranged into a dictionary
#
"""
Example:
                    VALUES                                           KEYS                  CURRENT FAMILY              LEFTOVER (all go under same key)
family = ListToDict(["Donald", "Nancy", "Billy", "Jonie", "Peewee"], ["Father", "Mother"], {"Pets":["Fido","Fluffy"]}, "Kids")
family = {
    "Pets:":["Fido", "Fluffy"],
    "Father":"Donald",
    "Mother":"Nancy",
    "Kids":["Billy", "Jonie", "Peewee"]
    } 
The Pets might be considered the defaults, they are already in the dictionary (but could be overwritten)
The Father and Mother are specifically named (only one of each)
The Kids all go under the leftover key, i.e. they do not have specific family positions
"""

def ListToDict(valueList, keyList, current = {}, leftovers = None):
    minlen = min(len(keyList), len(valueList)) # iterate the least of these two numbers
    for i in range(minlen):
        current[keyList[i]] = valueList[i]
    
    if valueList[minlen:] and leftovers:  # if we had more values than keys available, put the remaining values into the key leftovers as a list
        current[leftovers] = valueList[minlen:]
        
    return current        

# support a common type config file, JSON
def ReadJSONFile(filename):
    with open(filename) as json_file: 
        data = json.load(json_file) 
    return data

# function that called me (exclude caller)
def Stack(start = 0, finish = 9999):
    stack = inspect.stack()
    rval = []
    for index in range(start, min(finish, len(stack))):
        rval.append("%s:%s" % (os.path.basename(stack[index].filename), stack[index].lineno))
    return rval

#singleton, only one per app
# Log levels 0 always, 1 error, 2 warnings, 3 normal, 4 extra, 5 debug, 6 all
LogLevel = 6
def Log(*args):
    elements = args[1:]
    triviality = 3
    if type(elements[0]) == 'int':
        triviality = elements[0]
        del elements[0]
    if triviality > LogLevel and LogLevel < 6:
        return
    print(Stack(2, 3), ":", *elements)

def Output(*args):
    print(*args)
    
Formats = {"json":1,"pretty":1,"text":1}
Format = {"format":"pretty", "arg": 0}

def SetFormat(args):
    global Format, Formats
    if not format in args:
        return Format
    if not args['format'] in Formats:
        raise("Allowed formats:[]" % Formats.keys())
    Format =  {"format": args['format'], "arg":args['value']}
    return Format

# All textual output for the user should be piped through this.  The user can
# set the format he wants to see so all output should be done through this
def FormatContent(toshow):
    global Format, Formats
    method = Format['format'];
    param = Format['arg']
    if method == 'json':
        return json.dumps(toshow, indent=param)
    else:
        if method == 'pretty':
            return pprintpp.pformat(toshow, indent=param)
        else:
            return(toshow)

def FormatException(e):
    return FormatContent(e, traceback.format_tb(e[2]))

class TraderException(Exception):
    def __init__(self, description):
        super().__init__(description)
    
if __name__ == "__main__":
    print(Stack())
