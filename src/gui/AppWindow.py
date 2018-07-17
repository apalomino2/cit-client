import logging
from gui.Widgets.ConnectionBox import ConnectionBox
from gui.Widgets.VMManageBox import VMManageBox

import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from engine.Engine import Engine
from engine.Connection.Connection import Connection

# This class contains the main window, its main container is a notebook
class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        logging.debug("Creating AppWindow")
        super(AppWindow, self).__init__(*args, **kwargs)
        self.set_default_size(220, 180)
        #self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(5)
##Outer Box
        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box_outer)

        self.connectionBox = ConnectionBox(self)
        self.box_outer.pack_start(self.connectionBox, True, True, 0)

        self.vmManageBox = VMManageBox(self)
        self.box_outer.pack_start(self.vmManageBox, True, True, 0)
		
        self.connect('delete_event', self.catchClosing)
		
    def catchClosing(self, widget, event):
        logging.debug("delete_event(): instantiated")
        e = Engine.getInstance()
        res = e.execute("pptp status " + ConnectionBox.CONNECTION_NAME)
        logging.debug("delete_event(): result: " + str(res))
        if res == -1:
            self.destroy()
            return
        result = res["connStatus"]
        if result == Connection.CONNECTING:
            closingDialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK, "Cannot quit, connection is busy...")
            closingDialog.run()
            closingDialog.destroy()
        elif result == Connection.CONNECTED:
            closingDialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL, "Quit and close connection?")
            response = closingDialog.run()
            if response == Gtk.ResponseType.OK:	
                logging.debug("delete_event(): opening disconnect dialog")
                #need to create a thread (probably a dialog box with disabled ok button until connection either times out (5 seconds), connection good
                e = Engine.getInstance()
                e.execute("pptp stop " + ConnectionBox.CONNECTION_NAME)
                disconnectingDialog = DisconnectingDialog(self.parent, ConnectionBox.CONNECTION_NAME)
                disconnectingDialog.run()
                s = disconnectingDialog.getFinalStatus()
                disconnectingDialog.destroy()
                if s == Connection.NOT_CONNECTED:
                    self.destroy()
                    return
                else:
                    cannotCloseDialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                        Gtk.ButtonsType.OK_CANCEL, "Could not close connection, try again later.")
        
