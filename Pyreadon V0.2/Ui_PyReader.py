# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\QQPCmgr\Desktop\eric\PyReadon\PyReader.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(440, 288)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        MainWindow.setCentralWidget(self.centralWidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMovable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.addbar = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.addbar.setIcon(icon)
        self.addbar.setObjectName("addbar")
        self.setbar = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/upon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setbar.setIcon(icon1)
        self.setbar.setObjectName("setbar")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/layout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action.setIcon(icon2)
        self.action.setObjectName("action")
        self.toolBar.addAction(self.addbar)
        self.toolBar.addAction(self.action)
        self.toolBar.addAction(self.setbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.addbar.setText(_translate("MainWindow", "添加"))
        self.addbar.setToolTip(_translate("MainWindow", "添加文件"))
        self.addbar.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.setbar.setText(_translate("MainWindow", "设置"))
        self.setbar.setToolTip(_translate("MainWindow", "设置"))
        self.action.setText(_translate("MainWindow", "网格布局"))
        self.action.setToolTip(_translate("MainWindow", "网格布局"))

import r1_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

