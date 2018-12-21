import sys
from PyQt5.QtWidgets import QWidget,QMenu,QGridLayout,QPushButton,QApplication,QTextEdit,QLineEdit,qApp,QMainWindow
from PyQt5.QtGui import QIcon
import copy
import math
import re

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
        grid.addWidget(self.Text,0,0,1,5)
        grid.addWidget(self.Line,1,0,1,5)
        # initialize button's names
        names = ['!','^','√','π','cls',
                 'sin','(',')','e','bck',
                 'cos','7','8','9','/',
                 'tan','4','5','6','*',
                 'ln','1','2','3','-',
                 'lg','0','.','=','+']
        # initialize button's positions
        postions = [(i,j) for i in range(2,8) for j in range(5)]
        # create buttons
        for name,pos in zip(names,postions):
            if name == '':
                continue
            self.button = QPushButton(name)
            self.button.clicked.connect(self.ButtonAct)
            grid.addWidget(self.button,*pos)


        self.setGeometry(400,200,300,220)
        self.resize(400,400)
        self.setWindowTitle('calculator')
        self.setWindowIcon(QIcon('2.jpg'))
        self.show()
    # button's response
    def ButtonAct(self):
        global ulist
        sender = self.sender()
        ulist += sender.text()
        if sender.text() == '=':
            temp = ulist.replace('=','')
            try:
                value = eval(temp)
                self.Line.setText(str(value))
                ulist = str(value)
            except:
                ulist = temp

        elif sender.text() == 'cls':
            ulist = ''
        elif sender.text() == 'bck':
            ulist = ulist[:-4]
        elif sender.text() == '^':
            ulist = ulist[:-1]
            ulist += '**'
        elif sender.text() == 'π':
            ulist = ulist[:-1]
            ulist += 'math.pi'
        elif sender.text() == '√':
            ulist = ulist[:-1]
            ulist += 'math.sqrt'
        elif sender.text() == 'sin':
            ulist = ulist[:-3]
            ulist += 'math.sin'
        elif sender.text() == 'cos':
            ulist = ulist[:-3]
            ulist += 'math.cos'
        elif sender.text() == 'tan':
            ulist = ulist[:-3]
            ulist += 'math.tan'
        elif sender.text() == 'ln':
            ulist = ulist[:-2]
            ulist += 'math.log'
        elif sender.text() == 'lg':
            ulist = ulist[:-2]
            ulist += 'math.log10'
        elif sender.text() == 'e':
            ulist = ulist[:-1]
            ulist += 'math.e'
        elif sender.text() == '!':
            oldstr =  re.findall(r'\d*!', ulist)[0]
            newstr = 'factorial(' + re.findall(r'(\d*)!', ulist)[0] + ')'
            ulist = ulist.replace(oldstr,newstr)

        display = self.setResult(ulist)
        self.Text.setText(display)
    def setResult(self,u):
        u = u.replace('math.pi','π')
        u = u.replace('math.sqrt','√')
        u = u.replace('math.sin', 'sin')
        u = u.replace('math.cos', 'cos')
        u = u.replace('math.tan', 'tan')
        u = u.replace('math.log', 'ln')
        u = u.replace('math.log10', 'lg')
        u = u.replace('math.e', 'e')
        u = u.replace('**','^')
        if 'factorial' in u:
            old_str = re.findall('factorial\(\d*\)',u)[0]
            new_str = re.findall('factorial\((\d*)\)',u)[0] + '!'
            print(u)
            u = u.replace(old_str, new_str)
        return u
def factorial(n):
    int_n = int(n)
    if int_n>1:
        return int_n*factorial(int_n-1)
    else:
        return 1
# execute our application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = calculator()
    sys.exit(app.exec_())
