#!/bin/python3

# git_info: 0.1 1d5a57b trader 03/01/21-22:38:48-EST-0500

import sys

sys.path.append("Utils/")
sys.path.append("Plugins/")
sys.path.append("Configs/")
sys.path.append("Credentials/")
#sys.path.append("./")

import Controller

Controller.LoadPlugins("Plugins/")


