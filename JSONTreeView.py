from PySide2.QtWidgets import QTreeView
from PySide2.QtCore import QFile

class JSONTreeView(QTreeView):

    # TODO Constructor
    def __init__(self):
        super().__init__()
    
    # TODO Function for Loading a New File
    def loadJSONFile(self, JSONFile: QFile):
        pass


