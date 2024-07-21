# -------------------------------------------------------------------------------
# Name:             Generic Startup Loading a UI File
# Purpose:          Simplify a GUI interface app
#
# Author:           Jeffreaux
#
# Created:          20Mar23
#
# Required Packages:    PyQt5, PyQt5-Tools
# -------------------------------------------------------------------------------

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QAction,
    QTabWidget,
    QLabel,
    QPlainTextEdit,
    QLineEdit,
    QTextEdit,
)

from pythonhelpter_mod import *
from PyQt5 import uic
import sys
import sqlite3
import random

# Create dBase and create cursor
conn = sqlite3.connect("python.db")
c = conn.cursor()

command_create_table = """
                    CREATE TABLE IF NOT EXISTS tips(
                    id INTEGER PRIMARY KEY,
                    method_name TEXT,
                    keywords TEXT,
                    description TEXT
                    )"""

c.execute(command_create_table)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi("PythonHelper_GUI.ui", self)

        # define Widgets ##########################################################################
        self.tab = self.findChild(QTabWidget, "tab")

        self.btnExit = self.findChild(QPushButton, "btnExit")
        self.btnIndexForward = self.findChild(QPushButton, "btnIndexForward")
        self.btnIndexBack = self.findChild(QPushButton, "btnIndexBack")
        self.btnSaveRecord = self.findChild(QPushButton, "btnSaveRecord")
        self.btnGo = self.findChild(QPushButton, "btnGo")
        self.btnEditRecord = self.findChild(QPushButton, "btnEditRecord")
        self.btnCancelEdit = self.findChild(QPushButton, "btnCancelEdit")
        self.btnUpdateRecord = self.findChild(QPushButton, "btnUpdateRecord")

        self.txtKeyWords = self.findChild(QLineEdit, "txtKeyWords")
        self.txtMethod = self.findChild(QLineEdit, "txtMethod")
        self.txtSearchKeywords = self.findChild(QLineEdit, "txtSearchKeywords")
        self.txtSearchMethod = self.findChild(QLineEdit, "txtSearchMethod")
        self.txtSearchIndex = self.findChild(QLineEdit, "txtSearchIndex")
        self.txtSearchMethod = self.findChild(QLineEdit, "txtSearchMethod")
        self.pteResults = self.findChild(QPlainTextEdit, "pteResults")
        self.pteSearchResults = self.findChild(QPlainTextEdit, "pteSearchResults")
        self.txtInput = self.findChild(QTextEdit, "txtInput")
        self.txtEditMethod = self.findChild(QLineEdit, "txtEditMethod")
        self.txtEditKeyWords = self.findChild(QLineEdit, "txtEditKeyWords")
        self.txtEdit = self.findChild(QTextEdit, "txtEdit")

        self.lblKeyWords = self.findChild(QLabel, "lblKeyWords")
        self.lblMethod = self.findChild(QLabel, "lblMethod")
        self.lblCurrentIndex = self.findChild(QLabel, "lblCurrentIndex")

        self.actExit = self.findChild(QAction, "actExit")

        # Define the actions ######################################################################
        self.btnExit.clicked.connect(self.closeEvent)
        self.btnIndexForward.clicked.connect(self.index_forward)
        self.btnIndexBack.clicked.connect(self.index_back)
        self.btnSaveRecord.clicked.connect(self.write_to_dB)
        self.btnGo.clicked.connect(self.go_search)
        self.btnEditRecord.clicked.connect(self.record_to_edit)
        self.btnCancelEdit.clicked.connect(self.cancel_edit)
        self.btnEditRecord.clicked.connect(self.edit_record)
        self.btnUpdateRecord.clicked.connect(self.write_record)

        self.txtSearchMethod.returnPressed.connect(self.search_method_name)
        self.txtSearchIndex.returnPressed.connect(self.go_search)

        self.actExit.triggered.connect(self.closeEvent)

        # Show the app
        self.show()

        self.get_random_index()
        self.tab.setTabVisible(3, False)  # Makes Tab invisible

        # Show Home tab at startup
        self.tab.setCurrentIndex(0)

    def write_to_dB(self):
        method_name = self.txtMethod.text()
        print(method_name)
        keywords = self.txtKeyWords.text()
        #print(keywords)
        description = self.txtInput.toPlainText()
        #print(description)

        conn = sqlite3.connect("python.db")  # Open dBase
        c = conn.cursor()  # Create Cursor
        # Write Data
        c.execute(
            "INSERT INTO tips (method_name, keywords, description) VALUES (? ,? ,?)",
            (method_name, keywords, description),
        )
        conn.commit()  # Save Write
        conn.close()  # Close connection

        self.tab.setCurrentIndex(0)
        self.txtMethod.clear()
        self.txtKeyWords.clear()
        self.txtInput.clear()
        self.current_index = get_db_length(self)
        self.lblCurrentIndex.setText(str(self.current_index))

    def index_forward(self):
        # print("Record will index forward one record")
        eDb = get_db_length(self)
        if self.current_index >= eDb:
            self.current_index == eDb
            # print("Already at the last record")
            popup_Critical(self, "At the last Record")
        else:
            self.current_index = int(self.current_index) + 1
            self.lblCurrentIndex.setText(str(self.current_index))
            # print(self.current_index)
            self.get_random_record()

    def index_back(self):
        # print("Record will index back one record")
        if self.current_index <= 1:  # Test to stay in range of available records
            self.current_index == 1
            # print("At the First record")
            popup_Critical(self, "At the first Record")
        else:
            self.current_index = int(self.current_index) - 1
            self.lblCurrentIndex.setText(str(self.current_index))
            # print(self.current_index)
            self.get_random_record()

    def get_random_index(self):
        min_value = 1
        max_value = get_db_length(self)
        print(max_value)
        self.current_index = random.randint(min_value, max_value)
        self.lblCurrentIndex.setText(str(self.current_index))
        print(f"The Random number is {self.current_index}")
        self.get_random_record()

    def get_random_record(self):
        self.pteResult.clear()
        print(f"The random generated current index is {self.current_index}")
        conn = sqlite3.connect("python.db")  # Open dBase
        c = conn.cursor()  # Create Cursor
        c.execute(f"SELECT * FROM tips WHERE id ='{self.current_index}'")

        rlist = c.fetchone()

        conn.commit()  # Save Write
        conn.close()  # Close connection

        # print(f"{rlist[0]}, {rlist[1]}, {rlist[2]}, {rlist[3]}")
        # Fill form with results
        self.lblMethod.setText(rlist[1])
        self.lblKeyWords.setText(rlist[2])
        self.pteResult.appendPlainText(rlist[3])
        # Update the current indes
        self.lblCurrentIndex.setText(str(self.current_index))
        # Return to home form
        self.tab.setCurrentIndex(0)

    def search_method_name(self):
        print("Searching through state names")
        self.pteSearchResults.clear()
        conn = sqlite3.connect("python.db")  # Opening dB for reading
        c = conn.cursor()
        method_name_search = self.txtSearchMethod.text()

        c.execute(
            "SELECT * FROM tips WHERE method_name LIKE (?) ",
            (method_name_search + "%",),
        )
        items = c.fetchall()
        # Close Connection
        conn.commit()
        conn.close()

        for item in items:
            line = f"{item[0]}, {item[1]}"
            # print(line)
            self.pteSearchResults.appendPlainText(line)

    def record_to_edit(self):
        self.pteResult.clear()
        print(f"The random generated current index is {self.current_index}")
        conn = sqlite3.connect("python.db")  # Open dBase
        c = conn.cursor()  # Create Cursor
        c.execute(f"SELECT * FROM tips WHERE id ='{self.current_index}'")

        rlist = c.fetchone()

        conn.commit()  # Save Write
        conn.close()  # Close connection

        self.txtEditMethod.setText(rlist[1])
        self.txtEditKeyWords.setText(rlist[2])
        self.txtEdit.setText(rlist[3])
        # Update the current indes
        self.lblCurrentIndex.setText(str(self.current_index))
        # Return to home form
        self.tab.setCurrentIndex(3)

    def cancel_edit(self):
        self.tab.setCurrentIndex(0)

    def go_search(self):
        self.current_index = int(self.txtSearchIndex.text())  # Get index to display
        print(self.current_index)
        print(type(self.current_index))
        self.get_random_record()  # Display the requested record
        self.pteSearchResults.clear()  # Clearing results from previous search
        self.txtSearchIndex.clear()  # Clear box for next request

    def write_record(self):
        print(f"Edit record {self.current_index}")
        tmp = self.txtEditMethod.text()
        conn = sqlite3.connect("python.db")  # Open dBase
        c = conn.cursor()  # Create Cursor

        c.execute(
            "UPDATE tips SET method_name=?, keywords=?, description=? WHERE id=?",
            (
                self.txtEditMethod.text(),
                self.txtEditKeyWords.text(),
                self.txtEdit.toPlainText(),
                self.current_index,
            ),
        )

        # Close Connection
        conn.commit()
        conn.close()
        self.tab.setCurrentIndex(0)
        #print(f"The current index is {self.current_index} after running")
        self.get_random_record()

    def edit_record(self):
        self.tab.setCurrentIndex(3)

    def closeEvent(self, *args, **kwargs):
        # print("Program closed Successfully!")
        self.close()


# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
