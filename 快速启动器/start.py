from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QProcess
import os
import subprocess
import sys


from Ui_starter import Ui_MainWindow
from info import Info 
from db import read_db, remove_db, save2db


class Starter(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        # 继承主窗口类
        super(Starter, self).__init__(parent)
        # 不支持全屏
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        # 图标
        self.setWindowIcon(QIcon('source/1.ico'))
        self.setupUi(self)
        self.initUi()
        
    def initUi(self):
        # 工具栏
        self.addbar.triggered.connect(self.open)
        # 初始化按钮
        self.connect_db()

        
    def connect_db(self):
        # 初始化按钮
        for i, starter in enumerate(read_db()):
            button = self.gridLayout.itemAt(i).widget()
            button.fname = starter.fname
            button.name = starter.name
            button.state = starter.state
            button.setText(button.name)
        
    def get_file(self):
        # 打开单个文件
        # _ 返回类型
        fname, _ = QFileDialog.getOpenFileName(self, 'Open files', './', '(*.py)')
        return fname
        
    def open(self):
        fname = self.get_file()
        # 文件名非空
        if fname:
            process = QProcess()
            process.startDetached('python', [fname])
            #subprocess.run(['python', fname], shell=True)
            #qApp.quit()
            
    # 重写关闭事件
    def closeEvent(self, event):
        # 移除数据
        remove_db()
        # 保存每个按钮的信息
        for i in range(self.gridLayout.count()):
            button = self.gridLayout.itemAt(i).widget()    
            save2db(button)
        event.accept()
        
    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    starter = Starter()
    info = Info()
    starter.infobar.triggered.connect(info.show)
    starter.show()
    sys.exit(app.exec_())
