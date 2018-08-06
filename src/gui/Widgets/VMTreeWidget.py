import logging
import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from engine.Engine import Engine

class VMTreeWidget(Gtk.Grid):

    def __init__(self, parent):
        self.parent = parent
        self.vmList = []
        logging.debug("Creating VMTreeWidget")
        super(VMTreeWidget, self).__init__()

        self.set_border_width(5)
        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        
        self.liststore_manufacturers = Gtk.ListStore(str)        

        # Initialized fields
        self.treeStore = Gtk.TreeStore(str, str)
        self.treeView = Gtk.TreeView(self.treeStore)
        self.scrollableTreeList = Gtk.ScrolledWindow()
        
        self.drawTreeView()
        self.setLayout()

    def populateTreeStore(self, vmList):
        self.vmList = vmList
        for vm in self.vmList:
            logging.debug("populateTreeStore(): working with: " + str(vm))
            adaptor = str("1 - " + self.vmList[vm]["adaptorInfo"]["1"])
            if "\"none\"" in adaptor:
                adaptor = "1 - *adaptor disabled*"
            treeIter = self.treeStore.append(None, [vm, adaptor])
        self.adaptors = ["1", "2",
            "3", "4", "5", "6", "7", "8"]
        for item in self.adaptors:
            self.liststore_manufacturers.append([item])

    def drawTreeView(self):
        renderer = Gtk.CellRendererText()
        renderer_combo = Gtk.CellRendererCombo()
        renderer_combo.set_property("editable", True)
        renderer_combo.set_property("model", self.liststore_manufacturers)
        renderer_combo.set_property("text-column", 0)
        renderer_combo.set_property("has-entry", False)
        renderer_combo.connect("edited", self.on_combo_changed)
        
        vmColumn = Gtk.TreeViewColumn("Virtual Machine", renderer, text=0)
        adaptorColumn = Gtk.TreeViewColumn("Adaptor", renderer_combo, text=1)
        self.treeView.append_column(vmColumn)
        self.treeView.append_column(adaptorColumn)
        
    def on_combo_changed(self, widget, path, text):
        logging.debug("on_combo_changed(): widget: " + str(widget) + " path: " + str(path) + " text: " + str(text))
        chosenAdaptor = self.vmList[self.treeStore[path][0]]["adaptorInfo"][str(text)]
        if "\"none\"" in chosenAdaptor or "adaptor disabled" in chosenAdaptor:
            inputErrorDialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK, "The chosen adaptor is not currently enabled.\r\nChoose another adaptor.")
            inputErrorDialog.run()
            inputErrorDialog.destroy()
            return
        self.treeStore[path][1] = text + " - " + chosenAdaptor
        
    def setLayout(self):
        self.scrollableTreeList.set_min_content_width(100)
        self.scrollableTreeList.set_min_content_height(100)
        self.scrollableTreeList.set_vexpand(True)
        self.attach(self.scrollableTreeList, 0, 0, 4, 10)
        self.scrollableTreeList.add(self.treeView)
