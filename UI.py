import sys
import subprocess
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class PopupWindow(QWidget):
    # Signal to send text back after submit
    submitClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Layout
        self.layout = QGridLayout()

        # Widgets
        self.label = QLabel("Project Title:")
        self.projectNameInput = QLineEdit()
        self.submit = QPushButton("Create")
        self.cancel = QPushButton("Cancel")

        # Add to layout
        self.layout.addWidget(self.label, 0, 0, 1, 1)
        self.layout.addWidget(self.projectNameInput, 0, 1, 1, 5)
        self.layout.addWidget(self.submit, 1, 3, 1, 3, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.cancel, 1, 0, 1, 3, alignment=Qt.AlignCenter)
        self.cancel.clicked.connect(self.cancel_creation)
        self.submit.clicked.connect(self.submit_creation)

        self.setLayout(self.layout)
        self.setWindowTitle("Enter Project Title")
        self.setFixedSize(300, 100)

    def submit_creation(self):
        self.submitClicked.emit(self.projectNameInput.text())
        self.close()

    def cancel_creation(self):
        self.close()


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create Layout
        self.layout = QGridLayout(self)

        # Create Widgets
        self.loginButton = QPushButton("Clasp Login")
        self.refreshLoginStateButton = QPushButton("Refresh Login Status")
        self.createProjectButton = QPushButton("Create New Project")
        self.loginState = QLabel("")
        self.error = QLabel("")
        self.popup = None
        self.output = QTextBrowser()

        # Add Top Bar Widgets
        self.layout.addWidget(self.loginButton, 0, 0, 1, 1, alignment=Qt.AlignTop)
        self.layout.addWidget(self.refreshLoginStateButton, 0, 1, 1, 1, alignment=Qt.AlignTop)
        self.layout.addWidget(self.loginState, 0, 2, 1, 5, alignment=Qt.AlignTop)

        # Add Left Nav Buttons
        self.layout.addWidget(self.createProjectButton, 1, 0, 5, 1, alignment=Qt.AlignTop)

        # Add Middle Output Text
        self.layout.addWidget(self.output, 1, 1, 5, 6, alignment=Qt.AlignTop)

        # Add Footer Widgets
        self.layout.addWidget(self.error, 6, 0, 1, 7, alignment=Qt.AlignCenter)

        # Connect slots
        self.loginButton.clicked.connect(self.login)
        self.refreshLoginStateButton.clicked.connect(self.login_state)
        self.createProjectButton.clicked.connect(self.create_project)

    # Clasp Login
    def login(self):
        try:
            subprocess.check_output("clasp login", shell=True)
        except Exception as e:
            self.error.setText("Clasp Login Failed. Try Again Later\n" + str(e))

    # Clasp Logout
    def logout(self):
        try:
            subprocess.check_output("clasp logout", shell=True)
        except Exception as e:
            self.error.setText("Clasp Logout Failed. Try Again Later\n" + str(e))

    # Check Clasp Login State
    def login_state(self):
        try:
            state = subprocess.check_output("clasp login --status", shell=True)
            self.loginState.setText(state)
        except Exception as e:
            self.error.setText("Couldn't get clasp login state. Try Again Later\n" + str(e))

    # Create popup to get project ID
    def create_project(self):
        if self.popup is None:
            self.popup = PopupWindow()
            self.popup.submitClicked.connect(self.on_create_submit)
        self.popup.show()

    # Slot for getting project name from user input
    def on_create_submit(self, project_name):
        try:
            create_output = subprocess.check_output("clasp create " + project_name, shell=True)
        except Exception as e:
            self.error.setText("Couldn't create clasp project. Try Again Later\n" + str(e))


if __name__ == "__main__":
    app = QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
