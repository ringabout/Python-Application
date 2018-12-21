#import necessary library
import sys
from PyQt5.QtWidgets import QWidget,QGridLayout,QPushButton,QApplication,QTextEdit,QLineEdit,qApp,QMainWindow
from PyQt5.QtGui import QIcon
# pyinstaller's necessary component
# from PyQt5 import sip
# define global varible
ulist = ''
# define Qwidget's class
class calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        # choose frid latout
        grid = QGridLayout()
        self.setLayout(grid)
        # initialize display frame
        self.Line = QLineEdit()
        self.Text = QTextEdit()
        # initialize frame's position
        grid.addWidget(self.Text,0,0,1,4)
        grid.addWidget(self.Line,1,0,1,4)
        # initialize button's names
        names = ['cls','bck','plus','close',
                 '7','8','9','/',
                 '4','5','6','*',
                 '1','2','3','-',
                 '0','.','=','+']
        # initialize button's positions
        postions = [(i,j) for i in range(2,7) for j in range(4)]
        # create buttons
        for name,pos in zip(names,postions):
            if name == '':
                continue
            self.button = QPushButton(name)
            self.button.clicked.connect(self.ButtonAct)
            grid.addWidget(self.button,*pos)


        self.setGeometry(300,300,300,220)
        self.setWindowTitle('calculator')
        self.setWindowIcon(QIcon('2.jpg'))
        self.show()
    # button's response
    def ButtonAct(self):
        global ulist
        sender = self.sender()
        ulist += sender.text()
        if sender.text() == '=':
            value = eval(ulist.replace('=',''))
            if value:
                self.Line.setText(str(value))
            ulist = str(value)
        elif sender.text() == 'close':
            qApp.quit()
        elif sender.text() == 'cls':
            ulist = ''
        elif sender.text() == 'bck':
            ulist = ulist[:-4]
        elif sender.text() == 'plus':
            ulist = ulist[:-4]
        self.Text.setText(ulist)
# execute our application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = calculator()
    sys.exit(app.exec_())
