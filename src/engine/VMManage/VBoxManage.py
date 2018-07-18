#!/usr/bin/env python

from subprocess import Popen, PIPE
from sys import argv, platform
import logging
import shlex
import threading
from time import sleep
from VMManage import VMManage
from VM import VM
import re

class VBoxManage(VMManage):
    VBOX_PATH = "VBoxManage"
    
    def __init__(self):
        VMManage.__init__(self)
        self.readStatus = VMManage.MANAGER_UNKNOWN
        self.writeStatus = VMManage.MANAGER_UNKNOWN

    def configureVM(self, VMName, srcIPAddress, dstIPAddress, srcPort, dstPort):
        {}

    def refreshAllVMInfo(self):
        logging.info("getListVMS(): instantiated")
        
        if VMManage.POSIX:
            logging.debug("getListVMS() Starting List VMs thread")
            t = threading.Thread(target=self.runVMSInfo)
            t.start()
        else:
            logging.error("Platform is not linux or linux2")
            print("Sorry your platform is not supported")
        
    def refreshVMInfo(self, vmName):
        logging.info("refreshVMInfo(): instantiated: " + str(vmName))
        
        if VMManage.POSIX:
            logging.debug("refreshVMInfo() Starting List VMs thread")
            #check to make sure the vm is known, if not should refresh or check name:
            if vmName not in self.vms:
                logging.error("refreshVMInfo(): " + vmName + " not found in list of known vms")
                return -1
            aVM = self.vms[vmName]
            t = threading.Thread(target=self.runVMInfo, args=(aVM))
            t.start()
        else:
            logging.error("Platform is not linux or linux2")
            print("Sorry your platform is not supported")       
    
    def runVMSInfo(self):
        #run vboxmanage to get vm listing
        self.readStatus = VMManage.MANAGER_READING
        logging.debug("runVMSInfo(): instantiated")
        vmListCmd = VBoxManage.VBOX_PATH + " list vms"
        logging.debug("runVMSInfo(): Collecting VM Names")
        p = Popen(shlex.split(vmListCmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
        while True:
            out = p.stdout.readline()
            if out == '' and p.poll() != None:
                break
            if out != '':
                logging.debug("runVMSInfo(): stdout Line: " + out)
                logging.debug("runVMSInfo(): split Line: " + str(out.split("{")))
                splitOut = out.split("{")
                vm = VM()
                vm.name = splitOut[0]
                vm.UUID = splitOut[1].split("}")[0]
                logging.debug("UUID: " + vm.UUID)
                self.vms[vm.name] = vm
        p.wait()
        logging.info("Thread completed: " + vmListCmd)
        logging.info("Found # VMS: " + str(len(self.vms)))
        
        #for each vm, get the machine readable info
        logging.debug("runVMSInfo(): collecting VM extended info")
        vmNum = 1
        for aVM in self.vms:
            logging.debug("runVMSInfo(): collecting # " + str(vmNum) + " of " + str(len(self.vms)))
            vmShowInfoCmd = VBoxManage.VBOX_PATH + " showvminfo \"" + str(self.vms[aVM].UUID) + "\"" + " --machinereadable"
            logging.debug("runVMSInfo(): Running " + vmShowInfoCmd)
            p = Popen(shlex.split(vmShowInfoCmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
            while True:
                out = p.stdout.readline()
                if out == '' and p.poll() != None:
                    break
                if out != '':
                    #match example: nic1="none"
                    res = re.match("nic[0-9]+=", out)
                    if res:
                        logging.debug("Found nic: " + out + " added to " + self.vms[aVM].name)
                        self.vms[aVM].adaptorInfo.append(out.strip())
                    res = re.match("groups=", out)
                    if res:
                        logging.debug("Found groups: " + out + " added to " + self.vms[aVM].name)
                        self.vms[aVM].groups.append(out.strip())
                    res = re.match("VMState=", out)
                    if res:
                        logging.debug("Found vmState: " + out + " added to " + self.vms[aVM].name)
                        state = out.strip().split("\"")[1].split("\"")[0]
                        if state == "running":
                            self.vms[aVM].state = VM.VM_STATE_RUNNING
                        else:
                            self.vms[aVM].state = VM.VM_STATE_OTHER
                        
            p.wait()
            vmNum = vmNum + 1
        self.readStatus = VMManage.MANAGER_IDLE
        logging.info("Thread completed")

    def runVMInfo(self, aVM):
        logging.debug("runVMSInfo(): collecting # " + str(vmNum) + " of " + str(len(self.vms)))
        self.readStatus = VMManage.MANAGER_READING
        vmShowInfoCmd = VBoxManage.VBOX_PATH + " showvminfo \"" + self.vms[aVM].UUID + "\"" + " --machinereadable"
        logging.debug("runVMSInfo(): Running " + vmShowInfoCmd)
        p = Popen(shlex.split(vmShowInfoCmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
        while True:
            out = p.stdout.readline()
            if out == '' and p.poll() != None:
                break
            if out != '':
                #match example: nic1="none"
                res = re.match("nic[0-9]+=", out)
                if res:
                    logging.debug("Found nic: " + out + " added to " + self.vms[aVM].name)
                    self.vms[aVM].adaptorInfo.append(out.strip())
                res = re.match("groups=", out)
                if res:
                    logging.debug("Found groups: " + out + " added to " + self.vms[aVM].name)
                    self.vms[aVM].groups.append(out.strip())
                res = re.match("VMState=", out)
                if res:
                    logging.debug("Found vmState: " + out + " added to " + self.vms[aVM].name)
                    state = out.strip().split("\"")[1].split("\"")[0]
                    if state == "running":
                        self.vms[aVM].state = VM.VM_STATE_RUNNING
                    else:
                        self.vms[aVM].state = VM.VM_STATE_OTHER
        p.wait()
        self.readStatus = VMManage.MANAGER_IDLE
        logging.info("Thread completed")


    def getVMStatus(self, vmName):
        resVM = self.vms[vmName]
        #Don't want to rely on python objects in case we go with 3rd party clients in the future
        return {"vmName" : resVM.name, "vmUUID" : resVM.UUID, "setupStatus" : resVM.setupStatus, "vmState" : resVM.state, "adaptorInfo" : resVM.adaptorInfo, "groups" : resVM.groups}
        
    def getManagerStatus(self):
        return {"readStatus" : self.readStatus, "writeStatus" : self.writeStatus}

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("Starting Program")
    logging.info("Instantiating VBoxManage")
    vbm = VBoxManage()
    logging.info("vbm: " + str(vbm))
    
    logging.info("Refreshing VM Info - BEFORE")
    for vm in vbm.vms:
        logging.info("VM Info:\r\n" + str(vm.name))
    vbm.refreshAllVMInfo()
    
    while vbm.getManagerStatus()["readStatus"] != VMManage.MANAGER_IDLE:
        logging.info("waiting for manager to finish query...")
        sleep(1)
    logging.info("Refreshing VM Info - AFTER")

    #get vm info from objects
    for vm in vbm.vms:
        logging.info("VM Info:\r\n" + str(vbm.vms[vm].name) + "State: " + str(vbm.vms[vm].state) + "\r\n")
        for adaptor in vbm.vms[vm].adaptorInfo:
            logging.info("adaptor: " + str(adaptor) + "\r\n")
        for group in vbm.vms[vm].groups:
            logging.info("group:" + str(group) + "\r\n")
            
    #get vm info from status method:
    for vm in vbm.vms:
        logging.info("VM Info:\r\n" + str(vbm.getVMStatus(vm)))

    logging.info("Completed Exiting...")
