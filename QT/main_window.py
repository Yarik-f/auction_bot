from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import functools, datetime

import ИсторияТоргов, УдалениеТовара, user_admin_window, products_window, editMW
from DataBase.database import db


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, root=True):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1350, 930)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setIconSize(QtCore.QSize(50, 50))
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks | QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(26, 22, 371, 41))
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 130, 210, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(450, 130, 265, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(900, 130, 180, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1190, 0, 71, 41))
        self.label_2.setObjectName("label_2")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(1150, 80, 135, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(1160, 130, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1190, 50, 71, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(360, 180, 491, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(16)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_4.setObjectName("label_4")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(100, 220, 1100, 250))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.tableWidget.setFont(font)
        self.tableWidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tableWidget.setToolTipDuration(-1)
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setAutoScrollMargin(16)
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.AnyKeyPressed | QtWidgets.QAbstractItemView.DoubleClicked | QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tableWidget.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(280, 540, 761, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(16)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_5.setObjectName("label_5")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(500, 480, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(800, 480, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_8")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(90, 580, 1131, 221))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(6, item)
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(800, 850, 220, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setToolTip("")
        self.pushButton_10.setInputMethodHints(QtCore.Qt.ImhNone)
        self.pushButton_10.setObjectName("pushButton_11")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(500, 850, 220, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_11.setFont(font)
        self.pushButton_11.setToolTip("")
        self.pushButton_11.setInputMethodHints(QtCore.Qt.ImhNone)
        self.pushButton_11.setObjectName("pushButton_11")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1323, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.tableWidget.itemSelectionChanged.connect(self.EditingBlock)
        self.tableWidget_2.itemSelectionChanged.connect(self.EditingBlock_2)
        

        self.r = []
        self.pushButton_3.clicked.connect(functools.partial(self.ИТ))
        self.pushButton_4.clicked.connect(functools.partial(self.products_window))
        self.pushButton_5.setVisible(root)
        self.pushButton_5.clicked.connect(functools.partial(self.UA))
        self.pushButton_8.clicked.connect(functools.partial(self.Confirmation, 
                                                            'Вы действительно хотите удалить товар из аукциона? (при удалении товара произойдёт списания 5% от текущей стоимости товара )',
                                                            self.r, 8))
        self.pushButton_9.clicked.connect(functools.partial(self.editMWT1, 'editMWT1'))
        self.pushButton_10.clicked.connect(functools.partial(self.editMWT2, 'editMWT2'))
        self.pushButton_11.clicked.connect(functools.partial(self.Confirmation, 'Вы действительно хотите выставить данный товар на аукцион ?', self.r, 11 ))
        self.retranslateUi(MainWindow)
        
        self.tableWidget.itemSelectionChanged.connect(functools.partial(self.click_of_table, 1))
        self.tableWidget_2.itemSelectionChanged.connect(functools.partial(self.click_of_table, 2))

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:14pt;\">Данные администратора</span></p></body></html>"))       
        self.pushButton_3.setText(_translate("MainWindow", "Просмотр истории торгов"))
        self.pushButton_4.setText(_translate("MainWindow", "Товары"))
        self.pushButton_5.setText(_translate("MainWindow", "Пользователи/Админы"))
        self.label_2.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:14pt;\">Баланс</span></p></body></html>"))
        self.pushButton_6.setText(_translate("MainWindow", "Пополнения баланса"))
        self.pushButton_7.setText(_translate("MainWindow", "Вывести деньги"))
        self.label_3.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">100$</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" color:#da8f15;\">Товары которые участвуют в аукционе</span></p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Номер лота"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Описание и доп. информация"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Фото товара"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Стартовая цена товара"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "дложенная цена"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Время начала аукциона"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Время окончания аукциона"))
        self.label_5.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" color:#da8f15;\">Товары которые купили или у которых вышло время аукциона</span></p></body></html>"))
        self.pushButton_8.setText(_translate("MainWindow", "Удалить выделенный товар"))
        self.pushButton_9.setText(_translate("MainWindow", "Редактировать"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Номер лота"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Описание и доп. информация"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Фото товара"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Стартовая цена товара"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Предложенная ценна"))
        item = self.tableWidget_2.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Статус"))
        item = self.tableWidget_2.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Покупатель"))
        self.pushButton_10.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_11.setText(_translate("MainWindow", "Выставить выделеный \n"
                                                            "тавар на торги вновь"))


    #Отслеживаем нажатые ячейки 
    def click_of_table(self, n):
        self.r.clear()
        if n == 1:
            row = self.tableWidget.currentRow() # Номер строки
            self.r.append(self.tableWidget.item(row, 0).text())
        elif n == 2:
            row = self.tableWidget_2.currentRow() # Номер строки
            self.r.append(self.tableWidget_2.item(row, 0).text())

    def editMWT1(self, k):
        try:     
            row = self.tableWidget.currentRow()
            date_time_obj = datetime.datetime.strptime(self.tableWidget.item(row, 5).text(), '%Y-%m-%d %H')
            dt_now = datetime.datetime.today()
            if date_time_obj > dt_now:
                p = []
                for s in range(self.tableWidget.columnCount()):
                    if s != 4:
                        p.append(self.tableWidget.item(row, s).text()) 
                Dialog = QtWidgets.QDialog()
                ui = editMW.Ui_Dialog(k, p)
                ui.setupUi(Dialog)
                result = Dialog.exec_()
                if result == QtWidgets.QDialog.Rejected:
                    self.auction()
            else:
                QMessageBox.warning(self.MainWindow, "Запрет к редактированию!!!", "Редактировать разрешено только лоты, в которых не началось время торгов")
        except AttributeError: 
            QMessageBox.warning(self.MainWindow, "Ошибка", "Пожалуйста, выберите строку перед созданием лота.")

    def editMWT2(self, k):
        try:
            row = self.tableWidget_2.currentRow()
            p = []
            for s in range(self.tableWidget_2.columnCount()):
                if s != 4 and s != 6 and s != 5:
                    p.append(self.tableWidget_2.item(row, s).text()) 
            Dialog = QtWidgets.QDialog()
            ui = editMW.Ui_Dialog(k, p)
            ui.setupUi(Dialog)
            result = Dialog.exec_()
            if result == QtWidgets.QDialog.Rejected:
                self.auction()
        except AttributeError: 
            QMessageBox.warning(self.MainWindow, "Ошибка", "Пожалуйста, выберите строку перед созданием лота.")

        

    # Заполнение таблиц на главной страницы 
    def auction(self):
        home_page = db.Auction()
        table, tableNULL, table1, table1NULL = home_page[0], home_page[1], home_page[2], home_page[3]
        self.tableWidget.setRowCount(len(table) + len(tableNULL))  # Создаем строки в таблице
        # Заполняем сталбцы с окончанием торгов и стартовую цену лота
        for k in range(len(table)):
            self.tableWidget.setItem(k, 0, QtWidgets.QTableWidgetItem(str(table[k][0])))
            self.tableWidget.setItem(k, 1, QtWidgets.QTableWidgetItem(str(table[k][1])))
            self.tableWidget.setItem(k, 2, QtWidgets.QTableWidgetItem(str(table[k][2])))
            self.tableWidget.setItem(k, 3, QtWidgets.QTableWidgetItem(str(table[k][3])))
            self.tableWidget.setItem(k, 4, QtWidgets.QTableWidgetItem(str(table[k][4])))
            self.tableWidget.setItem(k, 5, QtWidgets.QTableWidgetItem(str(table[k][5])))
            self.tableWidget.setItem(k, 6, QtWidgets.QTableWidgetItem(str(table[k][6])))

        for k in range(len(tableNULL)):
            self.tableWidget.setItem((k + len(table)), 0, QtWidgets.QTableWidgetItem(str(tableNULL[k][0])))
            self.tableWidget.setItem((k + len(table)), 1, QtWidgets.QTableWidgetItem(str(tableNULL[k][1])))
            self.tableWidget.setItem((k + len(table)), 2, QtWidgets.QTableWidgetItem(str(tableNULL[k][2])))
            self.tableWidget.setItem((k + len(table)), 3, QtWidgets.QTableWidgetItem(str(tableNULL[k][3])))
            self.tableWidget.setItem((k + len(table)), 4, QtWidgets.QTableWidgetItem('-'))
            self.tableWidget.setItem((k + len(table)), 5, QtWidgets.QTableWidgetItem(str(tableNULL[k][4])))
            self.tableWidget.setItem((k + len(table)), 6, QtWidgets.QTableWidgetItem(str(tableNULL[k][5])))
            

        self.tableWidget_2.setRowCount(len(table1) + len(table1NULL)) # Создаем строки в таблице# Заполняем сталбцы с окончанием торгов и стартовую цену лота
        for k in range(len(table1)):
            self.tableWidget_2.setItem(k, 0, QtWidgets.QTableWidgetItem(str(table1[k][0])))
            self.tableWidget_2.setItem(k, 1, QtWidgets.QTableWidgetItem(str(table1[k][1])))
            self.tableWidget_2.setItem(k, 2, QtWidgets.QTableWidgetItem(str(table1[k][2])))
            self.tableWidget_2.setItem(k, 3, QtWidgets.QTableWidgetItem(str(table1[k][3])))
            self.tableWidget_2.setItem(k, 4, QtWidgets.QTableWidgetItem(str(table1[k][4])))
            self.tableWidget_2.setItem(k, 5, QtWidgets.QTableWidgetItem(str(table1[k][5])))
            self.tableWidget_2.setItem(k, 6, QtWidgets.QTableWidgetItem(str(table1[k][6])))
        for k in range(len(table1NULL)):
            self.tableWidget_2.setItem(k + len(table1), 0, QtWidgets.QTableWidgetItem(str(table1NULL[k][0])))
            self.tableWidget_2.setItem(k + len(table1), 1, QtWidgets.QTableWidgetItem(str(table1NULL[k][1])))
            self.tableWidget_2.setItem(k + len(table1), 2, QtWidgets.QTableWidgetItem(str(table1NULL[k][2])))
            self.tableWidget_2.setItem(k + len(table1), 3, QtWidgets.QTableWidgetItem(str(table1NULL[k][3])))
            self.tableWidget_2.setItem(k + len(table1), 4, QtWidgets.QTableWidgetItem('-'))
            self.tableWidget_2.setItem(k + len(table1), 5, QtWidgets.QTableWidgetItem(str(table1NULL[k][4])))
            self.tableWidget_2.setItem(k + len(table1), 6, QtWidgets.QTableWidgetItem('-'))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget_2.resizeColumnsToContents()

    # Блокируем изменения ячейки
    def EditingBlock(self):
        row = self.tableWidget.currentRow()
        date_time_obj = datetime.datetime.strptime(self.tableWidget.item(row, 5).text(), '%Y-%m-%d %H:%M')
        dt_now = datetime.datetime.today()
        if date_time_obj > dt_now:
            None
        else:
            it = self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn())
            it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEditable)

    def EditingBlock_2(self):
        it = self.tableWidget_2.item(self.tableWidget_2.currentRow(), self.tableWidget_2.currentColumn())
        it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEditable)

    def ИТ(self):
        Dialog = QtWidgets.QDialog()
        ui = ИсторияТоргов.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.exec_()

    def UA(self):
        Dialog = QtWidgets.QDialog()
        ui = user_admin_window.Ui_Dialog()
        ui.setupUi(Dialog)
        ui.fill_admin_table()
        ui.fill_user_table()
        Dialog.exec_()

    def products_window(self):
        Dialog = QtWidgets.QDialog()
        ui = products_window.Ui_Dialog()
        ui.setupUi(Dialog)
        ui.fill_product_table()
        result = Dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            self.auction()

    def Confirmation(self, n, t, u):
        Dialog = QtWidgets.QDialog()
        ui = УдалениеТовара.Ui_Dialog(n, t, u)
        ui.setupUi(Dialog)
        result = Dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            self.auction()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.auction()
    MainWindow.show()
    sys.exit(app.exec_())