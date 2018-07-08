#!/usr/bin/env python

import logging
import shlex
import argparse
import sys

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
            conns = []
            vms = []

            #build the parser
            self.buildParser()
    def engineStatusCmd(self, args):
        logging.debug("engineStatusCmd(): instantiated")

    def pptpStatusCmd(self, args):
        logging.debug("pptpStatusCmd(): instantiated")

    def pptpStartCmd(self, args):
        logging.debug("pptpStartCmd(): instantiated")

    def pptpStopCmd(self, args):
        logging.debug("pptpStopCmd(): instantiated")

    def vmManageStatusCmd(self, args):
        logging.debug("vmManageStatusCmd(): instantiated")

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

# -----------Connectivity
        self.connectivityParser = self.subParsers.add_parser('pptp')
        self.connectivitySubParsers = self.connectivityParser.add_subparsers(help='manage pptp connections')

    # -----------pptp
        self.pptpStatusParser = self.connectivitySubParsers.add_parser('status', help='retrieve connection status')
        self.pptpStatusParser.add_argument('<connection name>',
                                           help='name of connection to retrieve status')
        self.pptpStatusParser.set_defaults(func=self.pptpStatusCmd)

        self.pptpStartParser = self.connectivitySubParsers.add_parser('start', help='start pptp connection')
        self.pptpStartParser.add_argument('connName', metavar='<connection name>', action="store",
                                          help='name of connection')
        self.pptpStartParser.add_argument('ipAddr', metavar='<ip address>', action="store",
                                          help='pptp server IPv4 address')
        self.pptpStartParser.add_argument('username', metavar='<username>', action="store",
                                          help='username for pptp connection')
        self.pptpStartParser.add_argument('password', metavar='<password>', action="store",
                                          help='password for pptp connection')
        self.pptpStartParser.set_defaults(func=self.pptpStartCmd)

        self.pptpStopParser = self.connectivitySubParsers.add_parser('stop', help='stop an active pptp connection')
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


        self.vmStartParser = self.vmManageSubParsers.add_parser('start', help='start a vm')
        self.vmStartParser.add_argument('vmName', metavar='<vm name>', action="store",
                                          help='name of vm to start')
        self.vmStartParser.set_defaults(func=self.vmManageStartCmd)

        self.vmSuspendParser = self.vmManageSubParsers.add_parser('suspend', help='suspend a vm')
        self.vmSuspendParser.add_argument('vmName', metavar='<vm name>', action="store",
                                         help='name of vm to suspend')
        self.vmSuspendParser.set_defaults(func=self.vmManageSuspendCmd)

    def execute(self, cmd):
        #parse out the command
        logging.debug("Received: " + str(cmd))
        r = self.parser.parse_args(cmd)
        r.func(r)

        #self.parser.parse_args(shlex.split(cmd))


    def getUsage(self):
        return """
Usage:
engine help
engine status

pptp start <ip-address> <conn-name> <username> <password>
pptp stop <conn-name>
pptp status <conn-name>
 
vm config <vm-name> <src-ip-address> <dst-ip-address> [src-port] [dst-port] [adaptor#]
vm status <vm-name>
vm start <vm-name>
vm suspend <vm-name>
"""

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

    e.execute(sys.argv[1:])
