import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTabWidget, QWidget, QVBoxLayout, QScrollArea, \
    QApplication, QPushButton, QFrame, QAction, QFileDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QMenu, \
    QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt
from Ui_PyReader import Ui_MainWindow

from Area import MyArea
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
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        # 去掉 toolbar 右键菜单
        self.setContextMenuPolicy(Qt.NoContextMenu)
        # 固定界面大小，不可修改
        self.setFixedSize(self.screen.width(), self.screen.height() - 75)
        # 获取 QTableWidget 实例
        self.table = QTableWidget()
        # 将 self.table 设置为中心 widget
        # self.setCentralWidget(self.table)
        # 初始化选项卡
        self.tabwidget = QTabWidget()
        # 添加书库选项卡
        self.tabwidget.addTab(self.table, '书库')
        self.setCentralWidget(self.tabwidget)
        # 设置选项卡可以关闭
        self.tabwidget.setTabsClosable(True)
        # 点击选项卡叉号时，执行 removeTabab 操作
        self.tabwidget.tabCloseRequested[int].connect(self.remove_tab)
        self.initUi()

    def initUi(self):
        # 连接
        self._init_bookset()
        self.x = 0
        self.y = 0
        # 初始化
        self.crow = self.ccol = -1
        # 初始化表格类型
        self._set_table_style()
        # 将 toolbar + 号与 self.open 函数绑定
        self.addbar.triggered.connect(self.open)

    # 连接数据库
    def _init_bookset(self):
        self.booklist = []
        self.read_list = [None]
        # 需要改进，只允许打开一本书
        # 列表
        self.current_page = 0
        self.size = (2.6, 2.6)

    # 获取无重复图书的地址
    def filter_book(self, fname):
        if not fname:
            return False
        if fname not in self.booklist:
            self.booklist.append(fname)
            return True
        return False

    def get_file(self):
        # 打开单个文件
        fname, _ = QFileDialog.getOpenFileName(self, 'Open files', './', '(*.pdf)')
        return fname

    def open(self):
        # 打开文件
        fname = self.get_file()
        if self.filter_book(fname):
            self.set_icon(fname)

    def _set_table_style(self):
        # 开启水平与垂直滚轴
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # 设置 5 行 8 列 的表格
        self.table.setColumnCount(8)
        self.table.setRowCount(5)
        # 设置标准宽度
        self.width = self.screen.width() // 8
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
        self.table.customContextMenuRequested.connect(self.generate_menu)

    def set_icon(self, fname):
        # 打开 PDF
        doc = fitz.open(fname)
        # 加载封面
        page = doc.loadPage(0)
        # 生成封面图像
        cover = render_pdf_page(page)
        label = QLabel(self)
        label.resize(self.width, self.width * 4 // 3)
        # 设置图片自动填充 label
        label.setScaledContents(True)
        # 设置封面图片
        p = QPixmap(cover)
        p.scaled(self.width, self.width * 4 // 3, Qt.KeepAspectRatio)
        label.setPixmap(p)
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

    def generate_menu(self, pos):
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
                index = row_num * 8 + col_num
                fname = self.booklist[index]
                if fname not in self.read_list and len(self.read_list) < 2:
                    self.read_list.append(fname)
                    self.read_book(fname)
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
            self.set_icon(fname)

    def read_book(self, fname):
        # self.close()
        # 内存有可能泄露
        self.doc = fitz.open(fname)
        # metadata = doc.metadata
        title = fname.split('/' or '\\')[-1].replace('.pdf', '')

        vbox = self.book_area(self.doc.loadPage(0))
        self.book_add_tab(title, vbox)

    def book_add_tab(self, title, vbox):
        tab = QWidget()
        tab.setLayout(vbox)
        # tab 为页面，title 为标签名称
        self.tabwidget.addTab(tab, title)

    def page_pixmap(self, page):
        # 在标签上显示图片
        label = QLabel(self)
        p = render_pdf_page(page, size=self.size)
        # 按屏幕大小缩放标签
        p.scaled(self.screen.width(), self.screen.height())
        # 在标签上设置图片
        label.setPixmap(QPixmap(p))
        return label

    def book_area(self, page):
        label = self.page_pixmap(page)
        # area = QScrollArea()
        area = MyArea(self)
        area.init(self)
        area.setWidget(label)

        vbox = QVBoxLayout()
        vbox.addWidget(area)
        return vbox

    def set_current_page(self, right):
        if right and self.current_page < self.doc.pageCount - 1:
            self.current_page += 1

        elif not right and self.current_page > 0:
            self.current_page -= 1

    def switch_page(self, right=True):
        self.set_current_page(right)
        self.set_page()

    def set_page(self):
        page = self.doc.loadPage(self.current_page)
        tab = self.tabwidget.currentWidget()
        layout = tab.layout()
        widget = layout.itemAt(0).widget()
        label = self.page_pixmap(page)
        widget.setWidget(label)

        # self.setCurrentPage(right)
        # vbox = self.bookarea(self.doc.loadPage(self.current_page))
        # tab.setLayout(vbox)

    def zoom_book(self, plus=True):
        a, b = self.size
        if plus:
            a += 0.4
            b += 0.4
            self.size = (a, b)
            self.set_page()
        elif not plus and a > 0:
            if a >= 1:
                a -= 0.4
                b -= 0.4
            self.size = (a, b)
            self.set_page()

    def remove_tab(self, index):
        if index:
            # 当前页数
            self.current_page = 0
            self.tabwidget.removeTab(index)
            # 正在阅读的书
            self.read_list.pop(index)


# 显示 PDF 封面
def render_pdf_page(page_data, *, size=(1, 1)):
    # 图像缩放比例
    # zoom_matrix = fitz.Matrix(4, 4)
    # if for_cover:
    a, b = size
    zoom_matrix = fitz.Matrix(a, b)

    # 获取封面对应的 Pixmap 对象
    # alpha 设置背景为白色
    pagePixmap = page_data.getPixmap(
        matrix=zoom_matrix,
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
