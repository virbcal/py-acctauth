# ---------------------------------------------------------------------
# Copyright (c) 2001-2021 CALIMLIM Enterprises. All rights reserved.
#
# Author: Virgilio B Calimlim, 2021/01
# ---------------------------------------------------------------------
# Progname   : gAcctLgn.py
# Description: Account login
# System     : Access Authorization
# Purpose    : Authentication 
# ---------------------------------------------------------------------
# Revisions  :
# 0.0   2021-01-17 virbcal  Initial release;
# ---------------------------------------------------------------------

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QFrame,
                             QLineEdit, QPushButton,
                             QHBoxLayout, QVBoxLayout, QFormLayout,
                             QMessageBox)
from ceutils import lginval as lgn
#uff.savelist(dir(main.dev._widget),itemized=True,popup=True)

def version():
    # Function: Return version number.
    return os.path.basename(__file__)[:-3]+' 0.0'

class AppMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lblhdln = QLabel('<center>Login to Account</center>')
        lbluid  = QLabel('Userid')
        lblupwd = QLabel('Password')
        self.result = QLabel('Please login to access your account.')

       #lblusid.clicked.connect(self.onHelpUsid) 
       #lblupwd.clicked.connect(self.onHelpUpwd) 

        frame = QFrame()
        frame.setFrameShadow(QFrame.Sunken)
        frame.setFrameShape(QFrame.HLine)

        self.leuid  = QLineEdit()
        self.leupwd = QLineEdit()

        self.leuid.setPlaceholderText('Userid')
        self.leupwd.setPlaceholderText('Password')
        self.leupwd.setEchoMode(QLineEdit.Password)

        subbtn = QPushButton("Submit")
        subbtn.clicked.connect(self.onSubmit)
        rstbtn = QPushButton("Reset")
        rstbtn.clicked.connect(self.onReset)
        qitbtn = QPushButton("Quit")
        qitbtn.clicked.connect(self.onQuit)
        crebtn = QPushButton("Create Account")
        crebtn.clicked.connect(self.onCreate)
        updbtn = QPushButton("Update Account")
        updbtn.clicked.connect(self.onUpdate)

        loFuid = QFormLayout()
        loFuid.addRow("Userid:", self.leuid)
        loFuid.addRow("Password:", self.leupwd)

        loHbtns = QHBoxLayout()
        loHbtns.addWidget(subbtn)
        loHbtns.addWidget(rstbtn)
        loHbtns.addWidget(qitbtn)

        layoutV = QVBoxLayout()
        layoutV.addWidget(lblhdln)
        layoutV.addWidget(frame)
        layoutV.addLayout(loFuid)
        layoutV.addWidget(QLabel())
        layoutV.addWidget(self.result)
        layoutV.addWidget(QLabel())
        layoutV.addLayout(loHbtns)
        layoutV.addWidget(crebtn)
        layoutV.addWidget(updbtn)

        centralWidget = QWidget()
        centralWidget.setLayout(layoutV)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle(os.path.basename(__file__)[:-3])

    """
    def onHelpUsid(self):
         pass

    def onHelpUpwd(self):
         pass
    """

    def alertMsg(self, msg):
        reply = QMessageBox.warning(self, 'ALERT', msg,
                QMessageBox.Ok | QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            self.onReset()

    def onSubmit(self):
        self.onLogin()

    def onLogin(self):
        rc, msg = lgn.verusr(self.leuid.text(), self.leupwd.text())
        if rc:
            msx = '\nPlease review the format rules and re-enter.'
            self.alertMsg(msg+msx)
            self.result.setText('Please login to access your account.')
        else:
            self.leupwd.setText('')
            self.result.setText('Login successful.')

    def onReset(self):
        self.leuid.setText('')
        self.leupwd.setText('')
        self.result.setText('Please login to access your account.')

    def onQuit(self):
        sys.exit()

    def onCreate(self):
        os.system(f'start "Account" /separate /min python ceapps\gAcctCre.py')
        sys.exit()

    def onUpdate(self):
        os.system(f'start "Account" /separate /min python ceapps\gAcctUpd.py')
        sys.exit()

def main():
    app  = QApplication(sys.argv)
    appmn = AppMain()
    appmn.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()