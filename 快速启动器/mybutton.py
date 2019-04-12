from PyQt5.QtWidgets import QPushButton, QAction, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QFont

class MyButton(QPushButton):
    def __init__(self, parent=None):
        super(MyButton, self).__init__(parent)
        self.state = None
        self.fname = None
        self.name = None
        # 设置字体
        font = QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.setFont(font)
        # 支持右键菜单
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.initUi()
        
    def initUi(self):
        # 右键菜单工具栏
        addAction = QAction('添加', self)
        addAction.triggered.connect(self.add)
        delAction = QAction('删除', self)
        delAction.triggered.connect(self.delete)
        self.addAction(addAction)
        self.addAction(delAction)
        self.clicked.connect(self.run)
        
        
    def delete(self):
        if self.state:
            self.state = False
            self.name = None
            self.fname = None
            self.setText(None)
        
        
    def get_file(self):
        # 打开单个文件
        # _ 返回类型
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open files', './', '(*.py)')
 
        
    def add(self):
        # 工具栏功能
        if not self.state:
            self.get_file()
            if self.fname:
                self.name, ok = QInputDialog.getText(self, '文件', '应用名称')
                if ok and self.name:
                    self.state = True
                    self.setText(self.name)
                else:
                    self.fname = None
                    
        

        
    def run(self):
        # 执行程序
        if self.state:
            process = QProcess()
            process.startDetached('python', [self.fname])
            
    

