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

    def buildParser(self):
        self.parser = argparse.ArgumentParser()
        self.subParsers = self.parser.add_subparsers()

        self.engineParser = self.subParsers.add_parser('engine', help='retrieve overall engine status')
        self.engineParser.add_argument('status', help='retrieve engine status')

# -----------Connectivity
        self.connectivityParser = self.subParsers.add_parser('pptp')
        self.connectivitySubParsers = self.connectivityParser.add_subparsers(help='manage pptp connections')

    # -----------pptp
        self.pptpStatusParser = self.connectivitySubParsers.add_parser('status', help='retrieve connection status')
        self.pptpStatusParser.add_argument('<connection name>', action="store",
                                           help='name of connection to retrieve status')

        self.pptpStartParser = self.connectivitySubParsers.add_parser('start', help='start pptp connection')
        self.pptpStartParser.add_argument('<connection name>', action="store",
                                          help='name of connection')
        self.pptpStartParser.add_argument('<ip address>', action="store",
                                          help='pptp server IPv4 address')
        self.pptpStartParser.add_argument('<username>', action="store",
                                          help='username for pptp connection')
        self.pptpStartParser.add_argument('<password>', action="store",
                                          help='password for pptp connection')

        self.pptpStopParser = self.connectivitySubParsers.add_parser('stop', help='stop an active pptp connection')
        self.pptpStopParser.add_argument('<connection name>', action="store",
                                         help='name of connection to stop')
#-----------VM Manage
        self.vmManageParser = self.subParsers.add_parser('vm-manage')
        self.vmManageSubParsers = self.vmManageParser.add_subparsers(help='manage vm')

        self.vmStatusParser = self.vmManageSubParsers.add_parser('status', help='retrieve vm status')
        self.vmStatusParser.add_argument('<vm name>', action="store",
                                           help='name of vm to retrieve status')

        self.vmStartParser = self.vmManageSubParsers.add_parser('start', help='start a vm')
        self.vmStartParser.add_argument('<vm name>', action="store",
                                          help='name of vm to start')

        self.vmSuspendParser = self.vmManageSubParsers.add_parser('suspend', help='suspend a vm')
        self.vmSuspendParser.add_argument('<vm name>', action="store",
                                         help='name of vm to suspend')
    def execute(self, cmd):
        #parse out the command
        logging.debug("Received: " + str(cmd))
        self.parser.parse_args(cmd)
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
