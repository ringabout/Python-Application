import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Ui_Window import Ui_Form



class Info(QWidget, Ui_Form):
    def __init__(self, parent=None):
        # 继承主窗口类
        super(Info, self).__init__(parent)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon('source/book.png'))
        self.setupUi(self)
        self.setFixedSize(self.size())
  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    info = Info()
    info.show()
    sys.exit(app.exec_())  
