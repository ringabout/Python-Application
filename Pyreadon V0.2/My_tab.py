from PyQt5.QtCore import QTabBar


class MyTabBar(QTabBar):
    
    #自定义tabbar,实现双击关闭
    def __init__(self,parent = None):
        QTabBar.__init__(self,parent)
        
    def mouseDoubleClickEvent(self, event):
        
        #获取点击的tab
        tabId = self.tabAt(event.pos())
        #发送关闭信号和tabid
        self.emit(SIGNAL("tabCloseRequested(int)"),self.tabAt(event.pos()))
        

