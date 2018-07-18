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
        self.status = VMManage.MANAGER_UNKNOWN

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
        
    def runVMSInfo(self):
        #run vboxmanage to get vm listing
        self.status = VMManage.MANAGER_QUERYING
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
                vm.vmName = splitOut[0]
                vm.vmUUID = splitOut[1].split("}")[0]
                logging.debug("UUID: " + vm.vmUUID)
                self.vms.append(vm)
        p.wait()
        logging.info("Thread completed: " + vmListCmd)
        logging.info("Found # VMS: " + str(len(self.vms)))
        
        #for each vm, get the machine readable info
        logging.debug("runVMSInfo(): collecting VM extended info")
        vmNum = 1
        for aVM in self.vms:
            logging.debug("runVMSInfo(): collecting # " + str(vmNum) + " of " + str(len(self.vms)))
            vmShowInfoCmd = VBoxManage.VBOX_PATH + " showvminfo \"" + aVM.vmUUID + "\"" + " --machinereadable"
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
                        logging.debug("Found nic: " + out + " added to " + aVM.vmName)
                        aVM.adaptorInfo.append(out.strip())
                    res = re.match("groups=", out)
                    if res:
                        logging.debug("Found groups: " + out + " added to " + aVM.vmName)
                        aVM.groups.append(out.strip())
            p.wait()
            vmNum = vmNum + 1
        logging.info("Thread completed")
        self.status = VMManage.MANAGER_NOT_QUERYING

    def getVMStatus(self):
        

    def getManagerStatus(self):
        return self.status

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Starting Program")
    logging.info("Instantiating VBoxManage")
    vbm = VBoxManage()
    logging.info("vbm: " + str(vbm))
    
    logging.info("Refreshing VM Info - BEFORE")
    for vm in vbm.vms:
        logging.info("VM Info:\r\n" + str(vm.vmName))
    vbm.refreshAllVMInfo()
    
    while vbm.getManagerStatus() != VMManage.MANAGER_NOT_QUERYING:
        logging.info("waiting for manager to finish query...")
        sleep(1)
    logging.info("Refreshing VM Info - AFTER")
    for vm in vbm.vms:
        logging.info("VM Info:\r\n" + str(vm.vmName) + "\r\n")
        for adaptor in vm.adaptorInfo:
            logging.info("adaptor: " + str(adaptor) + "\r\n")
        for group in vm.groups:
            logging.info("group:" + str(group) + "\r\n")
    logging.info("Completed Exiting...")
