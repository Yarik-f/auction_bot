from PyQt5 import QtCore, QtGui, QtWidgets
import functools
import sqlite3 as sl
import datetime

from DataBase.database import db

import ИсторияТоргов, УдалениеТовара, ПА, НовыйЛот, products_window





class Ui_MainWindow(object):
    def setupUi(self, MainWindow, root=True):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1323, 907)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setIconSize(QtCore.QSize(50, 50))
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(26, 22, 371, 41))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 130, 185, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setIconSize(QtCore.QSize(16, 16))
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 130, 160, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(450, 130, 210, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(680, 130, 265, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(970, 130, 180, 40))
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
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label_4.setFont(font)
        self.label_4.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_4.setTabletTracking(False)
        self.label_4.setObjectName("label_4")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(100, 220, 1100, 250))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
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
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tableWidget.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
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
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(280, 540, 761, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label_5.setFont(font)
        self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_5.setTabletTracking(False)
        self.label_5.setObjectName("label_5")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(500, 480, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")
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
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(150, 820, 220, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(530, 820, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(940, 810, 220, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_11.setFont(font)
        self.pushButton_11.setMouseTracking(False)
        self.pushButton_11.setTabletTracking(False)
        self.pushButton_11.setAcceptDrops(False)
        self.pushButton_11.setToolTip("")
        self.pushButton_11.setAutoFillBackground(False)
        self.pushButton_11.setInputMethodHints(QtCore.Qt.ImhNone)
        self.pushButton_11.setCheckable(False)
        self.pushButton_11.setChecked(False)
        self.pushButton_11.setAutoRepeat(False)
        self.pushButton_11.setAutoExclusive(False)
        self.pushButton_11.setAutoDefault(False)
        self.pushButton_11.setDefault(False)
        self.pushButton_11.setFlat(False)
        self.pushButton_11.setObjectName("pushButton_11")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1323, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.Auction()
        # self.tableWidget.itemSelectionChanged.connect(self.EditingBlock)

        self.pushButton_2.clicked.connect(functools.partial(self.НЛ))
        self.pushButton_3.clicked.connect(functools.partial(self.ИТ))
        self.pushButton_4.clicked.connect(functools.partial(self.products_window))
        self.pushButton_5.setVisible(root)
        self.pushButton_5.clicked.connect(functools.partial(self.UA))
        self.pushButton_8.clicked.connect(functools.partial(self.Confirmation, 'УТ'))
        self.pushButton_11.clicked.connect(functools.partial(self.Confirmation, 'ВТ'))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Данные администратора</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Редактировать данные"))
        self.pushButton_2.setText(_translate("MainWindow", "Создать новый лот"))
        self.pushButton_3.setText(_translate("MainWindow", "Просмотр истории торгов"))
        self.pushButton_4.setText(_translate("MainWindow", "Товары"))
        self.pushButton_5.setText(_translate("MainWindow", "Пользователи/Админы"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Баланс</span></p></body></html>"))
        self.pushButton_6.setText(_translate("MainWindow", "Пополнения баланса"))
        self.pushButton_7.setText(_translate("MainWindow", "Вывести деньги"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">100$</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#da8f15;\">Товары которые участвуют в аукционе</span></p></body></html>"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Описание и доп. информация"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Фото товара"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Стартовая цена товара"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "дложенная цена"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Время окончания аукциона"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#da8f15;\">Товары которые купили или у которых вышло время аукциона</span></p></body></html>"))
        self.pushButton_8.setText(_translate("MainWindow", "Удалить выделенный товар"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Описание и доп. информация"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Фото товара"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Стартовая цена товара"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Предложенная ценна"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Статус"))
        item = self.tableWidget_2.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Покупатель"))
        item = self.tableWidget_2.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Статус оплаты"))
        self.pushButton_9.setText(_translate("MainWindow", "Удалить выделенный \n"
"товар из списка"))
        self.pushButton_10.setText(_translate("MainWindow", "Очистить весь список"))
        self.pushButton_11.setText(_translate("MainWindow", "Выставить выделеный \n"
"тавар на торги вновь")) 

    # Заполнение таблицы товаров на аукционе     
    # def Auction(self):
    #     dt_now = (datetime.datetime.now()) # Определяем текущее время
    #
    #     with con:
    #         #con.execute(f"""UPDATE Lots
    #                             #SET status = 'продан'
    #                             #WHERE lot_id = 3""")
    #
    #         table = con.execute(f"""SELECT description, image_pt, starting_price, MAX(bid_amount), end_time FROM Lots
    #                                     INNER JOIN Products
    #                                         ON Lots.product_id = Products.product_id
    #                                     INNER JOIN Product_images
    #                                         ON Lots.product_id = Product_images.product_id
    #                                     INNER JOIN Bids
    #                                         ON Lots.lot_id = Bids.lot_id
    #                                      WHERE Lots.end_time >= '{dt_now}'
    #                                      GROUP BY Bids.lot_id""")   # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
    #         table = table.fetchall()
    #
    #         tableNULL = con.execute(f"""SELECT description, image_pt, starting_price, end_time FROM Lots
    #                                     INNER JOIN Products
    #                                         ON Lots.product_id = Products.product_id
    #                                     INNER JOIN Product_images
    #                                         ON Lots.product_id = Product_images.product_id
    #                                     LEFT JOIN Bids
    #                                         ON Bids.lot_id = Lots.lot_id
    #                                      WHERE Lots.end_time >= '{dt_now}' AND Bids.lot_id IS NULL
    #                                      """)   # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
    #         tableNULL = tableNULL.fetchall()
    #
    #         self.tableWidget.setRowCount(len(table) + len(tableNULL)) # Создаем строки в таблице
    #         # Заполняем сталбцы с окончанием торгов и стартовую цену лота
    #         for k in range (len(table)):
    #             self.tableWidget.setItem(k, 0, QtWidgets.QTableWidgetItem(str(table[k][0])))
    #             self.tableWidget.setItem(k, 1, QtWidgets.QTableWidgetItem(str(table[k][1])))
    #             self.tableWidget.setItem(k, 2, QtWidgets.QTableWidgetItem(str(table[k][2])))
    #             self.tableWidget.setItem(k, 3, QtWidgets.QTableWidgetItem(str(table[k][3])))
    #             self.tableWidget.setItem(k, 4, QtWidgets.QTableWidgetItem(str(table[k][4])))
    #
    #         for k in range (len(tableNULL)):
    #             self.tableWidget.setItem((k + len(table)), 0, QtWidgets.QTableWidgetItem(str(tableNULL[k][0])))
    #             self.tableWidget.setItem((k + len(table)), 1, QtWidgets.QTableWidgetItem(str(tableNULL[k][1])))
    #             self.tableWidget.setItem((k + len(table)), 2, QtWidgets.QTableWidgetItem(str(tableNULL[k][2])))
    #             self.tableWidget.setItem((k + len(table)), 3, QtWidgets.QTableWidgetItem('-'))
    #             self.tableWidget.setItem((k + len(table)), 4, QtWidgets.QTableWidgetItem(str(tableNULL[k][3])))
    #
    #
    #         table1 = con.execute(f"""SELECT description, image_pt, starting_price, final_price, status, username FROM Auction_history
    #                                  INNER JOIN Lots
    #                                     ON Auction_history.lot_id = Lots.product_id
    #                                  INNER JOIN Products
    #                                     ON Lots.product_id = Products.product_id
    #                                  INNER JOIN Product_images
    #                                     ON Lots.product_id = Product_images.product_id
    #                                  INNER JOIN Users
    #                                     ON Auction_history.winner_id = Users.user_id
    #                                  WHERE Lots.end_time < '{dt_now}'""")   # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
    #         table1 = table1.fetchall()
    #
    #         self.tableWidget_2.setRowCount(len(table1)) # Создаем строки в таблице# Заполняем сталбцы с окончанием торгов и стартовую цену лота
    #         for k in range (len(table1)):
    #             self.tableWidget_2.setItem(k, 0, QtWidgets.QTableWidgetItem(str(table1[k][0])))
    #             self.tableWidget_2.setItem(k, 1, QtWidgets.QTableWidgetItem(str(table1[k][1])))
    #             self.tableWidget_2.setItem(k, 2, QtWidgets.QTableWidgetItem(str(table1[k][2])))
    #             self.tableWidget_2.setItem(k, 3, QtWidgets.QTableWidgetItem(str(table1[k][3])))
    #             self.tableWidget_2.setItem(k, 4, QtWidgets.QTableWidgetItem(str(table1[k][4])))
    #             self.tableWidget_2.setItem(k, 5, QtWidgets.QTableWidgetItem(str(table1[k][5])))
    #             self.tableWidget_2.setItem(k, 6, QtWidgets.QTableWidgetItem('оплачено (?????????)'))
    #
    # # Блокируем изменения ячейки
    # def EditingBlock(self):
    #     it = QtWidgets.QTableWidgetItem(self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn()).text())
    #     it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEditable)
    #     self.tableWidget.setItem(self.tableWidget.currentRow(), self.tableWidget.currentColumn(), it)
        
                          

            



    def ИТ(self):
        Dialog = QtWidgets.QDialog()
        ui = ИсторияТоргов.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.exec_()
    
    def НЛ(self):
        Dialog = QtWidgets.QDialog()
        ui = НовыйЛот.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.exec_()

    def UA(self):
        Dialog = QtWidgets.QDialog()
        ui = ПА.Ui_Dialog()
        ui.setupUi(Dialog)
        ui.fill_admin_table()
        ui.fill_user_table()
        Dialog.exec_()
    def products_window(self):
        Dialog = QtWidgets.QDialog()
        ui = products_window.Ui_Dialog()
        ui.setupUi(Dialog)
        ui.fill_product_table()
        Dialog.exec_()

    def Confirmation(self, n):
        if n == 'УТ':
            Dialog = QtWidgets.QDialog()
            ui = УдалениеТовара.Ui_Dialog()
            ui.setupUi(Dialog)
            Dialog.exec_()
        # elif n == 'ВТ':
        #     Dialog = QtWidgets.QDialog()
        #     ui = ВыставлениеТовара.Ui_Dialog()
        #     ui.setupUi(Dialog)
        #     Dialog.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
