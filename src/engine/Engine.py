#!/usr/bin/env python

import logging
import shlex
import argparse
import sys
from time import sleep
from Connection.Connection import Connection
from Connection.PPTPConnection import PPTPConnection

class Engine:
    __instance = None

    @staticmethod
    def getInstance():
        #status access method
        if Engine.__instance == None:
            Engine()
        return Engine.__instance

    def __init__(self):
        #Virtually private constructor
        if Engine.__instance != None:
            raise Exception("Use the getInstance method to obtain an instance of this class")
        else:
            Engine.__instance = self
            #setup other class specific objects
            self.conns = {}
            self.vms = {}

            #build the parser
            self.buildParser()

    def pptpStatusCmd(self, args):
        logging.debug("pptpStatusCmd(): instantiated")
        if args.connName not in self.conns:
            logging.error("Connection does not exist or was not created through the engine")
            return -1
        #if we're good up to this point, run the command
        c = self.conns[args.connName]
        return c.getStatus() # returns {"connStatus" : self.connStatus, "disConnStatus" : self.disConnStatus, "connectionName" : self.connectionName, "serverIP" : self.serverIP}


    def pptpStartCmd(self, args):
        logging.debug("pptpStartCmd(): instantiated")

        if args.connName not in self.conns:
            c = PPTPConnection(connectionName = args.connName)
            self.conns[args.connName] = c
        else:
            c = self.conns[args.connName]
            logging.debug("PPTP connection exists, checking status")
            s = c.getStatus()["connStatus"]
            if s != Connection.NOT_CONNECTED:
                logging.error("PPTP connection status: " + str(s) + " connection busy")
                return -1
        #if we're good up to this point, attempt to connect
        c.connect(args.ipAddr, args.username, args.password)
        logging.info("PPTP connection signal sent: " + args.ipAddr + " " + args.username + " " + " " + args.password)
        return 0

    def pptpStopCmd(self, args):
        logging.debug("pptpStopCmd(): instantiated")
        if args.connName not in self.conns:
            logging.error("Connection does not exist or was not created through the engine")
            return -1
        else:
            c = self.conns[args.connName]
            logging.debug("PPTP connection exists, checking status")
            s = c.getStatus()["connStatus"]
            if s != Connection.CONNECTED:
                logging.error("PPTP connection status: " + str(s) + " not connected, try again later")
                return -1
        #if we're good up to this point, attempt to disconnect
        c.disconnect()
        logging.info("PPTP stop connection signal sent: " + args.connName)
        return 0

    def engineStatusCmd(self, args):
        logging.debug("engineStatusCmd(): instantiated")
        connsStatus = []
        vmsStatus = []

        for conn in self.conns:
            connsStatus.append("Connection: " + str(self.conns[conn].getStatus()))
        for vm in self.vms:
            vmsStatus.append("VM: " + str(self.vms[vm].getStatus()))

        return "\r\nConnections: \r\n" + str(connsStatus) + "\r\nVMs:\r\n" + str(vmsStatus)


    def vmManageStatusCmd(self, args):
        logging.debug("vmManageStatusCmd(): instantiated")

    def vmConfigCmd(self, args):
        logging.debug("vmConfigCmd(): instantiated")

    def vmManageStartCmd(self, args):
        logging.debug("vmManageStartCmd(): instantiated")

    def vmManageSuspendCmd(self, args):
        logging.debug("vmManageSuspendCmd(): instantiated")

    def buildParser(self):
        self.parser = argparse.ArgumentParser(description='Interface to the emubox-client service.')
        self.subParsers = self.parser.add_subparsers()

        self.engineParser = self.subParsers.add_parser('engine', help='retrieve overall engine status')
        self.engineParser.add_argument('status', help='retrieve engine status')
        self.engineParser.set_defaults(func=self.engineStatusCmd)

# -----------Connection
        self.connectionParser = self.subParsers.add_parser('pptp')
        self.connectionSubParsers = self.connectionParser.add_subparsers(help='manage pptp connections')

    # -----------pptp
        self.pptpStatusParser = self.connectionSubParsers.add_parser('status', help='retrieve connection status')
        self.pptpStatusParser.add_argument('connName', metavar='<connection name>',
                                           help='name of connection to retrieve status')
        self.pptpStatusParser.set_defaults(func=self.pptpStatusCmd)

        self.pptpStartParser = self.connectionSubParsers.add_parser('start', help='start pptp connection')
        self.pptpStartParser.add_argument('connName', metavar='<connection name>', action="store",
                                          help='name of connection')
        self.pptpStartParser.add_argument('ipAddr', metavar='<ip address>', action="store",
                                          help='pptp server IPv4 address')
        self.pptpStartParser.add_argument('username', metavar='<username>', action="store",
                                          help='username for pptp connection')
        self.pptpStartParser.add_argument('password', metavar='<password>', action="store",
                                          help='password for pptp connection')
        self.pptpStartParser.set_defaults(func=self.pptpStartCmd)

        self.pptpStopParser = self.connectionSubParsers.add_parser('stop', help='stop an active pptp connection')
        self.pptpStopParser.add_argument('connName', metavar='<connection name>', action="store",
                                         help='name of connection to stop')
        self.pptpStopParser.set_defaults(func=self.pptpStopCmd)

#-----------VM Manage
        self.vmManageParser = self.subParsers.add_parser('vm-manage')
        self.vmManageSubParsers = self.vmManageParser.add_subparsers(help='manage vm')

        self.vmStatusParser = self.vmManageSubParsers.add_parser('status', help='retrieve vm status')
        self.vmStatusParser.add_argument('vmName', metavar='<vm name>', action="store",
                                           help='name of vm to retrieve status')
        self.vmStatusParser.set_defaults(func=self.vmManageStatusCmd)

        self.vmConfigParser = self.vmManageSubParsers.add_parser('config', help='configure vm to connect to emubox')
        self.vmConfigParser.add_argument('vmName', metavar='<vm name>', action="store",
                                          help='name vm to configure')
        self.vmConfigParser.add_argument('srcIPAddr', metavar='<source ip address>', action="store",
                                          help='source IP used for UDP Tunnel')
        self.vmConfigParser.add_argument('destIPAddr', metavar='<destination ip address>', action="store",
                                          help='destination IP used for UDP Tunnel')
        self.vmConfigParser.add_argument('srcPort', metavar='<source port>', action="store",
                                          help='source port used for UDP Tunnel')
        self.vmConfigParser.add_argument('destPort', metavar='<destination port>', action="store",
                                          help='destination port used for UDP Tunnel')
        self.vmConfigParser.add_argument('adaptorNum', metavar='<adaptor number>', action="store",
                                          help='adaptor to use for UDP Tunnel configuration')
        self.vmConfigParser.set_defaults(func=self.vmConfigCmd)

        self.vmStartParser = self.vmManageSubParsers.add_parser('start', help='start a vm')
        self.vmStartParser.add_argument('vmName', metavar='<vm name>', action="store",
                                          help='name of vm to start')
        self.vmStartParser.set_defaults(func=self.vmManageStartCmd)

        self.vmSuspendParser = self.vmManageSubParsers.add_parser('suspend', help='suspend a vm')
        self.vmSuspendParser.add_argument('vmName', metavar='<vm name>', action="store",
                                         help='name of vm to suspend')
        self.vmSuspendParser.set_defaults(func=self.vmManageSuspendCmd)

    def execute(self, cmd):
        try:
            #parse out the command
            logging.debug("Received: " + str(cmd))
            r = self.parser.parse_args(shlex.split(cmd))
            #r = self.parser.parse_args(cmd)
            return r.func(r)
        except argparse.ArgumentError, exc:
            logging.error(exc.message, '\n', exc.argument)	

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")
    logging.debug("Instantiating Engine")
    e = Engine()
    logging.debug("engine object: " + str(e))

    logging.debug("Calling Engine.getInstance()")
    e = Engine.getInstance()
    logging.debug("engine object: " + str(e))

    logging.debug("Calling Engine.getInstance()")
    e = Engine.getInstance()
    logging.debug("engine object: " + str(e))

	#error should be provided
    e.execute("pptp start mypptp")
    res = e.execute("pptp status mypptp")

    #e.execute(sys.argv[1:])
    e.execute("pptp start mypptp 11.0.0.100 test3 test3")
    res = e.execute("pptp status mypptp")
    print "STATUS: " + str(res)

    sleep(1)
    res = e.execute("engine status")
    print "ENGINE STATUS: " + str(res)

    res = e.execute("pptp status mypptp")
    print "STATUS: " + str(res)

    sleep(1)
    res = e.execute("pptp status mypptp")
    print "STATUS: " + str(res)

    sleep(5)
    res = e.execute("pptp status mypptp")
    print "STATUS: " + str(res)
    e.execute("pptp stop mypptp")

    sleep(5)
    res = e.execute("pptp status mypptp")
    print "STATUS: " + str(res)

