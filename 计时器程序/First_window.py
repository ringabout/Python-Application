import sys
from time import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton,  QFrame
from PyQt5.QtCore import QTimer
from Ui_timer import Ui_MainWindow
from my_func import convert

class Timer(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # 继承主窗口类
        super(Timer, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        # 初始化设置
        self.init_setting()
        

    def initUI(self):
        # 设定 label 的样式
        self.label.setStyleSheet("QLabel{background:rgb(0, 0, 0);}"
                                 "QLabel{color:rgb(250, 250, 250, 250); font-size:50px; font-weight:bold}")
        self.label.setFrameShadow(QFrame.Raised)
        
        # 创建 QTimer 对象
        # 将 QTimer 实例与 showTime 函数绑定
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        
        # 执行初始化按钮状态
        self.setPushButton()
        
        # 将按钮与对应函数绑定
        self.pushButton.clicked.connect(self.startTimer)
        self.pushButton_2.clicked.connect(self.pauseTimer)
        self.pushButton_3.clicked.connect(self.clearTimer)
    
    def init_setting(self):
        # 初始化设置
        self._start_time = None
        self._pause_flag = False
        self._pause_time = 0
        self._restart_time = 0
        self._pause_total = 0
        self.label.setText("00:00:00")
    
    @property
    def _current_time(self):
        # 返回当前时间
        return time()
        
    def showTime(self):
        # 如果暂停标志为真，self._pause_total 属性要加上暂停时间
        # 并设置暂停标志为假
        if self._pause_flag:
            self._pause_total +=  self._restart_time - self._pause_time
            self._pause_flag = False
        # 计算运行时间
        run_time = self._current_time - self._pause_total - self._start_time
        # 将时间转换为文本
        text = convert(run_time)
        # 标签显示文字
        self.label.setText(text)
        
        
    def startTimer(self):
        # 发出计时信号
        self.timer.start(0)
        # 如果 self._pause_flag 为真，更新开始时间
        # 否则，更新重启时间
        if not self._pause_flag:
            self._start_time = self._current_time
        else:
            self._restart_time = self._current_time
        # 设置按钮属性
        self.setPushButton(btn1=False, btn2=True, btn3=True)

        
    def pauseTimer(self):
        self._pause_flag = True
        self._pause_time =  self._current_time
        # 停止发送信号
        self.timer.stop()
        self.setPushButton(btn1=True, btn2=False, btn3=True)
 
        
    def clearTimer(self):
        # 还原至初始状态
        self.init_setting()
        self.timer.stop()
        self.setPushButton()

        
    def setPushButton(self, *, btn1=True, btn2=False, btn3=False):
        # 设置按钮属性
        self.pushButton.setEnabled(btn1)
        self.pushButton_2.setEnabled(btn2)
        self.pushButton_3.setEnabled(btn3)
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = Timer()
    timer.show()
    sys.exit(app.exec_())
