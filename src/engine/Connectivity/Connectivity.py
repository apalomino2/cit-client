#!/usr/bin/env python

from subprocess import Popen, PIPE
from sys import argv, platform
import logging
import shlex
import threading
from time import sleep
import sys

class Connectivity:
    NOT_CONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    NOT_DISCONNECTING =3
    DISCONNECTING = 4

    def __init__(self, connectionName):
        if platform == "linux" or platform == "linux2":
            self.POSIX = True

        self.connectAttemptTimeout = 5

        self.connectionName = connectionName
        self.connStatus = Connectivity.NOT_CONNECTED
        self.disConnStatus = Connectivity.NOT_DISCONNECTING
        self.serverIP = None
        self.username = ""
        self.password = ""

    def connProcess(self, cmd):

        # Function for starting the process and capturing its stdout
        try:
            logging.debug("Starting process: " + str(cmd) + "\r\n")
            localAddressSet = False
            remoteAddressSet = False
            if self.POSIX:
                p = Popen(shlex.split(cmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
                while True:
                    out = p.stdout.readline()
                    if out == '' and p.poll() != None:
                        break
                    if out != '':
                        logging.debug("connProcess(): stdout Line: " + out)
                        if "local  IP address " in out:
                            logging.debug("connProcess(): local IP address identified")
                            localAddressSet = True
                        if "remote IP address" in out:
                            logging.debug("connProcess(): local IP address identified")
                            remoteAddressSet = True
                        if localAddressSet and remoteAddressSet:
                            logging.debug("connProcess(): Connection Established")
                            self.connStatus = Connectivity.CONNECTED
                logging.debug("connProcess(): Connection Closed")
                logging.info("Process completed: " + cmd)

                self.connStatus = Connectivity.NOT_CONNECTED
            else:
                logging.error("Platform is not linux or linux2")
                print("Sorry your platform is not supported")

        except Exception as x:
            logging.error(" connProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
            self.disconnectPPTP()
            if p != None and p.poll() == None:
                p.terminate()

    def disconnProcess(self, cmd):

        # Function for starting the process and capturing its stdout
        try:
            logging.debug("Starting process: " + str(cmd) + "\r\n")
            outlog = ""
            if self.POSIX:
                p = Popen(shlex.split(cmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
                while True:
                    out = p.stdout.readline()
                    if out == '' and p.poll() != None:
                        break
                    if out != '':
                        logging.debug("disconnProcess(): stdout Line: " + out)

                logging.info("Process completed: " + cmd)
                self.disConnStatus = Connectivity.NOT_DISCONNECTING

                self.connStatus = Connectivity.NOT_CONNECTED
                self.serverIP = None
                self.username = ""
                self.password = ""
                #connectionName, serverIP, username, password

            else:
                logging.error("Platform is not linux or linux2")
                print("Sorry your platform is not supported")

        except Exception as x:
            logging.error(
                " disconnProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
            if p != None and p.poll() == None:
                p.terminate()
                self.disConnStatus = Connectivity.NOT_DISCONNECTING

    def connectPPTP(self, serverIP, username, password):
        logging.info("Using: " + username + "/" + password)
        if self.POSIX:
            logging.debug("Starting pptp connection thread")
            self.connStatus = Connectivity.CONNECTING
            # test command is:
            # pptpsetup --create pptpccaa --server 11.0.0.100 --username test3 --password test3 --encrypt --start
            connCmd = "timeout " + str(self.connectAttemptTimeout) + " pptpsetup --create " + self.connectionName + " --server " + serverIP + " --username " + username + " --password " + password + " --encrypt --start"
            t = threading.Thread(target=self.connProcess, args=(connCmd,))
            t.start()

    def disconnectPPTP(self):
        logging.debug(" disconnectPPTP(): initiated")
        if self.POSIX:
            logging.debug("Shutting down pptp connection thread")
            self.connStatus = Connectivity.DISCONNECTING
            # test command is:
            # pptpsetup --create pptpccaa --server 11.0.0.100 --username test3 --password test3 --encrypt --start
            closeConnCmd = "poff " + self.connectionName
            t = threading.Thread(target=self.disconnProcess, args=(closeConnCmd,))
            t.start()

    def getStatus(self):
        return {"connStatus" : self.connStatus, "disConnStatus" : self.disConnStatus, "connectionName" : self.connectionName, "serverIP" : self.serverIP}


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")

    conn = Connectivity(connectionName = "testpptp")
    serverIP = "11.0.0.100"
    username = "test3"
    password = "test3"

    logging.debug("Calling connectionPPTP()")
    conn.connectPPTP(serverIP, username, password)
    logging.debug("Status: " + str(conn.getStatus()))
    while conn.getStatus()["connStatus"] != Connectivity.CONNECTED:
        logging.debug("Connection not established, trying again in 5 seconds")
        sleep(5)
        if conn.getStatus()["connStatus"] == Connectivity.NOT_CONNECTED:
            conn.connectPPTP(serverIP, username, password)
    sleep(5)
    logging.debug("Status: " + str(conn.getStatus()))
    logging.debug("Calling disconnectPPTP()")
    conn.disconnectPPTP()
    sleep(5)
    logging.debug("Status: " + str(conn.getStatus()))
    logging.debug("Complete")

# keywords/phraes to search for connection status:
# Connect: -> connecting
# Modem hangup -> hanging up
# Connection Terminated -> connection terminated
