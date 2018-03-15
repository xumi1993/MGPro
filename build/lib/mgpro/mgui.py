# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 12:54:06 2018

@author: Mijian Xu
"""

import sys
import os
from datetime import datetime
import numpy as np
from mgpro.mgmat import mgmat
from PyQt5.QtWidgets import QMainWindow, QApplication, \
                    QAction, QMenu, QFileDialog, QGridLayout,QLineEdit, QLabel, \
                    QWidget, QHBoxLayout, QPushButton, QVBoxLayout,QFrame, \
                    QTextEdit
from PyQt5.QtGui import QColor
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


redColor = QColor(255, 0, 0)

class opts():
    def __init__(self):
        self.fname = ''
        self.h = 0
        self.order = 0
        self.log = datetime.now().strftime('%Y/%m/%d %H:%M:%S: OK')
        
        
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
        continuEdit.textChanged[str].connect(self.contiChanged)
        # continuEdit.resize(30, 40)
        
        deriv_la = QLabel('Derivative:')
        derivEdit = QLineEdit(self)
        derivEdit.textChanged[str].connect(self.derivChanged)
        
        calButton = QPushButton('Calculate', self)
        calButton.clicked[bool].connect(self.calculation)
        drawButton = QPushButton('draw result', self)
        drawButton.clicked[bool].connect(self.draw_result)
        buttonbox = QWidget(self)
        hbox = QHBoxLayout(buttonbox)
        buttonbox.setLayout(hbox)
        hbox.addWidget(calButton)
        hbox.addWidget(drawButton)

        grid.addWidget(continu_la, 0, 0)
        grid.addWidget(continuEdit, 0, 1)
        grid.addWidget(deriv_la, 1, 0)
        grid.addWidget(derivEdit, 1, 1)
        grid.addWidget(buttonbox, 2, 1)
        # grid.addWidget(calButton, 2, 0)
        # grid.addWidget(drawButton, 2, 1)
        # grid.addLayout(hbox)
        
        self.logEdit = QTextEdit(self)
        self.logEdit.resize(350, 375)
        self.logEdit.move(600, 460)
        self.logEdit.setReadOnly(True)
        self.logEdit.append(self.opts.log)

        self.figWid = QWidget(self)
        self.figWid.resize(532, 380)
        self.figWid.move(30, 80)
        layoutf = QVBoxLayout(self.figWid)
        self.figWid.setLayout(layoutf)
        self.raw_canvas = FigureCanvas(Figure(figsize=(7, 5)))
        layoutf.addWidget(self.raw_canvas)
        # self.toolbar = NavigationToolbar(self.raw_canvas, self)
        # self.toolbar.hide()
        
        self.rstWid = QWidget(self)
        self.rstWid.resize(532, 380)
        self.rstWid.move(30, 460)
        layoutd = QVBoxLayout(self.rstWid)
        self.rstWid.setLayout(layoutd)
        self.pro_canvas = FigureCanvas(Figure(figsize=(7, 5)))
        layoutd.addWidget(self.pro_canvas)
        
        self.colorset = QFrame(self)
        self.colorset.setFrameShape(QFrame.StyledPanel)
        self.colorset.resize(350, 100)
        self.colorset.move(600, 250)
        grid = QGridLayout(self.colorset)
        grid.setSpacing(10)
        
        color1 = QFrame(self)
        color1.setStyleSheet("QWidget {background-color: rgb(62, 225, 95)}")
        color1Edit = QLineEdit(self)
        color2 = QFrame(self)
        color2.setStyleSheet("QWidget {background-color: rgb(255, 225, 95)}")
        color2Edit = QLineEdit(self)
        grid.addWidget(color1, 0, 0)
        grid.addWidget(color1Edit,0,1)
        grid.addWidget(color2, 1, 0)
        grid.addWidget(color2Edit,1,1)
        
        
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
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open grid dat file', 
                                            os.path.dirname(__file__))
            self.writelog('Loading %s' % fname[0])
        except:
            self.writelog('Cannot open file', QColor(255,0,0))    
            return
        self.opts.fname = fname[0]
        self.fileEdit.setText(self.opts.fname)
        try:
            self.mg = mgmat(self.opts.fname)
        except:
            self.writelog('Error format of import file', QColor(255,0,0))
            return
        self.draw_raw_data_Button.setCheckable(True)
        self.writelog('Loading done')
        
    def onChanged(self, text):
        self.opts.fname = text
    
    def calculation(self):
        self.writelog('Calculating: h=%5.2f order=%5.2f' % (self.opts.h, self.opts.order))
        try:
            self.mg.continuation(self.opts.h, self.opts.order)
            self.writelog('Calculation done')
        except Exception as e:
            self.writelog('Error in calculating:\n%s' % e.args[0], QColor=(255,0,0))

    def draw_result(self):
        self.writelog('Drawing result')
        try:
            self.mg.pltmap(self.pro_canvas.figure, self.mg.result)
        except Exception as e:
                self.writelog('Error in mapping:\n%s' % e.args[0], QColor=(255,0,0))   

    def draw_raw_data(self):
        if isinstance(self.mg, mgmat):
            self.writelog('Drawing raw data')
            try:
                self.mg.pltmap(self.raw_canvas.figure, self.mg.data)
            except Exception as e:
                self.writelog('Error in mapping:\n%s' % e.args[0], QColor=(255,0,0))
        else:
            self.writelog('No data load', QColor)
            
    def writelog(self, content, color=QColor(0,0,0)):
        log = datetime.now().strftime('%Y/%m/%d %H:%M:%S')+': '+ content
        self.logEdit.setTextColor(color)
        self.logEdit.append(log)
    
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MGProUI()
    sys.exit(app.exec_())
