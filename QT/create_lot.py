from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from datetime import datetime, timedelta

from DataBase.database import db

start_time = datetime.now()
end_time = start_time + timedelta(days=3)
start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
class Ui_Dialog(object):

    def setupUi(self, Dialog, ):

        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(1117, 308)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 1081, 211))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(1)
        self.combo_box = QtWidgets.QComboBox(Dialog)
        self.combo_box_2 = QtWidgets.QComboBox(Dialog)
        self.combo_box.addItems(["Стандартный", "Ювелирный", "Историч ценный"])
        self.combo_box_2.addItems(["В процессе", "Продан", "Не продан"])
        self.tableWidget.setCellWidget(0, 5, self.combo_box)
        self.tableWidget.setCellWidget(0, 6, self.combo_box_2)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(970, 260, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.create)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Создать"))


    def table(self, product_id, price):
        table_column = ["ID Товара", "Стартовая цена", "ID Admin", "Начало аукциона", "Конец аукциона",
                        'Тип документа', 'Статус']
        self.tableWidget.setHorizontalHeaderLabels(table_column)

        self.tableWidget.setItem(0,0, QTableWidgetItem(str(product_id)))
        self.tableWidget.setItem(0,1, QTableWidgetItem(price))
        self.tableWidget.setItem(0,2, QTableWidgetItem(str(1)))
        self.tableWidget.setItem(0,3, QTableWidgetItem(start_time))
        self.tableWidget.setItem(0,4, QTableWidgetItem(end_time))

    def create(self):
        product_id = self.tableWidget.item(0, 0).text()
        starting_price = self.tableWidget.item(0, 1).text()
        seller_id = self.tableWidget.item(0, 2).text()
        start_time = self.tableWidget.item(0, 3).text()
        end_time = self.tableWidget.item(0, 4).text()

        document_type = self.combo_box.currentText()
        status = self.combo_box_2.currentText()

        db.create_lot(product_id, starting_price, seller_id, start_time, end_time, document_type, status)


        self.Dialog.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
