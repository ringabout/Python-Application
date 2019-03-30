from PyQt5.QtWidgets import QScrollArea, QShortcut
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

class MyArea(QScrollArea):
    def init(self, widget):
        self.widget = widget
        self.init_action()
        
    def init_action(self):
        zoom_minus = QShortcut(QKeySequence("Ctrl+-"), self)
        zoom_minus.activated.connect(self.minus)       
        zoom_plus = QShortcut(QKeySequence("Ctrl+="), self)
        zoom_plus.activated.connect(self.plus) 
        
        switch_left = QShortcut(QKeySequence(Qt.Key_Left), self)
        switch_left.activated.connect(self.left)       
        switch_right = QShortcut(QKeySequence(Qt.Key_Right), self)
        switch_right.activated.connect(self.right) 
        
        
        '''
        a1 = QAction(self)
        a1.setShortcut('Ctrl++')
        self.addAction(a1)
        a1.triggered.connect(self.plus)
        
        a2 = QAction(self)
        a2.setShortcut('Ctrl+-')
        self.addAction(a2)
        a2.triggered.connect(self.minus)
        '''
     
    def plus(self):
        self.widget.zoom_book(plus=True)
        
    def minus(self):
        self.widget.zoom_book(plus=False)
        
    def right(self):
        self.widget.switch_page(right=True)
        
    def left(self):
        self.widget.switch_page(right=False)
        
        
        
    #def keyPressEvent(self, event):
        #这里event.key（）显示的是按键的编码
        #print("按下：" + str(event.key()))
        # 举例，这里Qt.Key_A注意虽然字母大写，但按键事件对大小写不敏感
        #if (event.key() == Qt.Key_Left):
        #    self.widget.switch_page(right=False)
        #elif (event.key() == Qt.Key_Right):
        #    self.widget.switch_page(right=True)
        #elif (event.modifiers() == Qt.CTRL and event.key() == Qt.Key_Plus):
        #    self.widget.zoom_book(plus=True)
        #elif (event.modifiers() == Qt.CTRL and event.key() == Qt.Key_Minus):
        #    self.widget.zoom_book(plus=False)
        
 

    
