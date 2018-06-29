import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import logging
from gui.Dialogs.LoginDialog import LoginDialog


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

class ConnectivityBox(Gtk.ListBox):

    def __init__(self, parent):
        super(ConnectivityBox, self).__init__()
        logging.debug("Creating ConnectivityBox")
        self.parent = parent
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.set_border_width(10)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.connectionBoxDescLabel = Gtk.Label(xalign=0)
        self.connectionBoxDescLabel.set_markup("<b>Emubox Connectivity</b>")
        self.hbox.pack_start(self.connectionBoxDescLabel, True, True, 0)
        self.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.connStatusDescLabel = Gtk.Label("Connection Status: ", xalign=0)
        self.hbox.pack_start(self.connStatusDescLabel, True, True, 0)

        self.connStatusLabel = Gtk.Label(" Disconnected ", xalign=0)
        self.connEventBox = Gtk.EventBox()
        self.connEventBox.add(self.connStatusLabel)
        self.connEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 0, 0, .5))
        self.hbox.pack_start(self.connEventBox, False, True, 0)
        self.connectionButton = Gtk.Button("Connect")
        self.connectionButton.connect("clicked", self.changeConnState)
        self.connectionButton.props.valign = Gtk.Align.CENTER
        self.hbox.pack_start(self.connectionButton, False, True, 0)
        self.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.label = Gtk.Label("Automatic Reconnect", xalign=0)
        self.check = Gtk.CheckButton()
        # disable for now
        self.check.set_sensitive(False)

        self.hbox.pack_start(self.label, True, True, 0)
        self.hbox.pack_start(self.check, False, True, 0)

        self.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.add(self.row)

    def changeConnState(self, button):
        logging.debug("changeConnState(): initiated")
        logging.debug("changeConnState(): Button Label: " + button.get_label())
        if button.get_label() == "Connect":
            loginDialog = LoginDialog(self.parent)
            response = loginDialog.run()
            if response == Gtk.ResponseType.OK:
                button.set_label("Disconnect")
                self.connStatusLabel.set_label(" Connected ")
                self.connEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0, 1, 0, .5))
            elif response == Gtk.ResponseType.CANCEL:
                {}
            loginDialog.destroy()

        else:
            button.set_label("Connect")
            self.connStatusLabel.set_label(" Disconnected ")
            self.connEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 0, 0, .5))
