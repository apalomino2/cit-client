#!/usr/bin/env python

from subprocess import Popen, PIPE
from sys import argv, platform
import logging
import shlex
import threading
from time import sleep

class Connection():
    NOT_CONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    NOT_DISCONNECTING = 3
    DISCONNECTING = 4

    def __init__(self, connectionName):
        if platform == "linux" or platform == "linux2":
            self.POSIX = True

        self.connectAttemptTimeout = 5

        self.connectionName = connectionName
        self.connStatus = Connection.NOT_CONNECTED
        self.disConnStatus = Connection.NOT_DISCONNECTING
        self.serverIP = None
        self.username = ""
        self.password = ""
