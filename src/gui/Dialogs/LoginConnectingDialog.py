import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from engine.Engine import Engine
from time import sleep
import threading
from engine.Connection.Connection import Connection
import logging

class LoginConnectingDialog(Gtk.Dialog):
    def __init__(self, parent, connName):
        Gtk.Dialog.__init__(self, "Emubox Connection Status", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.connName = connName

        box = self.get_content_area()

        self.set_default_size(150, 100)
        self.box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)

        self.label = Gtk.Label("Connecting to Emubox Server")
        self.box_main.pack_start(self.label, True, True, 0)

        self.spinner = Gtk.Spinner()
        self.spinner.start()
        self.box_main.pack_start(self.spinner, True, True, 0)
        
        self.box_spacer01 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.box_main.pack_start(self.box_spacer01, True, True, 0)

        self.box_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.statusLabel = Gtk.Label("Attempting to connect...")
        self.box_status.pack_start(self.statusLabel, True, True, 0)
        self.box_main.pack_start(self.box_status, True, True, 0)

        self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(False)

        box.pack_start(self.box_main, True, True, 0)
        
        self.show_all()

        self.status = -1
        t = threading.Thread(target=self.watchConnStatus)
        t.start()
        
    def watchConnStatus(self):
        logging.debug("watchConnStatus(): instantiated")
        self.statusLabel.set_text("Checking connection")
        e = Engine.getInstance()
        #will check status every 1 second and will either display stopped or ongoing or connected
        while(True):
            logging.debug("watchConnStatus(): running: pptp status " + self.connName)
            self.status = e.execute("pptp status " + self.connName)["connStatus"]
            logging.debug("watchConnStatus(): result: " + str(self.status))
            if self.status == Connection.CONNECTING:
                self.statusLabel.set_text("Trying to establish connection")
            elif self.status == Connection.CONNECTED:
                self.statusLabel.set_text("Connection Established.")
                self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(True)
                self.spinner.stop()
                break
            else:
                self.statusLabel.set_text("Could not connect.")
                self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(True)
                self.spinner.stop()
                break
            sleep(1)
            
    def getFinalStatus(self):
        return self.status
