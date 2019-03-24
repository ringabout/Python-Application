import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, \
        QApplication, QPushButton, QFrame, QAction, QFileDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QMenu, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt
from Ui_PyReader import Ui_MainWindow
import fitz



class Reader(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # 继承主窗口类
        super(Reader, self).__init__(parent)
        # 设置应用图标
        self.setWindowIcon(QIcon('source/book.png'))
        # 获取屏幕对象
        self.screen = QDesktopWidget().screenGeometry()
        self.setupUi(self)
        # 仅支持最小化以及关闭按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        # 去掉 toolbar 右键菜单
        self.setContextMenuPolicy(Qt.NoContextMenu)
        # 固定界面大小，不可修改
        self.setFixedSize(self.screen.width(), self.screen.height())
        # 获取 QTableWidget 实例 
        self.table = QTableWidget()  
        # 将 self.table 设置为中心 widget
        self.setCentralWidget(self.table)
        # 初始化
        self.initUi()

    def initUi(self):
        # 连接
        self._init_bookset()
        self.x = 0
        self.y = 0
        # 初始化表格类型
        self._setTableStyle()
        # 将 toolbar + 号与 self.open 函数绑定
        self.addbar.triggered.connect(self.open)
        
    # 连接数据库
    def _init_bookset(self):
        self.booklist = []
    
    # 获取无重复图书的地址
    def filter_book(self, fname):
        if not fname:
            return False
        if fname not in self.booklist:
            self.booklist.append(fname)
            return True
        return False
 
    def getfile(self):
        # 打开单个文件
        fname, _ = QFileDialog.getOpenFileName(self, 'Open files', './', '(*.pdf)')
        return fname
        
    def open(self):
        # 打开文件
        fname = self.getfile()
        if self.filter_book(fname):
            self.setIcon(fname)
        
    def _setTableStyle(self):
        # 开启水平与垂直滚轴
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # 设置 5 行 8 列 的表格
        self.table.setColumnCount(8)
        self.table.setRowCount(5)
        # 设置标准宽度
        self.width = self.screen.width()// 8
        # 设置单元格的宽度
        for i in range(8):
            self.table.setColumnWidth(i, self.width)
        # 设置单元格的高度
        # 设置纵横比为 4 : 3
        for i in range(5):
            self.table.setRowHeight(i, self.width * 4 // 3)
        # 隐藏标题栏
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        # 禁止编辑
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 不显示网格线
        self.table.setShowGrid(False)
        # 将单元格绑定右键菜单
        # 点击单元格，调用 self.generateMenu 函数
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.generateMenu)


    def setIcon(self, fname):
        # 打开 PDF
        doc = fitz.open(fname)
        # 加载封面
        page = doc.loadPage(0)
        # 生成封面图像
        cover = render_pdf_page(page, True)
        label = QLabel(self)
        # 设置图片自动填充 label
        label.setScaledContents (True)
        # 设置封面图片
        label.setPixmap(QPixmap(cover))
        # 设置单元格元素为 label
        self.table.setCellWidget(self.x, self.y, label)
        # 删除 label 对象，防止后期无法即时刷新界面
        # 因为 label 的生存周期未结束
        del label
        # 设置当前行数与列数
        self.crow, self.ccol = self.x, self.y
        # 每 8 个元素换行
        if (not self.y % 7) and (self.y):
            self.x += 1
            self.y = 0
        else:
            self.y += 1

        

    def generateMenu(self, pos):
        row_num = col_num = -1
        # 获取选中的单元格的行数以及列数
        for i in self.table.selectionModel().selection().indexes():
            row_num = i.row()
            col_num = i.column()
        # 若选取的单元格中有元素，则支持右键菜单
        if (row_num < self.crow) or (row_num == self.crow and col_num <= self.ccol):
            menu = QMenu()
            item1 = menu.addAction('开始阅读')
            item2 = menu.addAction('删除图书')
            # 获取选项
            action = menu.exec_(self.table.mapToGlobal(pos))
            if action == item1:
                pass
            elif action == item2:
                self.delete_book(row_num, col_num)
              
      
    # 删除图书
    def delete_book(self, row, col):
        # 获取图书在列表中的位置
        index = row * 8 + col
        self.x = row
        self.y = col
        if index >= 0:
            self.booklist.pop(index)

        i, j = row, col
        while 1:
            # 移除 i 行 j 列单元格的元素
            self.table.removeCellWidget(i, j)
            # 一直删到最后一个有元素的单元格
            if i == self.crow and j == self.ccol:
                break
            if (not j % 7) and j:
                i += 1
                j = 0
            else:
                j += 1
  
        # 如果 booklist 为空，设置当前单元格为 -1
        if not self.booklist:
            self.crow = -1
            self.ccol = -1
        # 删除图书后，重新按顺序显示封面图片
        for fname in self.booklist[index:]:
            self.setIcon(fname)
 

# 显示 PDF 封面
def render_pdf_page(page_data, for_cover=False):
    # 图像缩放比例
    zoom_matrix = fitz.Matrix(4, 4)
    if for_cover:
        zoom_matrix = fitz.Matrix(1, 1)
    
    # 获取封面对应的 Pixmap 对象
    # alpha 设置背景为白色
    pagePixmap = page_data.getPixmap(
        matrix = zoom_matrix, 
        alpha=False) 
    # 获取 image 格式
    imageFormat = QtGui.QImage.Format_RGB888 
    # 生成 QImage 对象
    pageQImage = QtGui.QImage(
        pagePixmap.samples,
        pagePixmap.width, 
        pagePixmap.height, 
        pagePixmap.stride,
        imageFormat)

    # 生成 pixmap 对象
    pixmap = QtGui.QPixmap()
    pixmap.convertFromImage(pageQImage)
    return pixmap

        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = Reader()
    reader.show()
    sys.exit(app.exec_())
