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
        self.draw_raw_data_Button.move(420, 40)
        self.draw_raw_data_Button.clicked[bool].connect(self.draw_raw_data)
        
        self.figWid = QWidget(self)
        self.figWid.resize(570, 300)
        self.figWid.move(30, 80)
        layout = QVBoxLayout(self.figWid)
        self.figWid.setLayout(layout)
        
        self.raw_canvas = FigureCanvas(Figure(figsize=(5, 5)))
        layout.addWidget(self.raw_canvas)
        '''
        static_ax = self.raw_canvas.figure.subplots()
        t = np.array([[1,2,3,4],[1,2,3,4]])
        static_ax.pcolor(t)
        '''
        
        # self.grid.addWidget(static_canvas,2,0)
        # self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, 1000, 800)
        self.setWindowTitle('MGPro')    
        self.show()
    
    def importFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open grid dat file', 
                                            os.path.expanduser('~'))
        self.opts.fname = fname[0]
        self.fileEdit.setText(self.opts.fname)
        self.mg = mgmat(self.opts.fname)
        
    def onChanged(self, text):
        self.opts.fname = text
        
    def draw_raw_data(self):
        if isinstance(self.mg, mgmat):
            ax_raw = self.raw_canvas.figure.subplots()
            pcm = ax_raw.pcolor(self.mg.data, 
                         cmap='jet') 
                         #norm=JetNormalize(midpoint=breakpoint))
            ax_raw.figure.canvas.draw()
            self.raw_canvas.figure.colorbar(pcm, extend='both')
            self.raw_canvas.figure.canvas.draw()
            #self.mg.pltmap(self.raw_canvas.figure)
    
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MGProUI()
    sys.exit(app.exec_())