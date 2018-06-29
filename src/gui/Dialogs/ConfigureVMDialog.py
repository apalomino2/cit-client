import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ConfigureVMDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Configure Virtual Machine", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Configure VM for EmuBox")

        box = self.get_content_area()
        box.add(label)
        self.show_all()