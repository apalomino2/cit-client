import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class LoginDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Login", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        box = self.get_content_area()

        self.set_default_size(150, 100)
        self.box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.label = Gtk.Label("Login to Emubox Server")
        self.box_main.pack_end(self.label, True, True, 0)

        self.box_serverIP = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.serverIPLabel = Gtk.Label("Server Address")
        self.box_serverIP.pack_start(self.serverIPLabel, True, True, 0)

        self.box_spacer01 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box.pack_end(self.box_spacer01, True, True, 0)

        self.serverIPEntry = Gtk.Entry()
        self.box_serverIP.pack_start(self.serverIPEntry, True, True, 0)
        box.pack_end(self.box_serverIP, True, True, 0)

        self.box_username = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.usernameLabel = Gtk.Label("Username")
        self.box_username.pack_start(self.usernameLabel, True, True, 0)

        self.usernameEntry = Gtk.Entry()
        self.box_username.pack_start(self.usernameEntry, True, True, 0)
        box.pack_end(self.box_username, True, True, 0)

        self.box_password = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.passwordLabel = Gtk.Label("Password")
        self.box_password.pack_start(self.passwordLabel, True, True, 0)

        self.passwordEntry = Gtk.Entry()
        self.box_password.pack_start(self.passwordEntry, True, True, 0)
        box.pack_end(self.box_password, True, True, 0)




        box.pack_end(self.box_main, True, True, 0)

        self.show_all()