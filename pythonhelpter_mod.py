from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction, QLineEdit, QMessageBox

import sys
import os
from pathlib import Path
import sqlite3



#--------------------------------------------------------------------------------------------------
# Will return the length of a database
# Database must be setup in this module
#
# Created: 15July24
#--------------------------------------------------------------------------------------------------

def get_db_length(self):
        conn = sqlite3.connect("python.db")  # Open dBase
        c = conn.cursor()
        c.execute("SELECT * FROM tips")
        items = c.fetchall()
        conn.commit()  # Save Write
        conn.close()  # Close connection

        dB_length = len(items)
        print(f"the dB length is {dB_length}")
        return(dB_length)


#--------------------------------------------------------------------------------------------------
# Critical Pop up Message box
# Notify when out of range of records.
#
# Created: 15July24
#--------------------------------------------------------------------------------------------------



def popup_Critical(self, inMessage):
    msg = QMessageBox()
    msg.setWindowTitle("Critial Error has occured")
    #msg.setText("Wrong Number")
    msg.setText(inMessage)
    msg.setIcon(QMessageBox.Critical)

    x = msg.exec_()