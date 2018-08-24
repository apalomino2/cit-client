#!/usr/bin/env python

from subprocess import Popen, PIPE
from Connection import Connection
from sys import argv, platform
import logging
import shlex
import threading
from time import sleep

class PPTPConnectionWin(Connection):

    def __init__(self, connectionName):
        Connection.__init__(self, connectionName)

    # Function to establish create and connect to a VPN.
    def checkConnExists(self):
        logging.debug("checkConnExists(): instantiated")
        checkCmd = "powershell (Get-VpnConnection -Name "+self.connectionName+").ConnectionStatus"
        try:
            process = Popen(shlex.split(checkCmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
            result = process.communicate()[0]
            status = str(result.decode("utf-8").strip())
            if status == "Connected" or status == "Disconnected":
                logging.debug("Connection exists")
                return True
            else:
                return False
        except Exception as x:
            logging.error(" checkConnExists(): Something went wrong while running process: " + str(checkCmd) + "\r\n" + str(x))
            return None
            
    def removeConnProcess(self):
        logging.debug("removeConnProcess(): instantiated")
        removeCmd = "powershell Remove-VpnConnection -Name "+self.connectionName+" -Force -PassThru "
        try:
            process = Popen(shlex.split(removeCmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
            result = process.communicate()[0]
            if self.checkConnExists() != False:
                logging.error("removeConnProcess(): Could not remove connection" + str(result))
                return False
            else:
                logging.debug("removeConnProcess(): Removal successful")
                return True
        except Exception as x:
            logging.error(" removeConnProcess(): Something went wrong while running process: " + str(removeCmd) + "\r\n" + str(x))
            return False

    def addConn(self):
        logging.debug("addConn(): instantiated")
        addCmd = "powershell (Add-VpnConnection -Name "+self.connectionName + " -ServerAddress "+ self.serverIP + " -PassThru -TunnelType Pptp).Name"
        try:
            process = Popen(shlex.split(addCmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
            result = process.communicate()[0]
            
            if str(result).strip() != self.connectionName:
                logging.error("addConn(): Could not add connection: " + str(result) + " != " + self.connectionName)
                return False
            else:
                logging.debug("addConn(): Connection add successful")
                return True
        except Exception as x:
            logging.error(" addConn(): Something went wrong while running process: " + str(addCmd) + "\r\n" + str(x))
            return False
    
    def getVPNLocalIP(self):
        #(Get-NetIPAddress -InterfaceAlias emubox-client).IPAddress
        logging.debug("getVPNLocalIP(): instantiated")
        
        getLocalCmd = "powershell (Get-NetIPAddress -InterfaceAlias "+self.connectionName+").IPAddress"
        try:
            process = Popen(shlex.split(getLocalCmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
            result = process.communicate()[0]
            
            if str(result) == "":
                logging.error("getVPNLocalIP(): Could not get VPN local IP: " + str(result))
            else:
                logging.debug("getVPNLocalIP(): VPN local IP retrieved: " + str(result))
            return str(result)
        except Exception as x:
            logging.error(" getVPNLocalIP(): Something went wrong while running process: " + str(getLocalCmd) + "\r\n" + str(x))
            return False
        
    def getVPNServerIP(self):
        #(Get-VpnConnection -Name test-emu).ServerAddress
        logging.debug("getVPNServerIP(): instantiated")
        #powershell (Get-VpnConnection -Name test-emu).ServerAddress
        getServerCmd = "powershell (Get-VpnConnection -Name "+self.connectionName+").ServerAddress"
        try:
            process = Popen(shlex.split(getServerCmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
            result = process.communicate()[0]
            
            if str(result) == "":
                logging.error("getServerCmd(): Could not get VPN server IP: " + str(result))
            else:
                logging.debug("getVPNServerIP(): VPN server IP retrieved: " + str(result))
            return str(result)
        except Exception as x:
            logging.error(" getVPNServerIP(): Something went wrong while running process: " + str(getServerCmd) + "\r\n" + str(x))
            return False
        
    def connProcess(self, cmd):
        logging.debug("connProcess(): instantiated")
        # Function for starting the process and capturing its stdout
        localAddressSet = False
        remoteAddressSet = False
        connSuccess = False
        
        #First remove connection if it already exists
        if self.checkConnExists() == True:
            if self.removeConnProcess() == False:
                logging.error("connProcess(): removeConn unsuccessful, canceling connect and returning")
                self.connStatus = Connection.NOT_CONNECTED
                return False

        #Register connection:
        if self.addConn() == False:
            logging.error("connProcess(): addConn unsuccessful, canceling connect and returning")
            self.connStatus = Connection.NOT_CONNECTED
            return False
        
        #Connect to server
        try:
            logging.debug("Starting process: " + str(cmd) + "\r\n")
            connSuccess = False
            p = Popen(shlex.split(cmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
            while True:
                out = p.stdout.readline()
                if out == '' and p.poll() != None:
                    break
                if out != '':
                    logging.debug("connProcess(): connection process output: " + out)
                    if "Successfully connected" in out:
                        logging.debug("connProcess(): Connection established")
                        connSuccess = True
            logging.info("Process completed: " + cmd)
        
            #Get the VPN local and server IP addresses
            self.localIPAddress = self.getVPNLocalIP()
            if self.localIPAddress == "":
                logging.error("connProcess(): getVPNLocalIP unsuccessful")
            else:
                localAddressSet = True
            
            self.remoteIPAddress = self.getVPNServerIP()
            if self.remoteIPAddress == "":
                logging.error("connProcess(): getVPNServerIP unsuccessful")
            else:
                remoteAddressSet = True

            if connSuccess and localAddressSet and remoteAddressSet:
                self.connStatus = Connection.CONNECTED
            else:
                Connection.NOT_CONNECTED

        except Exception as x:
            logging.error(" connProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
            self.disconnect()
            if p != None and p.poll() == None:
                p.terminate()

    def disconnProcess(self, cmd):
        logging.debug("diconnProcess(): instantiated")
        # Function for starting the process and capturing its stdout
        #Check if conn exists
        if self.checkConnExists() == True:
            try:
                logging.debug("Starting process: " + str(cmd) + "\r\n")
                outlog = ""
                p = Popen(shlex.split(cmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
                while True:
                    out = p.stdout.readline()
                    if out == '' and p.poll() != None:
                        break
                    if out != '':
                        logging.debug("disconnProcess(): stdout Line: " + out)
            except Exception as x:
                logging.error(
                    " disconnProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
                if p != None and p.poll() == None:
                    p.terminate()
                    self.disConnStatus = Connection.NOT_DISCONNECTING
                    return False
            logging.info("Process completed: " + cmd)

            #disconnect
            logging.debug("disconnProcess(): removing connection: " + self.connectionName)
            if self.removeConnProcess() == False:
                logging.error("connProcess(): removeConn unsuccessful, returning")
                self.disConnStatus = Connection.NOT_DISCONNECTING
                return False
                
        #if it existed or not, we clean up
        self.disConnStatus = Connection.NOT_DISCONNECTING

        self.connStatus = Connection.NOT_CONNECTED
        self.serverIP = None
        self.username = ""
        self.password = ""
        self.localIPAddress = ""
        self.serverIPAddress = ""       

    def connect(self, serverIP, username, password):
        logging.info("Using: " + username + "/" + password)
        logging.debug("Starting pptp connection thread")
        self.connStatus = Connection.CONNECTING
        self.serverIP = serverIP
        #["powershell", "rasdial %s %s %s" % (name, username, password)
        connCmd = "powershell rasdial " + self.connectionName + " " + username + " " + password
        t = threading.Thread(target=self.connProcess, args=(connCmd,))
        t.start()

    def disconnect(self):
        logging.debug(" disconnect(): initiated")
        logging.debug("Shutting down pptp connection thread")
        self.connStatus = Connection.DISCONNECTING
                      
        closeConnCmd = "powershell rasdial " + self.connectionName + " /DISCONNECT "
        t = threading.Thread(target=self.disconnProcess, args=(closeConnCmd,))
        t.start()

    def getStatus(self):
        logging.debug( "getStatus(): instantiated")
        #Don't want to rely on python objects in case we go with 3rd party clients in the future
        return {"connStatus" : self.connStatus, "disConnStatus" : self.disConnStatus, "connectionName" : self.connectionName, "serverIP" : self.serverIP, "localIP" : self.localIPAddress, "remoteIP" : self.remoteIPAddress}

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")

    conn = PPTPConnectionWin(connectionName = "emubox-client")
    serverIP = "192.168.197.3"
    username = "test3"
    password = "test3"

    logging.debug("Calling connection()")
    conn.connect(serverIP, username, password)
    logging.debug("Status: " + str(conn.getStatus()))
    sleep(5)
    while conn.getStatus()["connStatus"] != Connection.CONNECTED:
        if conn.getStatus()["connStatus"] == Connection.CONNECTING:
            logging.debug("Attempting to connect, checking status in 5 seconds")
            sleep(5)
        if conn.getStatus()["connStatus"] == Connection.NOT_CONNECTED:
            logging.debug("Connection failed, trying to reconnect")    
            conn.connect(serverIP, username, password)

    logging.debug("Status: " + str(conn.getStatus()))
    logging.debug("Calling disconnect()")
    conn.disconnect()
    sleep(5)
    logging.debug("Status: " + str(conn.getStatus()))
    logging.debug("Complete")

