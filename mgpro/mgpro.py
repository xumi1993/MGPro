# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 12:54:06 2018

@author: zxuxmij
"""

import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, \
                    QAction, QMenu, QFileDialog, QGridLayout,QLineEdit, QLabel, \
                    QWidget, QHBoxLayout, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas)
from matplotlib.figure import Figure

class opts():
    def __init__(self):
        self.fname = ''

class MGProUI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        # self.opts = opts()
        self.initUI()     
        
    def initUI(self):  

        impAct = QAction('Import', self)
        impAct.setShortcut('Ctrl+i')
        impAct.triggered.connect(self.importFile)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(impAct)             

        self.filetitle = QLabel('Data file:', self)
        self.filetitle.move(30, 40)
        self.fileEdit = QLineEdit(self)
        self.fileEdit.resize(300, 30)
        self.fileEdit.move(100, 40)
        self.fileEdit.textChanged[str].connect(self.onChanged)
        
        self.figWid = QWidget(self)
        self.figWid.resize(570, 300)
        self.figWid.move(30, 80)
        layout = QVBoxLayout(self.figWid)
        self.figWid.setLayout(layout)
        
        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(static_canvas)
        self.ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self.ax.plot(t, np.tan(t), ".")
        
        '''
        self.ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self.ax.plot(t, np.tan(t), ".")
        '''
        # self.grid.addWidget(static_canvas,2,0)
        # self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('MGPro')    
        self.show()
    
    def importFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open grid dat file', '/home')
        self.opts.fname = fname[0]
        
    def onChanged(self, text):
        self.opts.fname = text
    
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MGProUI()
    sys.exit(app.exec_())