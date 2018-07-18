#!/usr/bin/env python

from VMAdaptorInfo import VMAdaptorInfo
from VMManage import VMManage

class VM:
    VM_STATE_ON = 2
    VM_STATE_OFF = 3
    VM_STATE_SUSPENDED = 4
    VM_STATE_ABORTED = 5
    VM_STATE_UNKNOWN = 6
    VM_STATE_OTHER = -2
    
    def __init__(self):
        #TODO: think of making these into a dictionary entry
        self.vmName = ""
        self.vmUUID = ""
        self.setupStatus = VMManage.VM_SETUP_UNKNOWN
        self.vmState = VM.VM_STATE_UNKNOWN
        self.adaptorInfo = [] #list adaptors (strings)
        self.groups = []#list groups (strings)

    
