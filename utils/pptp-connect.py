#!/usr/bin/env python

from subprocess import Popen, PIPE, STDOUT
from sys import argv, platform
import logging
import shlex
import threading
from time import sleep

class Connection:
    
    def __init__(self, connectionName, serverIP):
        if platform == "linux" or platform == "linux2":
            self.POSIX = True
    
        self.procRunning = False
        self.connectionName = connectionName
        self.serverIP = serverIP
        self.p = None #will hold connection process

    def connectPPTP(self, username, password):
        logging.info("Using: " + username + "/"+password)
        if self.POSIX:
            logging.debug("Starting pptp connection thread")
            #test command is: 
            #pptpsetup --create pptpccaa --server 11.0.0.100 --username test3 --password test3 --encrypt --start
            connCmd = "pptpsetup --create " + connectionName + " --server " + serverIP + " --username " + username + " --password " + password + " --encrypt --start"
            t = threading.Thread(target=self.watchProcess, args=(connCmd,))
            t.start()
    
    def watchProcess(self, cmd):
        
        #Function for starting the process and capturing its stdout
        try:
            logging.debug("Starting process: " + str(cmd) + "\r\n")
            
            if self.POSIX:
                self.p = Popen(shlex.split(cmd, posix=self.POSIX), shell=False, stdout=PIPE, stderr=STDOUT, bufsize=1)
                self.procRunning = True
            else:
                logging.error("Platform is not linux or linux2")
                print("Sorry your platform is not supported")
    
            logging.debug(" watchProcess(): finished call to popen, observing stdout... ")
            #TODO: should start a thread that monitors the connection status if it's not apparent from the process output
            with self.p.stdout:
                for line in iter(self.p.stdout.readline, b''):
                    logging.debug(" watchProcess(): new line identified: " + line)
                    #TODO: process output to check status of connection
                    logging.info(" PPTP Connection Status: " + line)
            self.p.wait()
            self.procRunning = False
            logging.info("Connection closed")
            
        except Exception as x:
            logging.error(" watchProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
            if self.p != None and self.p.poll() == None:
                self.p.terminate()
                self.procRunning = False
    
    def disconnectPPTP():
        if self.p != None and self.p.poll() == None:
            self.p.terminate()
            self.procRunning = False

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.debug("Starting Program")
    #TODO: read from an XML file eventually
    connectionName = "pptpccaa"
    serverIP = "11.0.0.100"
    conn = Connection(connectionName, serverIP)
    
    #TODO: read from a dialog box eventually
    #username = "test3"
    #password = "test3"

    username = argv[1]
    password = argv[2]

    conn.connectPPTP(username, password)
    sleep(100)
    conn.disconnectPPTP()
