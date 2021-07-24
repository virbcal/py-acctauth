# ---------------------------------------------------------------------
# Copyright (c) 2001-2021 CALIMLIM Enterprises. All rights reserved.
#
# Author: Virgilio B Calimlim, 2021/01
# ---------------------------------------------------------------------
# Progname   : gAcctUpd.py
# Description: Account update
# System     : Access Authorization
# Purpose    : Authentication 
# ---------------------------------------------------------------------
# Revisions  :
# 0.0   2021-01-16 virbcal  Initial release;
# ---------------------------------------------------------------------

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QFrame,
                             QLineEdit, QPushButton, QCheckBox,
                             QHBoxLayout, QVBoxLayout, QFormLayout,
                             QMessageBox)
from ceutils import lginval as lgn, ufilefunc as uff
#uff.savelist(dir(self.rbcre),itemized=True,popup=True)

def version():
    # Function: Return version number.
    return os.path.basename(__file__)[:-3]+' 0.0'


class FormLO(QWidget):
    def __init__(self):
        super().__init__()

    def bldUid(self):
        self.leuid  = QLineEdit()
        self.leupwd = QLineEdit()

        self.leuid.setPlaceholderText('Userid')
        self.leupwd.setPlaceholderText('Password')
        self.leupwd.setEchoMode(QLineEdit.Password)

        self.loFuid = QFormLayout()
        self.loFuid.addRow("Userid:", self.leuid)
        self.loFuid.addRow("Password:", self.leupwd)
        self.setFixedSize(self.loFuid.sizeHint())

    def bldDtl(self):
        self.leunam = QLineEdit()
        self.leuadr = QLineEdit()
        self.leuphn = QLineEdit()
        self.leueml = QLineEdit()
        self.leupwn = QLineEdit()
        self.leupwc = QLineEdit()

        self.leunam.setPlaceholderText('Lastname, Firstname, MI')
        self.leuadr.setPlaceholderText('Address')
        self.leuphn.setPlaceholderText('Phone')
        self.leueml.setPlaceholderText('Email')
        self.leupwn.setPlaceholderText('New password')
        self.leupwn.setEchoMode(QLineEdit.Password)
        self.leupwc.setPlaceholderText('Confirm new password')
        self.leupwc.setEchoMode(QLineEdit.Password)

        self.loFudtl = QFormLayout()
        self.loFudtl.addRow("Name:", self.leunam)
        self.loFudtl.addRow("Address:", self.leuadr)
        self.loFudtl.addRow("Phone:", self.leuphn)
        self.loFudtl.addRow("Email:", self.leueml)
        self.loFudtl.addRow("New password:", self.leupwn)
        self.loFudtl.addRow("Confirm:", self.leupwc)
        self.cbdelt = QCheckBox('',self)
        self.loFudtl.addRow("Delete account", self.cbdelt)
        self.setFixedSize(self.loFudtl.sizeHint())


class AppMain(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(AppMain, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        lblhdln = QLabel('<center>Update User Account</center>')
        self.result = QLabel('Please login to access your account.')
        self.step = '0'
        self.prms = ''
        self.uid = ''

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

        self.flo = FormLO()
        self.flo.bldUid()

        subbtn = QPushButton("Submit")
        subbtn.clicked.connect(self.onSubmit)
        rstbtn = QPushButton("Reset")
        rstbtn.clicked.connect(self.onReset)
        qitbtn = QPushButton("Quit")
        qitbtn.clicked.connect(self.onQuit)
        lgnbtn = QPushButton("Login")
        lgnbtn.clicked.connect(self.onLogin)
        crebtn = QPushButton("Create Account")
        crebtn.clicked.connect(self.onCreate)

        loHbtns = QHBoxLayout()
        loHbtns.addWidget(subbtn)
        loHbtns.addWidget(rstbtn)
        loHbtns.addWidget(qitbtn)

        self.layoutV = QVBoxLayout()
        self.layoutV.addWidget(lblhdln)
        self.layoutV.addWidget(frame)
        self.layoutV.addLayout(self.flo.loFuid)
        self.layoutV.addWidget(QLabel())
        self.layoutV.addWidget(self.result)
        self.layoutV.addWidget(QLabel())
        self.layoutV.addLayout(loHbtns)
        self.layoutV.addWidget(lgnbtn)
        self.layoutV.addWidget(crebtn)

        centralWidget = QWidget()
        centralWidget.setLayout(self.layoutV)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle(os.path.basename(__file__)[1:-3])

        if len(sys.argv) > 1:
            keys = ['stp', 'uid', 'pwd']
            rc, msg = uff.parsSysargv(sys.argv, keys)
            if rc:
                self.alertMsg(msg)
            else:
                self.step = msg[0].strip("[]',\"")              # stp
                self.flo.leuid.setText(msg[1].strip("[]',\""))  # uid
                self.flo.leupwd.setText(msg[2].strip("[]',\"")) # pwd
                self.onSubmit()
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
            self.startUpdate()

    def onSubmit(self):
        self.onUpdate()
            
    def onUpdate(self):
        flo = self.flo
        if '0' in self.step:
            rc, msg = lgn.getdtls(flo.leuid.text(), flo.leupwd.text())
            if rc:
                msx = '\nPlease review the format rules and re-enter.'
                self.alertMsg(msg+msx)
                self.startUpdate()
            else:
                if self.step == '0d':
                    self.restart()
                flo.bldDtl()
                flo.loFuid.addRow(flo.loFudtl)
                flo.leunam.setText(msg[1])
                flo.leuadr.setText(msg[2])
                flo.leuphn.setText(msg[3])
                flo.leueml.setText(msg[4])
                self.result.setText('Please make your updates then re-submit.')
                self.uid = flo.leuid.text()
                self.step = '1'
        elif self.step != '0':
            if self.uid != flo.leuid.text():
                self.restart()
            if flo.cbdelt.isChecked():
                rmv = True
                self.alertMsg("Delete this account?")
            else:
                rmv = False
            rc, msg = lgn.upddtls(flo.leuid.text() , flo.leupwd.text(),
                                  flo.leunam.text(), flo.leuadr.text(),
                                  flo.leuphn.text(), flo.leueml.text(),
                                  flo.leupwn.text(), flo.leupwc.text(), rmv)
            if rc > 1:
                msx = '\nPlease review the format rules and re-enter.'
                self.alertMsg(msg+msx)
            elif rc == 1:
                msx = '\nPlease make your updates then re-submit.'
                self.result.setText(msg+msx)
            elif rmv:
                flo.leupwd.setText('')
                flo.loFuid.removeRow(flo.loFudtl)
               #print(f"loF_rowcount={self.loFuid.rowCount()}")
               #print(f"loF_gdtcount={self.loFuid.count()}")
                self.result.setText('Account successfully deleted.')
                self.setFixedSize(flo.loFuid.sizeHint())
                self.setFixedSize(self.layoutV.sizeHint())
                self.step = '0d'
            else:
                flo.leupwn.setText('')
                flo.leupwc.setText('')
                self.result.setText('Account successfully updated.')
                self.step = '2'

    def rmvRow(self,widget):
        for i in range(self.loFudtl.count()-1,0,-1): 
            self.loFudtl.itemAt(i).widget().setParent(None)
       #for i in range(self.loFudtl.rowCount(),2,-1):
       #    self.loFudtl.takeRow(i)

       # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt/13103617
       #for i in reversed(range(layout.count())): 
       #    layout.itemAt(i).widget().setParent(None)

       #self.loFudtl.takeRow(widget)
       #self.trr = self.loFudtl.takeRow(widget)
        """
        label = self.loFudtl.labelForField(widget)
        if label is not None:
            label.deleteLater()
        widget.deleteLater()
        """

    def onReset(self):
        self.startUpdate()

    def onQuit(self):
        sys.exit()

    def restart(self):
        self.prms = ['0', self.flo.leuid.text(), self.flo.leupwd.text()]
        self.startUpdate()

    def startUpdate(self):
        base = os.path.basename(__file__)
        os.system(f'start "Update" /separate /min python ceapps\{base} {self.prms}')
        sys.exit()

    def onLogin(self):
        os.system(f'start "Login" /separate /min python ceapps\gAcctLgn.py')
        sys.exit()

    def onCreate(self):
        os.system(f'start "Create" /separate /min python ceapps\gAcctCre.py')
        sys.exit()

def main():
    app  = QApplication(sys.argv)
    appmn = AppMain()
    appmn.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()