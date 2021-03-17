# git_info: 0.1 1d5a57b trader 03/01/21-22:38:48-EST-0500

# The intent of this file is to serve as the interface between the UIs
# And the exchanges. It's the "Controller" of the Model-View-Controller paradigm
# This will be expanded at some point to use the network so the application can be
# distributed even having multiple user interfaces active at the same time.

import os
import re
import sys
import traceback
import json
import Util
import inspect

# A "Model" is a tangible entity we have coded up like an Exchange, or a
# UserInterface. In an object oriented sense we might say the Base Class is the
# abstract, idealized form of the model. Derived classes of that model we want
# to be able to add dynamically by writing a module and putting it into a
# directory without having to change the code of the entire system. We call
# this a Plugin. Each Plugin is a subclass/derivedclass/child class, of a base
# class model. The model should be a good description of the type of thing
# being represented.  So the base class "Exchange" has derived classes
# "Binance" and "Coinbase" that a plugins and can be added to the system by
# just "plugging them in". Our UserInterface base class, only has one derived
# class currently, the "TextUserInterface" plugin.  Each plugin class should
# have the same interface (member functions) as its base class. Since each
# derived class will have the same functions as the base class, the system
# doesn't have to know which particular plugin it is dealing with and so
# commands can apply to all instances of plugins, and new plugins can be placed
# into the system without requiring code changes to the framework, they will
# just work. Like plugging in any USB device to any USB socket.

# A Model is a simplified, idealized representation of something we want to
# emulate inside the computer. For trading cryptos and other things we have
# models of Exchanges, maybe securities, crypto coins, User Interfaces etc.
# These are the current types of models we have in this code so far (see below
# dictionary). Each of these has a base class file called Exchange.py or
# UserInterface.py.  For each base class we can have an unlimited number of
# derived classes we create in python code modules, files, we generally refer
# to as plugins, slightly different cases of the same type of thing. Like
# Binance and Coinbase are different, yet they are both Exchanges where you
# essentially perform the same tasks, buy and sell crypto coins, and so they
# have the same "Interface" for our purposes. The "Interface" is simply the
# list of functions they make available to users of those classes. The only
# functions that will be useful in those derived classes will be the functions
# that exist in the Base class. If a derived class cannot perform a function
# that a base class has, then the base class version will normally be called
# and throw an exception which is just displayed to the user (depends on
# setting) and isn't normally a problem unless the user was depending on that
# function (like "Sell Everything!!!!"). Some functions are meant to live in
# the base class. These are functions common to all the derived classes and
# having one copy in the base class prevents excessive complexity and code. So
# try to make every derived class able to keep its promise to the user of what
# it's going to do. Functions that are performed by the base class don't have
# to be implemented in the derived class unless the derived class needs to do
# that function differently for some reason.  For the sake of keeping the code
# simple, try not to duplicate functions in derived classes. If something is
# done in all derived classes, simply put one copy of it in the base class. If
# a function is called and does not exist in the derived class, the bass class
# will automagically be searched for that function name and will be satisfied
# there.

from Config import Config

Config = Config("Controller")

Plugins = {}

# All the objects of those types are kept in those dictionaries. Like all
# UserInterfaces are kept in the Plugins['UserInterface'] dictionary. When a
# command is issued to the UI from one of the user interfaces, the response is
# broadcast to all of them. This lets you have multiple copies of the program
# open but still be talking to the same world. If an exchange commnand is
# issued like "Buy Bitcoin" an exchange, or exchanges are specified and the
# command will go do all the the exchanges. This way for example, you can set a
# very low limit order, to watch for flash crashes, on every exchange and a
# list of coins, with just one command: "TriggerMarket
# Coinbase,Binance,Huobi,Kucoin BTC:1/USDT,ETH/USDT:10000,LTC/USDT:100 -50%"
# meaning On all those exchanges, watch those coins, for a price drop of
# %50. Make any buy triggered using USDT.  This would watch all those exchanges
# in realtime looking for a crash of the coin by 50% and trigger a
# purchase. BTC:1/USDT means "buy one Bitcoin at market price when the trigger
# executes (price drop of 50%)). ETH/USDT:10000 means "spend 100000 USDT on
# ETH" when or if the trigger executes.
    
ControllerModule = sys.modules[__name__] # gets THIS module, the controller (needs to be passed to UserInterfaces so they can talk to us)

# Loads a module from a filename and instantiates any classes in that module that we want to use as plugins.
def Load(args):
    modname = args['module']
    instanceName = args['name']
    mod = __import__(modname)
    # iterate through all the attributes of the module looking for classes
    for member_name, member in inspect.getmembers(mod):
        # is it a class? does it have base classes?
        if inspect.isclass(member) and member.__bases__:
            for base in member.__bases__:
                # if it's not a base class we are interested in, skip it, it's a general purpose class not a plugin
                if not base.__name__ in Plugins:
                    continue
                Util.Log(4, "Loading module type:%s name:%s module:%s class:%s" % (base.__name__, instanceName, modname, member.__name__))
                instance = member(instanceName)  # create an instance of the class in the module
                Plugins[base.__name__][instanceName] = instance # store it as a living object into the dictionary of that type of thing (clasname, plugin)
                instance.Link(ControllerModule) # tell the plugin where the controller is (me, this Module, is the controller)
                instance.Start() # start the module
                Util.Log(4, "Loaded module:%s %s" % (instanceName, instance))

def LoadPlugins(directory="Plugins/"):
    #fileNames = [fileName for fileName in os.listdir(directory) if re.search('.py$', fileName)]
    #Util.Log(5, "Plugins Config:\n", json.dumps(Plugins, indent=2))
    plugins = Config.Get('Plugins')
    for plugType in plugins:
        Plugins[plugType] = {}
        for name in plugins[plugType]:
            if Config.Get("Plugins.%s.%s.status" % (plugType, name), "enabled") == "disabled":
                continue # cofigured as disabled? skip it
            module = plugins[plugType][name]['plugin']
            #Util.Log(5, "Request Load %s:%s" % (module, name))
            Load({"module":module, "name":name})

# Calls done to the controller            
def Manage(request):
    command = request['command']
    response = ({"source": command, "response":"No command called %s" % command})
    if command == 'ListEntities':
        rval = {}
        for ptype in Plugins:
            rval[ptype] = {}
            for entity in Plugins[ptype]:
                rval[ptype][entity] = Plugins[ptype][entity]
        response = rval

    if command == 'Dump':  # write all internal databases to Cache directory
        from ConfigBase import ConfigBase
        Util.WriteFile("Cache/Config.json", json.dumps(ConfigBase.ConfigData, indent=2))
        from HttpDataFeed import HttpDataFeed
        Util.WriteFile("Cache/HttpDataFeed.json", json.dumps(HttpDataFeed.Info, indent=2))
        response = "Written to Cache/"
        
    for name, ui in Plugins['UserInterface'].items():
        ui.Response({"source": command, "response": response})

# Calls done to plugins

# for linkages done with python code                
def PluginRequest(request):
    #Util.Log(5, "DirectCall:", DirectCall, request)
    return Command(request)

# for linking to controller over networks
def RESTCall(request):
    # not implemented yet
    # answser = Command(request)
    pass

def PluginResponse(source, data):
    # send the answer to each UserInterface
    for name, ui in Plugins['UserInterface'].items():
        #ui = UserInterfaces[name]
        try:
            ui.Response({"source": name, "response": data})
        except Exception as e:
            # if the ui throws, then we have nowhere to send the
            # information except to stderr
            Util.Log(1, "Error:", e)

def Command(request): 
    target = request['target']
    if (target == 'controller'):
        return Manage(request)

    Util.Log(5, "Request:", request)
    command = request['command']
    for ptype in Plugins:
        for name in Plugins[ptype]:
            plugin = Plugins[ptype][name]
            if not re.match(target, plugin.Name()):
                continue # this is not the plugin you are looking for
            data = []
            try:
                func = None
                try:
                    func = getattr(plugin, command)
                except:
                    continue
                item = func(request)
                data.append(item)
            except Exception as e:
                # because this command will be going to multiple exchanges, we
                # cant end processing of this loop at the first error, we we stringinze
                # the exception as a return value, so we can send it to each listening UI
                info = sys.exc_info()
                #Util.Log(5, "Error:", e)
                data.append({"error": info[1], "stack": traceback.print_tb(info[2])})
                
            PluginResponse(name, data)
                
    
if __name__ == "main":
    print(len(Exchanges))
