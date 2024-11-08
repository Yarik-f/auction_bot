import sys, os, functools
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from DataBase.database import db

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(850, 900)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(210, 0, 351, 41))
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(70, 50, 750, 750))
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 700))
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
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(70, 810, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(470, 810, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.tableWidget.itemSelectionChanged.connect(self.EditingBlock)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">История торгов</span></p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Номер предложения"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Номер лота"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Описание и доп. информация"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Фото товара"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Покупатель"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "Стартовая цена"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "Цена продажи"))
        self.pushButton.setText(_translate("Dialog", "Удалить выделенный товар\n"
" из списка"))
        self.pushButton_2.setText(_translate("Dialog", "Очистить весь список"))

        self.tableWidget.resizeColumnsToContents()

    def AddTradingHistory(self):
        home_page = db.AddTradingHistory_db()[0]
        self.tableWidget.setRowCount(len(home_page))  # Создаем строки в таблице
        # Заполняем сталбцы с окончанием торгов и стартовую цену лота
        for k in range(len(home_page)):
            print(home_page)
            self.tableWidget.setItem(k, 0, QtWidgets.QTableWidgetItem(str(home_page[k][0])))
            self.tableWidget.setItem(k, 1, QtWidgets.QTableWidgetItem(str(home_page[k][1])))
            self.tableWidget.setItem(k, 2, QtWidgets.QTableWidgetItem(str(home_page[k][2])))
            self.tableWidget.setItem(k, 3, QtWidgets.QTableWidgetItem(str(home_page[k][3])))
            self.tableWidget.setItem(k, 4, QtWidgets.QTableWidgetItem(str(home_page[k][4])))
            self.tableWidget.setItem(k, 5, QtWidgets.QTableWidgetItem(str(home_page[k][5])))
            self.tableWidget.setItem(k, 6, QtWidgets.QTableWidgetItem(str(home_page[k][6])))
        #self.tableWidget.sortItems(1, order=QtCore.Qt.AscendingOrder)
        self.tableWidget.setSortingEnabled(True)

    def EditingBlock(self):
        it = self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn())
        it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEditable)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.AddTradingHistory()
    Dialog.show()
    sys.exit(app.exec_())