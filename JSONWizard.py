# Import Statements
from fileinput import filename
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize, Qt, QFile, QTextStream
from PySide2.QtWidgets import QStyle, QPushButton, QLabel, QHBoxLayout, QApplication, QAction, QWidget, QMainWindow, QToolBar, QFileDialog, QFormLayout, QLineEdit
import sys
from pathvalidate import ValidationError, validate_filename

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
        # Local Variables
        minTextFieldHeight = 25
        buttonWidth = 150
        buttonHeight = 30
        # Set Window Settings for Pop Up Menu
        self.setWindowTitle("Create New JSON File")
        self.setMinimumSize(490, 320)
        self.setWindowModality(Qt.ApplicationModal)
        appIcon = QIcon("./icons/appIcon.png")
        self.setWindowIcon(appIcon)

        # Create UI Elements and add them to the Form Layout
        layout = QFormLayout()
        layout.setMargin(80)
        layout.setVerticalSpacing(50)

        # Create and Configure File Name Field
        hbox = QHBoxLayout()

        self.fileNameField = QLineEdit()
        self.fileNameField.setMaxLength(250)
        self.fileNameField.setMinimumHeight(minTextFieldHeight)
        self.fileNameField.setPlaceholderText("Enter file name <= 255 characters ")
        hbox.addWidget(self.fileNameField)

        self.fileExtensionLabel = QLabel(" .json")
        self.fileExtensionLabel.setScaledContents(True)
        hbox.addWidget(self.fileExtensionLabel)
        # Add to Layout
        layout.addRow("Save As: ", hbox)

        # Create and Configure File Path Field and Selection Button
        hbox2 = QHBoxLayout()

        self.filePathField = QLineEdit()
        self.filePathField.setPlaceholderText("Select a valid file path")
        self.filePathField.setReadOnly(True)
        self.filePathField.setMinimumHeight(minTextFieldHeight)
        hbox2.addWidget(self.filePathField)

        self.filePathSelectionButton = QPushButton("Select Path")
        self.filePathSelectionButton.clicked.connect(self.openPathSelectionScreen)
        hbox2.addWidget(self.filePathSelectionButton)
        # Add to the Layout
        layout.addRow("Select new file path: ", hbox2)

        # Create and Configure Confirm and Cancel Buttons
        hbox3 = QHBoxLayout()
        hbox3.setAlignment(Qt.AlignCenter)

        # Custom Cancel Button Style Sheet Setup
        styleSheetFile = QFile("./qss/cancelButton.qss")
        styleSheetFile.open(QFile.ReadOnly | QFile.Text)
        styleSheet = QTextStream(styleSheetFile)
        # Cancel Button Setup
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setStyleSheet(styleSheet.readAll())
        self.cancelButton.setFixedWidth(buttonWidth)
        self.cancelButton.setFixedHeight(buttonHeight)
        self.cancelButton.clicked.connect(self.close)
        hbox3.addWidget(self.cancelButton)

        hbox3.addSpacing(25)
        # Confirm button Setup
        self.confirmButton = QPushButton("Create File")
        self.confirmButton.setFixedWidth(buttonWidth)
        self.confirmButton.setFixedHeight(buttonHeight)
        self.confirmButton.clicked.connect(self.validateInput)
        hbox3.addWidget(self.confirmButton)
        # Add to layout
        layout.addRow(hbox3)
        # Set Layout of the Window
        self.setLayout(layout)
    
    # Function to validate entered file name and selected path
    def validateInput(self):
        fileName = self.fileNameField.text()
        if not fileName:
            # Error Handling!
            pass
        path = self.filePathField.text()
        if not path:
            # Error Handling!
            pass
            
    # Function to Create New JSON Files
    def createNewJsonFile(self, filePath):
        # Create New JSON File

        pass

    # Function to open screen where user can select the directory for their new file
    def openPathSelectionScreen(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_():
            directoryName = dialog.selectedFiles()[0]
            self.filePathField.setText(directoryName)
    
            


# Main Program Window
class JSONWizard(QMainWindow):
    
    def __init__(self):
        super().__init__()
        # Currently Open File
        self.openFile = None
        self.openFilePath = None
        self.fileCurrentlyOpen = False
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

        # Menu Item for Converting from JSON to another file type?

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
        self.openFilePath = fileTuple[0]
        self.fileCurrentlyOpen = True

    def saveCurrentFile(self):
        pass

    def saveAsCurrentFile(self):
        pass

    
        

        

mainPage = JSONWizard()
mainPage.show()





# Start App Loop, Code Below this will not execute until application is exited
app.exec_()
