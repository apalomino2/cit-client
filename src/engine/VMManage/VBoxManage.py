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
        logging.info("VBoxManage.__init__(): instantiated")
        VMManage.__init__(self)
        self.readStatus = VMManage.MANAGER_UNKNOWN
        self.writeStatus = VMManage.MANAGER_UNKNOWN
        #initial refresh
        self.refreshAllVMInfo()

    def configureVM(self, vmName, srcIPAddress, dstIPAddress, srcPort, dstPort, adaptorNum):
        logging.info("configureVM(): instantiated")
        
        if VMManage.POSIX:
            #check to make sure the vm is known, if not should refresh or check name:
            if vmName not in self.vms:
                logging.error("refreshVMInfo(): " + vmName + " not found in list of known vms: \r\n" + str(self.vms))
                return -1
            t = threading.Thread(target=self.runConfigureVM, args=(vmName, srcIPAddress, dstIPAddress, srcPort, dstPort, adaptorNum))
            t.start()
            return 0
        else:
            logging.error("Platform is not linux or linux2")
            print("Sorry your platform is not supported")       
    

    def refreshAllVMInfo(self):
        logging.info("refreshAllVMInfo(): instantiated")
        
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
            logging.debug("refreshVMInfo() refresh VMs thread")
            #check to make sure the vm is known, if not should refresh or check name:
            if vmName not in self.vms:
                logging.error("refreshVMInfo(): " + vmName + " not found in list of known vms: \r\n" + str(self.vms))
                return -1
            t = threading.Thread(target=self.runVMInfo, args=(vmName,))
            t.start()
            return 0
        else:
            logging.error("Platform is not linux or linux2")
            print("Sorry your platform is not supported")       
    
    def runVMSInfo(self):
        logging.debug("runVMSInfo(): instantiated")
        #run vboxmanage to get vm listing
        self.readStatus = VMManage.MANAGER_READING
        #clear out the current set
        self.vms = {}
        vmListCmd = "timeout " + str(VMManage.MANAGER_STATUS_TIMEOUT_VAL) + " " + VBoxManage.VBOX_PATH + " list vms"
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
                vm.name = splitOut[0].strip()
                vm.UUID = splitOut[1].split("}")[0].strip()
                logging.debug("UUID: " + vm.UUID)
                self.vms[vm.name] = vm
        p.wait()
        logging.info("runVMSInfo(): Thread 1 completed: " + vmListCmd)
        logging.info("Found # VMS: " + str(len(self.vms)))
        
        #for each vm, get the machine readable info
        logging.debug("runVMSInfo(): collecting VM extended info")
        vmNum = 1
        for aVM in self.vms:
            logging.debug("runVMSInfo(): collecting # " + str(vmNum) + " of " + str(len(self.vms)))
            vmShowInfoCmd = "timeout " + str(VMManage.MANAGER_STATUS_TIMEOUT_VAL) + " " + VBoxManage.VBOX_PATH + " showvminfo \"" + str(self.vms[aVM].UUID) + "\"" + " --machinereadable"
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
                        out = out.strip()
                        nicNum = out.split("=")[0][3:]
                        nicType = out.split("=")[1]
                        self.vms[aVM].adaptorInfo[nicNum] = nicType
                    res = re.match("groups=", out)
                    if res:
                        logging.debug("Found groups: " + out + " added to " + self.vms[aVM].name)
                        self.vms[aVM].groups = out.strip()
                    res = re.match("VMState=", out)
                    if res:
                        logging.debug("Found vmState: " + out + " added to " + self.vms[aVM].name)
                        state = out.strip().split("\"")[1].split("\"")[0]
                        if state == "running":
                            self.vms[aVM].state = VM.VM_STATE_RUNNING
                        elif state == "poweroff":
                            self.vms[aVM].state = VM.VM_STATE_OFF
                        else:
                            self.vms[aVM].state = VM.VM_STATE_OTHER
                        
            p.wait()
            vmNum = vmNum + 1
        self.readStatus = VMManage.MANAGER_IDLE
        logging.info("runVMSInfo(): Thread 2 completed: " + vmShowInfoCmd)

    def runVMInfo(self, aVM):
        logging.debug("runVMSInfo(): instantiated")
        self.readStatus = VMManage.MANAGER_READING
        vmShowInfoCmd = "timeout " + str(VMManage.MANAGER_STATUS_TIMEOUT_VAL) + " " + VBoxManage.VBOX_PATH + " showvminfo \"" + self.vms[aVM].UUID + "\"" + " --machinereadable"
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
                    out = out.strip()
                    nicNum = out.split("=")[0][3:]
                    nicType = out.split("=")[1]
                    self.vms[aVM].adaptorInfo[nicNum] = nicType
                res = re.match("groups=", out)
                if res:
                    logging.debug("Found groups: " + out + " added to " + self.vms[aVM].name)
                    self.vms[aVM].groups = out.strip()
                res = re.match("VMState=", out)
                if res:
                    logging.debug("Found vmState: " + out + " added to " + self.vms[aVM].name)
                    state = out.strip().split("\"")[1].split("\"")[0].strip()
                    if state == "running":
                        self.vms[aVM].state = VM.VM_STATE_RUNNING
                    elif state == "poweroff":
                        self.vms[aVM].state = VM.VM_STATE_OFF
                    else:
                        self.vms[aVM].state = VM.VM_STATE_OTHER
        p.wait()
        self.readStatus = VMManage.MANAGER_IDLE
        logging.debug("runVMInfo(): Thread completed")


    def runConfigureVM(self, vmName, srcIPAddress, dstIPAddress, srcPort, dstPort, adaptorNum):
        logging.debug("runConfigureVM(): instantiated")
        self.writeStatus = VMManage.MANAGER_WRITING
        vmConfigVMCmd = "timeout " + str(VMManage.MANAGER_STATUS_TIMEOUT_VAL) + " " + VBoxManage.VBOX_PATH + " modifyvm " + str(vmName) + " --nic" + str(adaptorNum) + " generic" + " --nicgenericdrv1 UDPTunnel " + "--cableconnected" + str(adaptorNum) + " on --nicproperty" + str(adaptorNum) + " sport=" + str(srcPort) + " --nicproperty" + str(adaptorNum) + " dport=" + str(dstPort) + " --nicproperty" + str(adaptorNum) + " dest=" + str(dstIPAddress)
        logging.debug("runConfigureVM(): Running " + vmConfigVMCmd)
        p = Popen(shlex.split(vmConfigVMCmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
        while True:
            out = p.stdout.readline()
            if out == '' and p.poll() != None:
                break
            if out != '':
                logging.debug("output line: " + out)
        p.wait()
        self.writeStatus = VMManage.MANAGER_IDLE
        logging.debug("runConfigure(): Thread completed")

    def getVMStatus(self, vmName):
        logging.debug("getVMStatus(): instantiated " + str(vmName))
        #TODO: need to make this thread safe
        resVM = self.vms[vmName]
        #Don't want to rely on python objects in case we go with 3rd party clients in the future
        return {"vmName" : resVM.name, "vmUUID" : resVM.UUID, "setupStatus" : resVM.setupStatus, "vmState" : resVM.state, "adaptorInfo" : resVM.adaptorInfo, "groups" : resVM.groups}
        
    def getManagerStatus(self):
        logging.debug("getManagerStatus(): instantiated")
        return {"readStatus" : self.readStatus, "writeStatus" : self.writeStatus}

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Starting Program")
    logging.info("Instantiating VBoxManage")
    vbm = VBoxManage()
    
    logging.info("Refreshing VM Info - BEFORE")
    for vm in vbm.vms:
        logging.info("VM Info:\r\n" + str(vm.name))
    vbm.refreshAllVMInfo()
    
    while vbm.getManagerStatus()["readStatus"] != VMManage.MANAGER_IDLE:
        logging.info("waiting for manager to finish query...")
        sleep(1)
    logging.info("Refreshing VMs Info - AFTER")

    #get vm info from objects
    for vm in vbm.vms:
        logging.info("VM Info:\r\nName: " + str(vbm.vms[vm].name) + "\r\nState: " + str(vbm.vms[vm].state) + "\r\n" + "Groups: " + str(vbm.vms[vm].groups + "\r\n"))
        for adaptor in vbm.vms[vm].adaptorInfo:
            logging.info("adaptor: " + str(adaptor) + " Type: " + vbm.vms[vm].adaptorInfo[adaptor] + "\r\n")
    
    logging.info("Refreshing single VM Info--")
    logging.info("Result: " + str(vbm.refreshVMInfo("\"ubuntu-core4.7\"")))

    while vbm.getManagerStatus()["readStatus"] != VMManage.MANAGER_IDLE:
        logging.info("waiting for manager to finish query...")
        sleep(1)
    
    logging.info("Status for \"ubuntu-core4.7\"")
    logging.info(vbm.getVMStatus("\"ubuntu-core4.7\""))

    #runConfigureVM(self, vmName, srcIPAddress, dstIPAddress, srcPort, dstPort, adaptorNum)
    vbm.configureVM("\"ubuntu-core4.7\"", "", "127.0.0.1", 100, 100, 1)

    while vbm.getManagerStatus()["readStatus"] != VMManage.MANAGER_IDLE and vbm.getManagerStatus()["writeStatus"] != VMManage.MANAGER_IDLE:
        logging.info("waiting for manager to finish reading/writing...")
        sleep(1)
    
    logging.info("Result: " + str(vbm.refreshVMInfo("\"ubuntu-core4.7\"")))
    while vbm.getManagerStatus()["readStatus"] != VMManage.MANAGER_IDLE and vbm.getManagerStatus()["writeStatus"] != VMManage.MANAGER_IDLE:
        logging.info("waiting for manager to finish reading/writing...")
        sleep(1)
    
    logging.info("Status for \"ubuntu-core4.7\"")
    logging.info(vbm.getVMStatus("\"ubuntu-core4.7\""))
    
    logging.info("Completed Exiting...")
