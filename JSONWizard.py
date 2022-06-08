# Import Statements
from msilib.schema import File
from PySide2.QtGui import QIcon, QCloseEvent, QKeySequence
from PySide2.QtCore import QSize, Qt, QFile, QTextStream, QModelIndex
from PySide2.QtWidgets import QShortcut, QMessageBox, QPushButton, QLabel, QHBoxLayout, QApplication, QAction, QWidget, QMainWindow, QToolBar, QFileDialog, QFormLayout, QLineEdit
from pathvalidate import ValidationError, validate_filename
import QJSONModel
import json
import os
from JSONView import JSONView

# QApplication Instance
app = QApplication([])

# Set up general Style Sheet
styleSheetFile = QFile("./qss/stylesheet.qss")
styleSheetFile.open(QFile.ReadOnly | QFile.Text)
styleSheet = QTextStream(styleSheetFile)
app.setStyleSheet(styleSheet.readAll())

class JSONWizard(QMainWindow):
    fileCurrentlyOpen = False

    def __init__(self):
        super().__init__()
        
        # Visual Editor (JSONTreeView)
        self.treeView = JSONView(self)
        self.model = QJSONModel.QJsonModel()
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 350)
        # Clear Selection Hotkey
        self.clearSelectionHotkey = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.clearSelectionHotkey.activated.connect(self.treeView.clearSelection)
        self.clearSelectionHotkey.setEnabled(False)
        # Add Tree View to the Window
        self.setCentralWidget(self.treeView)
        # Currently Open File
        self.openFile = ""
        self.unsavedChanges = False
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
        self.toolBar = QToolBar(self)
        self.toolBar.setIconSize(QSize(48,48))
        self.toolBar.setMovable(False)
        self.toolBar.setMinimumHeight(25)
        
        self.setUpToolBar()
        
        self.addToolBar(self.toolBar)       
    
    def setUpToolBar(self):
        self.addValueAction = QAction(QIcon("./icons/add.png"), "Add New Value", self)
        self.addValueAction.triggered.connect(self.addItem)
        self.addValueAction.setDisabled(True)
        
        self.addArrayAction = QAction(QIcon("./icons/addArray.png"), "Add New Array", self)
        self.addArrayAction.triggered.connect(self.addArray)
        self.addArrayAction.setDisabled(True)

        self.addObjectAction = QAction(QIcon("./icons/addObject.png"), "Add New Object", self)
        self.addObjectAction.triggered.connect(self.addObject)
        self.addObjectAction.setDisabled(True)

        self.removeAction = QAction(QIcon("./icons/remove.png"), "Remove Selected Item", self)
        self.removeAction.triggered.connect(self.removeSelectedItem)
        self.removeAction.setDisabled(True)

        self.toolBar.addAction(self.addValueAction)
        self.toolBar.addAction(self.addArrayAction)
        self.toolBar.addAction(self.addObjectAction)
        self.toolBar.addAction(self.removeAction)

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
        saveFileAction = QAction(QIcon("./icons/SaveFile.png"), "Save current file...", self)
        saveFileAction.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
        saveFileAction.setShortcutVisibleInContextMenu(True)
        saveFileAction.triggered.connect(self.saveCurrentFile)
        # TODO Menu Item for Saving the current file as a new file (with hotkey Shift-Ctrl-S)
        saveAsFileAction = QAction(QIcon("./icons/SaveFile.png"), "Save current file as...", self)
        saveAsFileAction.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_S))
        saveAsFileAction.setShortcutVisibleInContextMenu(True)
        saveAsFileAction.triggered.connect(self.saveAsCurrentFile)
        # TODO Menu Item for Converting from JSON to another file type?

        # Add all menu items
        file_menu.addAction(createFileAction)
        file_menu.addAction(openFileAction)
        file_menu.addAction(saveFileAction)
        file_menu.addAction(saveAsFileAction)

        # TODO Set Up Help Menu
        help_menu = menu.addMenu("Help")

    def isFileOpen(self) -> bool:
        return self.fileCurrentlyOpen

    def openCreateFileMenu(self):
        if self.createFileWindow is None:
            self.createFileWindow = FileCreationWindow()
        self.createFileWindow.show()
    
    def openFileExplorer(self):
        fileTuple = QFileDialog.getOpenFileName(self, "Open JSON File", "./", "JSON Files (*.json)")
        fileNameAndPath = fileTuple[0]
        fileNameAndPath.replace('\\','/')
        self.openFile = fileNameAndPath
        self.openNewFile()

    def openNewFile(self):
        with open(self.openFile, "r+") as file:
            if os.stat(self.openFile).st_size != 0:
                document = json.load(file)
            else:
                document = {}
                json.dump(document, file)
            self.model.load(document)

        self.fileCurrentlyOpen = True
        self.addValueAction.setDisabled(False)
        self.addObjectAction.setDisabled(False)
        self.addArrayAction.setDisabled(False)
        self.removeAction.setDisabled(False)
        self.clearSelectionHotkey.setEnabled(True)
        
    def saveCurrentFile(self):
        saveStateDict = self.model.json()
        with open(self.openFile, "w") as file:
            json.dump(saveStateDict, file, indent=4)

    def saveAsCurrentFile(self):
        saveStateDict = self.model.json()
        fileTuple = QFileDialog.getSaveFileName(self, "Save JSON File", "./", "JSON Files (*.json)")
        fileNameAndPath = fileTuple[0]
        fileNameAndPath.replace('\\','/')
        self.openFile = fileNameAndPath
        with open(self.openFile, "w") as file:
            json.dump(saveStateDict, file, indent=4)
    
    def addItem(self):
        # Get the currently selected object
        if len(self.treeView.selectedIndexes()) > 0:
            currentIndex = self.treeView.selectedIndexes()[0]
            parentIndex = currentIndex.parent()
        # If none selected, use root
        else:
            currentIndex = None
            parentIndex = QModelIndex()
        self.model.insertRow(currentIndex, str, parentIndex)
        if currentIndex:
            self.treeView.expand(currentIndex)
        self.treeView.clearSelection()

    def addArray(self):
        # Get the currently selected object
        if len(self.treeView.selectedIndexes()) > 0:
            currentIndex = self.treeView.selectedIndexes()[0]
            parentIndex = currentIndex.parent()
        # If none selected, use root
        else:
            currentIndex = None
            parentIndex = QModelIndex()
        self.model.insertRow(currentIndex, list, parentIndex)
        if currentIndex:
            self.treeView.expand(currentIndex)
        self.treeView.clearSelection()

    def addObject(self):
        # Get the currently selected object
        if len(self.treeView.selectedIndexes()) > 0:
            currentIndex = self.treeView.selectedIndexes()[0]
            parentIndex = currentIndex.parent()
        # If none selected, use root
        else:
            currentIndex = None
            parentIndex = QModelIndex()
        self.model.insertRow(currentIndex, dict, parentIndex)
        if currentIndex:
            self.treeView.expand(currentIndex)
        self.treeView.clearSelection()

    def removeSelectedItem(self):
        # Get the currently selected object
        currentIndex = self.treeView.currentIndex()
        currentItem = self.treeView.model().data(currentIndex, Qt.EditRole)
        # If the object has children, do a confirm deletion pop-up
        if currentItem.childCount() > 0:
            messageBox = QMessageBox()
            confirmation = messageBox.question(self, "Delete Confirmation", "Are you sure you want to delete this item and all of its children?", messageBox.Yes | messageBox.No)
            if confirmation == messageBox.No:
                return
        
        self.model.removeRow(currentIndex.row(), currentIndex.parent())

mainPage = JSONWizard()
mainPage.show()

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

        layout.addRow(hbox3)

        # Create Error Label that displays when something goes wrong
        self.errorLabel = QLabel("ERROR LABEL")
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.errorLabel.setStyleSheet("color: red; font-size: 16px")
        self.errorLabel.hide()


        layout.addRow(self.errorLabel)
        # Set Layout of the Window
        self.setLayout(layout)
    
    # Function to validate entered file name and selected path
    def validateInput(self):
        fileName = self.fileNameField.text()
        path = self.filePathField.text()
        if len(fileName) == 0:
            self.errorLabel.setText("*Error: Please enter a file name!*")
            self.errorLabel.show()
        elif len(path) == 0:
            self.errorLabel.setText("*Error: Please select a file path!*")
            self.errorLabel.show()
        else:
            try:
                fileName += ".json"
                validate_filename(fileName)
            except ValidationError:
                self.errorLabel.setText("*Error: Please enter a VALID file name!*")
                self.errorLabel.show()
            else:
                self.errorLabel.hide()
                self.createNewJsonFile(fileName, path)
 
    # Function to Create New JSON Files
    def createNewJsonFile(self, fileName, filePath):
        fileNameAndPath = filePath + "/" + fileName
        try:
            open(fileNameAndPath, 'x')
        except FileExistsError:
            self.errorLabel.setText("*Error: File already exists!*")
            self.errorLabel.show()
        except:
            self.errorLabel.setText("*WEIRD OS ERROR, SHOULD BE UNREACHABLE*")
            self.errorLabel.show()
        else:
            fileNameAndPath.replace('\\','/')
            mainPage.openFile = fileNameAndPath
            mainPage.openNewFile()
            self.close()
            
    # Function to open screen where user can select the directory for their new file
    def openPathSelectionScreen(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_():
            directoryName = dialog.selectedFiles()[0]
            self.filePathField.setText(directoryName)
    
    # Function to Wipe the Form after it is closed
    def closeEvent(self, event: QCloseEvent) -> None:
        super().closeEvent(event)
        self.errorLabel.hide()
        self.fileNameField.clear()
        self.filePathField.clear()
    
# Start App Loop, Code Below this will not execute until application is exited
app.exec_()
