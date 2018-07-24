import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gui.Widgets.VMTreeWidget import VMTreeWidget

class ConfigureVMDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Configure Virtual Machine", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
             
        self.vmName = ""
        self.set_default_size(350, 100)

        label = Gtk.Label("Select a VM and Adaptor")

        # Here we will place the tree view
        treeWidget = VMTreeWidget()
        self.connect("response", self.dialogResponseActionEvent)

        treeWidget.populateTreeStore(['a', 'b'])
        select = treeWidget.treeView.get_selection()
        select.connect("changed", self.onItemSelected)
        
        self.status = None

        box = self.get_content_area()
        box.add(label)
        box.add(treeWidget)
        
        self.show_all()
        
    def onItemSelected(self, selection):
        model, treeiter = selection.get_selected()

        if treeiter == None:
            return

        self.vmName = model[treeiter][0]
            
    def dialogResponseActionEvent(self, dialog, responseID):
        # OK was clicked and there is text
        if responseID == Gtk.ResponseType.OK:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "OK Button pressed, " + self.vmName + " selected")
            dialog.run()
            dialog.destroy()
