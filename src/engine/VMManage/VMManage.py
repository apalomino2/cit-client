#!/usr/bin/env python

from subprocess import Popen, PIPE
from sys import argv, platform
import logging
import shlex
import threading
from time import sleep

class VMManage:
    VM_SETUP_COMPLETE = 0
    VM_SETUP_NONE = 1
    VM_SETUP_UNKNOWN = -1
       
    MANAGER_QUERYING = 7
    MANAGER_NOT_QUERYING = 8
    MANAGER_UNKNOWN = 9
    
    POSIX = False
    if platform == "linux" or platform == "linux2":
        POSIX = True
      
    def __init__(self):
        self.vms = [] #list of VM()

    #abstractmethod
    def configureVM(self, VMName, srcIPAddress, dstIPAddress, srcPort, dstPort):
        raise NotImplementedError()

    #abstractmethod
    def refreshVMStates(self):
        raise NotImplementedError()

    #abstractmethod
    def getManagerStatus(self):
        raise NotImplementedError()

