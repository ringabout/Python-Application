# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\QQPCmgr\Desktop\eric\快速启动器\starter.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(648, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(160, 90, 331, 321))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_7 = MyButton(self.gridLayoutWidget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_7.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_7.setText("")
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 0, 1, 1, 1)
        self.pushButton_8 = MyButton(self.gridLayoutWidget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_8.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_8.setText("")
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 1, 1, 1, 1)
        self.pushButton_10 = MyButton(self.gridLayoutWidget)
        self.pushButton_10.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_10.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_10.setText("")
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 0, 2, 1, 1)
        self.pushButton_9 = MyButton(self.gridLayoutWidget)
        self.pushButton_9.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_9.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setText("")
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 1, 2, 1, 1)
        self.pushButton_6 = MyButton(self.gridLayoutWidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_6.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_6.setText("")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 1, 0, 1, 1)
        self.pushButton_5 = MyButton(self.gridLayoutWidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_5.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 0, 0, 1, 1)
        self.pushButton_11 = MyButton(self.gridLayoutWidget)
        self.pushButton_11.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_11.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_11.setText("")
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 2, 0, 1, 1)
        self.pushButton_13 = MyButton(self.gridLayoutWidget)
        self.pushButton_13.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_13.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_13.setText("")
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout.addWidget(self.pushButton_13, 2, 1, 1, 1)
        self.pushButton_12 = MyButton(self.gridLayoutWidget)
        self.pushButton_12.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_12.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_12.setText("")
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout.addWidget(self.pushButton_12, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.addbar = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addbar.setIcon(icon)
        self.addbar.setObjectName("addbar")
        self.infobar = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.infobar.setIcon(icon1)
        self.infobar.setObjectName("infobar")
        self.toolBar.addAction(self.addbar)
        self.toolBar.addAction(self.infobar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.addbar.setText(_translate("MainWindow", "添加"))
        self.addbar.setToolTip(_translate("MainWindow", "添加程序"))
        self.infobar.setText(_translate("MainWindow", "信息"))
        self.infobar.setToolTip(_translate("MainWindow", "显示信息"))

from mybutton import MyButton
import r1_rc
import r2_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

