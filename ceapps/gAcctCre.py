# ---------------------------------------------------------------------
# Copyright (c) 2001-2021 CALIMLIM Enterprises. All rights reserved.
#
# Author: Virgilio B Calimlim, 2021/01
# ---------------------------------------------------------------------
# Progname   : gAcctCre.py
# Description: Account creation
# System     : Access Authorization
# Purpose    : Authentication 
# ---------------------------------------------------------------------
# Revisions  :
# 0.0   2021-01-11 virbcal  Initial release;
# ---------------------------------------------------------------------

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QFrame,
                             QLineEdit, QPushButton,
                             QHBoxLayout, QVBoxLayout, QFormLayout,
                             QMessageBox)
from ceutils import lginval as lgn
#from ceutils import ufilefunc as uff
#uff.savelist(dir(self.rbcre),itemized=True,popup=True)

def version():
    # Function: Return version number.
    return os.path.basename(__file__)[:-3]+' 0.0'

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lblhdln = QLabel('<center>Create User Account</center>')
        self.result = QLabel('Please enter the details for your new account.')
        self.step = QLabel('0')

       #lblunam = QLabel('Name')
       #lbluadr = QLabel('Address')
       #lbluphn = QLabel('Phone')
       #lblueml = QLabel('Email')
       #lbluid  = QLabel('Userid')
       #lblupwd = QLabel('Password')
       #self.lblupwn = QLabel('New password')
       #lblupwc = QLabel('Confirm')

       #lblunam.clicked.connect(self.onHelpUnam) 
       #lbluadr.clicked.connect(self.onHelpUadr) 
       #lbluphn.clicked.connect(self.onHelpUphn) 
       #lblueml.clicked.connect(self.onHelpUeml) 
       #lblusid.clicked.connect(self.onHelpUsid) 
       #lblupwd.clicked.connect(self.onHelpUpwd) 

        frame = QFrame()
        frame.setFrameShadow(QFrame.Sunken)
        frame.setFrameShape(QFrame.HLine)

        self.leuid  = QLineEdit()
        self.leupwd = QLineEdit()
        self.leupwc = QLineEdit()
        self.leunam = QLineEdit()
        self.leuadr = QLineEdit()
        self.leuphn = QLineEdit()
        self.leueml = QLineEdit()

        self.leuid.setPlaceholderText('Userid')
        self.leupwd.setPlaceholderText('Password')
        self.leupwd.setEchoMode(QLineEdit.Password)
        self.leupwc.setPlaceholderText('Confirm password')
        self.leupwc.setEchoMode(QLineEdit.Password)
        self.leunam.setPlaceholderText('Lastname, Firstname, MI')
        self.leuadr.setPlaceholderText('Address')
        self.leuphn.setPlaceholderText('Phone')
        self.leueml.setPlaceholderText('Email')

        subbtn = QPushButton("Submit")
        subbtn.clicked.connect(self.onSubmit)

        rstbtn = QPushButton("Reset")
        rstbtn.clicked.connect(self.onReset)

        qitbtn = QPushButton("Quit")
        qitbtn.clicked.connect(self.onQuit)

        lgnbtn = QPushButton("Login")
        lgnbtn.clicked.connect(self.onLogin)

        updbtn = QPushButton("Update Account")
        updbtn.clicked.connect(self.onUpdate)

        self.loFudtl = QFormLayout()
        self.loFudtl.addRow(QLabel("Userid:"), self.leuid)
        self.loFudtl.addRow(QLabel("Password:"), self.leupwd)
        self.loFudtl.addRow(QLabel("Confirm:"), self.leupwc)
        self.loFudtl.addRow(QLabel("Name:"), self.leunam)
        self.loFudtl.addRow(QLabel("Address:"), self.leuadr)
        self.loFudtl.addRow(QLabel("Phone:"), self.leuphn)
        self.loFudtl.addRow(QLabel("Email:"), self.leueml)

        loHbtns = QHBoxLayout()
        loHbtns.addWidget(subbtn)
        loHbtns.addWidget(rstbtn)
        loHbtns.addWidget(qitbtn)

        layoutV = QVBoxLayout()
        layoutV.addWidget(lblhdln)
        layoutV.addWidget(frame)
        layoutV.addLayout(self.loFudtl)
        layoutV.addWidget(QLabel())
        layoutV.addWidget(self.result)
        layoutV.addWidget(QLabel())
        layoutV.addLayout(loHbtns)
        layoutV.addWidget(lgnbtn)
        layoutV.addWidget(updbtn)

        centralWidget = QWidget()
        centralWidget.setLayout(layoutV)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle(os.path.basename(__file__)[1:-3])

    """
    def onHelpUnam(self):
         pass

    def onHelpUadr(self):
         pass

    def onHelpUphn(self):
         pass

    def onHelpUeml(self):
         pass

    def onHelpUsid(self):
         pass

    def onHelpUpwd(self):
         pass
    """

    def alertMsg(self, msg):
        reply = QMessageBox.warning(self, 'ALERT', msg,
                QMessageBox.Ok | QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            self.startCreate()

    def onSubmit(self):
        self.onCreate()
            
    def onCreate(self):
        rc, msg = lgn.addusr(self.leuid.text(), self.leupwd.text(),
                             self.leupwc.text(),
                             self.leunam.text(), self.leuadr.text(),
                             self.leuphn.text(), self.leueml.text())
        if rc:
            msx = "\nPlease review the format rules and re-enter."
            self.alertMsg(msg+msx)
        else:
            self.result.setText('Account successfully created.\nYou may now proceed to login.')
            self.leupwd.setText('')
            self.leupwc.setText('')

    def onReset(self):
        self.startCreate()

    def onQuit(self):
        sys.exit()

    def startCreate(self):
        os.system(f'start "Create" /separate /min python ceapps\gAcctCre.py')
        sys.exit()

    def onLogin(self):
        os.system(f'start "Login" /separate /min python ceapps\gAcctLgn.py')
        sys.exit()

    def onUpdate(self):
        os.system(f'start "Update" /separate /min python ceapps\gAcctUpd.py')
        sys.exit()

def main():
    app  = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()