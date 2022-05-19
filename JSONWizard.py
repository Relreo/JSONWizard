# Import Statements
from fileinput import filename
import sys, json
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize, Qt, QFile, QTextStream
from PySide2.QtWidgets import QApplication, QAction, QMenu, QMainWindow, QToolBar, QFileDialog

# Currently Open File
openFile = None
# QApplication Instance
app = QApplication([])

# Set up Style Sheet
styleSheetFile = QFile("./qss/stylesheet.qss")
styleSheetFile.open(QFile.ReadOnly | QFile.Text)
styleSheet = QTextStream(styleSheetFile)
app.setStyleSheet(styleSheet.readAll())

# Main Program Window
class JSONWizard(QMainWindow):
    
    def __init__(self):
        super().__init__()
        # Window Title and Size
        self.setWindowTitle("JSONWizard")
        self.setMinimumSize(980, 640)
        appIcon = QIcon("./icons/appIcon.png")
        self.setWindowIcon(appIcon)

        openFile = None
        fileOpen = False
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
        createFileAction = QAction(QIcon("./icons/JSONFile.png"), "Create new JSON file...", self)
        createFileAction.triggered.connect(self.openCreateFileMenu())
        openFileAction = QAction(QIcon("./icons/JSONFile.png"), "Open existing JSON file...", self)
        openFileAction.triggered.connect(self.openFileExplorer)

        file_menu.addAction(createFileAction)
        file_menu.addAction(openFileAction)

        # Set Up Help Menu
        help_menu = menu.addMenu("Help")

        # file_menu.addAction()

    def openCreateFileMenu(self):
        pass
    
    def openFileExplorer(self):
        fileTuple = QFileDialog.getOpenFileName(self, "Open JSON File", "./", "JSON Files (*.json)")
        self.openFile = fileTuple[0]
        self.fileOpen = True

    
        

        

mainPage = JSONWizard()
mainPage.show()




# Start App Loop, Code Below this will not execute until application is exited
app.exec_()
