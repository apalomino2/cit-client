import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gui.Widgets.VMTreeWidget import VMTreeWidget
from gui.Dialogs.VMRetrieveDialog import VMRetrieveDialog
import logging

class ConfigureVMDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Configure Virtual Machine", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
             
        self.vmName = ""
        self.set_default_size(500, 300)

        label = Gtk.Label("Select a VM and Adaptor")

        # Here we will place the tree view
        treeWidget = VMTreeWidget(self)
        self.connect("response", self.dialogResponseActionEvent)
            
        select = treeWidget.treeView.get_selection()
        select.connect("changed", self.onItemSelected)
        
        self.status = None

        box = self.get_content_area()
        box.add(label)
        box.add(treeWidget)
        
        self.show_all()
    
        vmRetrieveDialog = VMRetrieveDialog(self)
        vmRetrieveDialog.run()
        s = vmRetrieveDialog.getFinalData()
        vms = s["mgrStatus"]["vmstatus"]
        vmRetrieveDialog.destroy()
        
        treeWidget.populateTreeStore(vms)
        
    def onItemSelected(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter == None:
            return
        self.vmName = model[treeiter][0]
        self.adaptorSelected = model[treeiter][1]
        if "\"none\"" in self.adaptorSelected or "adaptor disabled" in self.adaptorSelected:
            self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(False)
            return
            
        self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(True)
            
    def dialogResponseActionEvent(self, dialog, responseID):
        # OK was clicked and there is text
        if responseID == Gtk.ResponseType.OK:
            logging.debug("dialogResponseActionEvent(): OK was pressed: " + self.vmName + " " + self.adaptorAdaptorSelected)
        
