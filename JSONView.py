from PySide2.QtWidgets import QTreeView

class JSONView(QTreeView):
    def __init__(self, parent = None):
        super().__init__()
        self.parentWindow = parent
    
    def selectionChanged(self, selected, deselected):
        # Does nothing at the moment but could be useful in the future
        pass

    