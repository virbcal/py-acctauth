# https://stackoverflow.com/questions/54486508/populating-pyqt5-inputs-from-dictionary-selection

import sys
import os
import cedat
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QFrame,
                             QComboBox, QPushButton, QHBoxLayout, QVBoxLayout)

#from ceutils import ufilefunc as uff
#uff.savelist(dir(main.dev._widget),itemized=True,popup=True)

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        labl = QLabel('<center>Development, Utililities and Games Menu</center>')

        frame = QFrame()
        frame.setFrameShadow(QFrame.Sunken)
        frame.setFrameShape(QFrame.HLine)

        self.cmbbx1 = self.setComboBox(cedat.devdct)
        self.cmbbx2 = self.setComboBox(cedat.utidct)
        self.cmbbx3 = self.setComboBox(cedat.gamdct)

        selbtn = QPushButton("Select")
        selbtn.clicked.connect(self.onSelect)

        rstbtn = QPushButton("Reset")
        rstbtn.clicked.connect(self.onReset)

        qitbtn = QPushButton("Quit")
        qitbtn.clicked.connect(self.onQuit)

        layoutV = QVBoxLayout()
        layoutV.addWidget(labl)
        layoutV.addWidget(frame)
        layoutV.addWidget(self.cmbbx1)
        layoutV.addWidget(self.cmbbx2)
        layoutV.addWidget(self.cmbbx3)
        layoutV.addWidget(selbtn)
        layoutV.addWidget(rstbtn)
        layoutV.addWidget(qitbtn)

        centralWidget = QWidget()
        centralWidget.setLayout(layoutV)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle('Apps Menu')

    def setComboBox(self, cList):
        self.comboBox = QComboBox()
        self.comboBox.clear()
        for k, v in cList.items():
            self.comboBox.addItem(k, v)
        return self.comboBox

    def onSelect(self):
        nam, sel = self.get_selections(self.cmbbx1)
        if not sel:
            nam, sel = self.get_selections(self.cmbbx2)
            if not sel:
                nam, sel = self.get_selections(self.cmbbx3)
        if sel:
            os.system(f'start "{nam}" /separate /min {sel}')

    def get_selections(self, name):
        '''
        Returns the selected items in widget *name*.
        Raises TypeError if the widget does not support selection.
        '''
       #widget = self.widgets[name]
        widget = name

        if hasattr(widget, 'selectedItems'):
            return map(lambda x: x.text(), widget.selectedItems())

        elif hasattr(widget, 'selectedText'):
            return widget.selectedText()

        elif hasattr(widget, 'currentText') and hasattr(widget, 'currentData'):
            return widget.currentText(), widget.currentData()

        elif hasattr(widget, 'currentText'):
            return widget.currentText()

        else:
            raise TypeError('Widget %s has no selection methods' % widget)

    def onReset(self):
        self.cmbbx1.setCurrentIndex(0)
        self.cmbbx2.setCurrentIndex(0)
        self.cmbbx3.setCurrentIndex(0)

    def onQuit(self):
        sys.exit()

def main():
    app  = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()