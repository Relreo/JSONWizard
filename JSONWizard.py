# Import Statements
import sys
from PySide2.QtCore import QSize, Qt, QFile, QTextStream
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGroupBox, QVBoxLayout


# QApplication Instance
app = QApplication([])

# Set up Style Sheet
styleSheetFile = QFile("./qss/stylesheet.qss")
styleSheetFile.open(QFile.ReadOnly | QFile.Text)
styleSheet = QTextStream(styleSheetFile)
app.setStyleSheet(styleSheet.readAll())

# Entry Point for Program, and Main Menu for opening and creating files
class JSONWizard(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window Title and Size
        self.setWindowTitle("JSONWizard")
        self.setMinimumSize(720, 480)

        # Set up Menu Bar

        # Set up Visual Editor
        

        

mainPage = JSONWizard()
mainPage.show()




# Start App Loop, Code Below this will not execute until application is exited
app.exec_()
