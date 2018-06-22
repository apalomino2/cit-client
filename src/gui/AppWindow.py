import os
import shutil
import logging
import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# This class contains the main window, its main container is a notebook
class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        logging.debug("Creating AppWindow")
        super(AppWindow, self).__init__(*args, **kwargs)
        self.set_default_size(250, 180)
        # self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(5)

        # TODO: fix error when soft saving
        self.isRemoveVM = False

        # Layout container initialization
        self.windowBox = Gtk.Box(spacing=5)

        # Labels
        self.PPTPStateLabel = Gtk.Label("PPTP Connection State: ")

        # Initialization
        self.initializeContainers()

        # Signal initialization

        # This will get called when the window terminates
        #self.connect("delete-event", self.on_delete)

    def initializeContainers(self):
        self.add(self.windowBox)

        self.windowBox.pack_start(self.PPTPStateLabel, True, True, 5)
        #self.windowBox.pack_end(self.actionEventBox, True, True, PADDING)
