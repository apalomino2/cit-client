import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import logging
from gui.Dialogs.ConfigureVMDialog import ConfigureVMDialog


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

class VMManageBox(Gtk.ListBox):

    def __init__(self, parent):
        super(VMManageBox, self).__init__()
        logging.debug("Creating VMManageBox")
        self.parent = parent
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        ####Lower ListBox (Virtual Machine Configuration)
        self.vmManageListBox = Gtk.ListBox()
        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.vmManageBoxDescLabel = Gtk.Label(xalign=0)
        self.vmManageBoxDescLabel.set_markup("<b>Virtual Machine Configuration</b>")
        self.hbox.pack_start(self.vmManageBoxDescLabel, True, True, 0)
        self.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.vmSelectDescLabel = Gtk.Label("Virtual Machine Status: ", xalign=0)
        self.hbox.pack_start(self.vmSelectDescLabel, True, True, 0)

        self.vmStatusLabel = Gtk.Label(" Not Configured ", xalign=0)
        self.vmStatusEventBox = Gtk.EventBox()
        self.vmStatusEventBox.add(self.vmStatusLabel)
        self.vmStatusEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 0, 0, .5))
        self.hbox.pack_start(self.vmStatusEventBox, False, True, 0)
        self.configVMButton = Gtk.Button("Configure")
        self.configVMButton.connect("clicked", self.configureVM)
        self.configVMButton.props.valign = Gtk.Align.CENTER
        self.hbox.pack_start(self.configVMButton, False, True, 0)
        self.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.vmNameDescLabel = Gtk.Label("Virtual Machine Name:", xalign=0)
        self.vmNameLabel = Gtk.Label("")
        self.vmNameLabel.set_markup("<i>Not ConfiguredAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</i>")

        self.vmActionHBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        image = Gtk.Image(stock=Gtk.STOCK_MEDIA_PLAY)
        self.startVMButton = Gtk.Button(image=image)
        self.startVMButton.set_tooltip_text("Start Virtual Machine")
        self.startVMButton.set_sensitive(False)
        self.startVMButton.connect("clicked", self.vmAction)
        self.startVMButton.props.valign = Gtk.Align.CENTER

        image = Gtk.Image(stock=Gtk.STOCK_MEDIA_PAUSE)
        self.suspendVMButton = Gtk.Button(image=image)
        self.suspendVMButton.set_tooltip_text("Stop Virtual Machine")
        self.suspendVMButton.set_sensitive(False)
        self.suspendVMButton.connect("clicked", self.vmAction)
        self.suspendVMButton.props.valign = Gtk.Align.CENTER
        self.vmActionHBox.pack_start(self.startVMButton, False, True, 0)
        self.vmActionHBox.pack_start(self.suspendVMButton, False, True, 0)

        self.hbox.pack_start(self.vmNameDescLabel, False, True, 0)
        self.hbox.pack_start(self.vmNameLabel, True, True, 0)
        self.hbox.pack_start(self.vmActionHBox, False, True, 0)
        self.add(self.row)

        self.show_all()

    def configureVM(self, button):
        logging.debug("configureVM(): initiated")
        logging.debug("configureVM(): Button Label: " + button.get_label())
        configureVMDialog = ConfigureVMDialog(self.parent)
        response = configureVMDialog.run()
        if response == Gtk.ResponseType.OK:
            self.vmStatusLabel.set_label(" Connected ")
            self.vmStatusEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0, 1, 0, .5))
        elif response == Gtk.ResponseType.CANCEL:
            {}
        configureVMDialog.destroy()

    def vmAction(self, button):
        logging.debug("configureVM(): initiated")
        logging.debug("configureVM(): Button pressed was: " + button.get_tooltip_text())