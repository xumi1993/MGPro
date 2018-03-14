# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 12:54:06 2018

@author: zxuxmij
"""

import sys
import os
import numpy as np
from mgpro.mgmat import mgmat
from PyQt5.QtWidgets import QMainWindow, QApplication, \
                    QAction, QMenu, QFileDialog, QGridLayout,QLineEdit, QLabel, \
                    QWidget, QHBoxLayout, QPushButton, QVBoxLayout,QFrame
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas)
from matplotlib.figure import Figure

class opts():
    def __init__(self):
        self.fname = ''
        self.h = 0
        self.order = 0

class MGProUI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.opts = opts()
        self.mg = None
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
        
        self.draw_raw_data_Button = QPushButton('Draw Data', self)
        self.draw_raw_data_Button.setCheckable(False)
        self.draw_raw_data_Button.move(420, 40)
        self.draw_raw_data_Button.clicked[bool].connect(self.draw_raw_data)
        
        self.proFrame = QFrame(self)
        self.proFrame.setFrameShape(QFrame.StyledPanel)
        self.proFrame.resize(350, 200)
        self.proFrame.move(600, 40)
        grid = QGridLayout(self.proFrame)
        grid.setSpacing(30)
        
        continu_la = QLabel('Continuation:')
        continuEdit = QLineEdit(self)
        self.continuEdit.textChanged[str].connect(self.contiChanged)
        # continuEdit.resize(30, 40)
        
        deriv_la = QLabel('Derivative:')
        derivEdit = QLineEdit(self)
        self.derivEdit.textChanged[str].connect(self.derivChanged)
        
        calButton = QPushButton('Calculate', self)
        drawButton = QPushButton('draw result', self)
        grid.addWidget(continu_la, 0, 0)
        grid.addWidget(continuEdit, 0, 1)
        grid.addWidget(deriv_la, 1, 0)
        grid.addWidget(derivEdit, 1, 1)
        grid.addWidget(calButton, 2, 0)
        grid.addWidget(drawButton, 2, 1)
        
        
        self.figWid = QWidget(self)
        self.figWid.resize(532, 380)
        self.figWid.move(30, 80)
        layoutf = QVBoxLayout(self.figWid)
        self.figWid.setLayout(layoutf)
        self.raw_canvas = FigureCanvas(Figure(figsize=(7, 5)))
        layoutf.addWidget(self.raw_canvas)
        
        self.rstWid = QWidget(self)
        self.rstWid.resize(532, 380)
        self.rstWid.move(30, 460)
        layoutd = QVBoxLayout(self.rstWid)
        self.rstWid.setLayout(layoutd)
        self.pro_canvas = FigureCanvas(Figure(figsize=(7, 5)))
        layoutd.addWidget(self.pro_canvas)
        
        
        '''
        static_ax = self.raw_canvas.figure.subplots()
        t = np.array([[1,2,3,4],[1,2,3,4]])
        static_ax.pcolor(t)
        '''
        
        # self.grid.addWidget(static_canvas,2,0)
        # self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, 1000, 900)
        self.setWindowTitle('MGPro')    
        self.show()
        
    def contiChanged(self, text):
        try:
            self.opts.h = float(text)
        except:
            pass
    
    def derivChanged(self, text):
        try:
            self.opts.order = float(text)
        except:
            pass
    
    def importFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open grid dat file', 
                                            os.path.dirname(__file__))
        self.opts.fname = fname[0]
        self.fileEdit.setText(self.opts.fname)
        self.mg = mgmat(self.opts.fname)
        self.draw_raw_data_Button.setCheckable(True)
        
    def onChanged(self, text):
        self.opts.fname = text
        
    def draw_raw_data(self):
        if isinstance(self.mg, mgmat):
            self.mg.pltmap(self.raw_canvas.figure, self.mg.data)
    
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MGProUI()
    sys.exit(app.exec_())