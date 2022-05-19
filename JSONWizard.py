# Import Statements
import sys, json
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize, Qt, QFile, QTextStream
from PySide2.QtWidgets import QApplication, QAction, QWidget, QMainWindow, QToolBar, QFileDialog, QVBoxLayout

# Currently Open File
openFile = None
# QApplication Instance
app = QApplication([])

# Set up Style Sheet
styleSheetFile = QFile("./qss/stylesheet.qss")
styleSheetFile.open(QFile.ReadOnly | QFile.Text)
styleSheet = QTextStream(styleSheetFile)
app.setStyleSheet(styleSheet.readAll())

class FileCreationWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Set Window Settings for Pop Up Menu
        self.setWindowTitle("Create New JSON File")
        self.setMinimumSize(490, 320)
        self.setWindowModality(Qt.ApplicationModal)

        # Set Layout of the Window
        layout = QVBoxLayout()
        self.setLayout(layout)

# Main Program Window
class JSONWizard(QMainWindow):
    
    def __init__(self):
        super().__init__()
        # Set up popup create file window
        self.createFileWindow = None

        # Window Title and Size
        self.setWindowTitle("JSONWizard")
        self.setMinimumSize(980, 640)
        appIcon = QIcon("./icons/appIcon.png")
        self.setWindowIcon(appIcon)

        # Create Menu Bar
        self.setUpMenuBar()
        # Create Tool Bar
        toolBar = QToolBar()
        toolBar.setIconSize(QSize(64,64))
        toolBar.setMovable(False)
        toolBar.setMinimumHeight(25)
        
        
        self.addToolBar(toolBar)
        # Set up Visual Editor
    
    def setUpMenuBar(self):
        menu = self.menuBar()
        # Set Up File Menu
        file_menu = menu.addMenu("File")
        # Menu Item for creating new JSON files
        createFileAction = QAction(QIcon("./icons/JSONFile.png"), "Create new JSON file...", self)
        createFileAction.triggered.connect(self.openCreateFileMenu)
        # Menu Item for opening existing JSON files
        openFileAction = QAction(QIcon("./icons/JSONFile.png"), "Open existing JSON file...", self)
        openFileAction.triggered.connect(self.openFileExplorer)
        # Menu Item for Saving the Current File (with hotkey Ctrl-S)

        # Menu Item for Saving the current file as a new file (with hotkey Shift-Ctrl-S)

        # Add all menu items
        file_menu.addAction(createFileAction)
        file_menu.addAction(openFileAction)

        # Set Up Help Menu
        help_menu = menu.addMenu("Help")

        # file_menu.addAction()

    def openCreateFileMenu(self):
        if self.createFileWindow is None:
            self.createFileWindow = FileCreationWindow()
        self.createFileWindow.show()
        
    
    def openFileExplorer(self):
        fileTuple = QFileDialog.getOpenFileName(self, "Open JSON File", "./", "JSON Files (*.json)")
        self.openFile = fileTuple[0]
        self.fileOpen = True

    def saveCurrentFile(self):
        pass

    def saveAsCurrentFile(self):
        pass

    
        

        

mainPage = JSONWizard()
mainPage.show()





# Start App Loop, Code Below this will not execute until application is exited
app.exec_()
