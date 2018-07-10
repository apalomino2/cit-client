import logging
from gui.Widgets.Connection import ConnectionBox
from gui.Widgets.VMManageBox import VMManageBox

import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

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

