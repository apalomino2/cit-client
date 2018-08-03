import logging
import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from engine.Engine import Engine

class VMTreeWidget(Gtk.Grid):

    def __init__(self):
        logging.debug("Creating VMTreeWidget")
        super(VMTreeWidget, self).__init__()

        self.set_border_width(5)
        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        
        self.liststore_manufacturers = Gtk.ListStore(str)
        self.adaptors = ["Sony", "LG",
            "Panasonic", "Toshiba", "Nokia", "Samsung"]
        #for item in self.manufacturers:
        #    self.liststore_manufacturers.append([item])

        # Initialized fields
        self.treeStore = Gtk.TreeStore(str)
        self.treeView = Gtk.TreeView(self.treeStore)
        self.scrollableTreeList = Gtk.ScrolledWindow()
        
        self.drawTreeView()
        self.setLayout()

    def populateTreeStore(self, registeredVMList):
        for vm in registeredVMList:
            treeIter = self.treeStore.append(None, [vm])

    def drawTreeView(self):
        renderer = Gtk.CellRendererText()
        renderer_combo = Gtk.CellRendererCombo()
        renderer_combo.set_property("editable", True)
        renderer_combo.set_property("model", self.liststore_manufacturers)
        renderer_combo.set_property("text-column", 0)
        renderer_combo.set_property("has-entry", False)
        
        vmColumn = Gtk.TreeViewColumn("Virtual Machine", renderer, text=0)
        adaptorColumn = Gtk.TreeViewColumn("Adaptor", renderer_combo, text=0)
        self.treeView.append_column(vmColumn)
        self.treeView.append_column(adaptorColumn)

    def setLayout(self):
        self.scrollableTreeList.set_min_content_width(100)
        self.scrollableTreeList.set_min_content_height(100)
        self.scrollableTreeList.set_vexpand(True)
        self.attach(self.scrollableTreeList, 0, 0, 4, 10)
        self.scrollableTreeList.add(self.treeView)
