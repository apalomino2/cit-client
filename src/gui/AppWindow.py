import os
import shutil
import logging
from gui.Dialogs.LoginDialog import LoginDialog
import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

# This class contains the main window, its main container is a notebook
class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        logging.debug("Creating AppWindow")
        super(AppWindow, self).__init__(*args, **kwargs)
        self.set_default_size(250, 180)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(5)

        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box_outer)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box_outer.pack_start(self.listbox, True, True, 0)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.hbox.pack_start(self.vbox, True, True, 0)

        self.connStatusDescLabel = Gtk.Label("Emubox Connection Status: ", xalign=0)
        self.vbox.pack_start(self.connStatusDescLabel, True, True, 0)

        self.connStatusLabel = Gtk.Label("Disconnected", xalign=0)
        self.hbox.pack_start(self.connStatusLabel, False, True, 0)
        self.connectionButton = Gtk.Button("Connect")
        self.connectionButton.connect("clicked", self.changeConnState)
        self.connectionButton.props.valign = Gtk.Align.CENTER
        self.hbox.pack_start(self.connectionButton, False, True, 0)

        self.listbox.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.label = Gtk.Label("Enable Automatic Update", xalign=0)
        self.check = Gtk.CheckButton()
        self.hbox.pack_start(self.label, True, True, 0)
        self.hbox.pack_start(self.check, False, True, 0)

        self.listbox.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.label = Gtk.Label("Date Format", xalign=0)
        self.combo = Gtk.ComboBoxText()
        self.combo.insert(0, "0", "24-hour")
        self.combo.insert(1, "1", "AM/PM")
        self.hbox.pack_start(self.label, True, True, 0)
        self.hbox.pack_start(self.combo, False, True, 0)

        self.listbox.add(self.row)

        self.listbox_2 = Gtk.ListBox()
        self.items = 'This is a sorted ListBox Fail'.split()

        for item in self.items:
            self.listbox_2.add(ListBoxRowWithData(item))

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.data.lower() > row_2.data.lower()

        def filter_func(row, data, notify_destroy):
            return False if row.data == 'Fail' else True

        self.listbox_2.set_sort_func(sort_func, None, False)
        self.listbox_2.set_filter_func(filter_func, None, False)

        self.listbox_2.connect('row-activated', lambda widget, row: (row.data))

        self.box_outer.pack_start(self.listbox_2, True, True, 0)
        self.listbox_2.show_all()

    def changeConnState(self, button):
        logging.debug("changeConnState(): initiated")
        logging.debug("changeConnState(): Button Label: " + button.get_label())
        if button.get_label() == "Connect":
            loginDialog = LoginDialog(self)
            response = loginDialog.run()
            if response == Gtk.ResponseType.OK:
                button.set_label("Disconnect")
                self.connStatusLabel.set_label("Connected")
            elif response == Gtk.ResponseType.CANCEL:
                {}
            loginDialog.destroy()

        else:
            button.set_label("Connect")
            self.connStatusLabel.set_label("Disconnected")

