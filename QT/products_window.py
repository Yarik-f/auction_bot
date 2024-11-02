from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QDialog
import create_lot

from DataBase.database import db, item_is_not_editable


class Ui_Dialog(QtCore.QObject):
    lot_created = QtCore.pyqtSignal()
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(1117, 723)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 1081, 611))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(970, 670, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 670, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(180, 670, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(320, 670, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(460, 670, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton.clicked.connect(self.save_and_close)
        self.pushButton_5.clicked.connect(self.create_lot)
        self.tableWidget.itemClicked.connect(self.get_product_id_and_price)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Сохранить"))
        self.pushButton_2.setText(_translate("Dialog", "Добавить"))
        self.pushButton_3.setText(_translate("Dialog", "Удалить"))
        self.pushButton_4.setText(_translate("Dialog", "Редактировать"))
        self.pushButton_5.setText(_translate("Dialog", "Создать лот"))

    def fill_product_table(self):
        products = db.get_product_data()

        self.tableWidget.setRowCount(len(products))

        table_column = ["Название", "Описание", "Цена", "Количество", "Местоположение", 'Ссылка на фото']

        self.tableWidget.setColumnCount(len(table_column))
        self.tableWidget.setHorizontalHeaderLabels(table_column)

        for i, product in enumerate(products):
            for j, value in enumerate(product):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))

        item_is_not_editable(self.tableWidget)
        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeColumnToContents(1)
        self.tableWidget.resizeColumnToContents(4)
        self.tableWidget.resizeColumnToContents(5)

    def get_product_id_and_price(self):
        row = self.tableWidget.currentRow()
        if row != -1:
            title = self.tableWidget.item(row, 0).text()
            description = self.tableWidget.item(row, 1).text()
            price = self.tableWidget.item(row, 2).text()
            product_id = db.get_id_product(title, description)
            return [product_id, price]
    def create_lot(self):
        product = self.get_product_id_and_price()
        product_id = product[0]
        price = product[1]
        Dialog = QtWidgets.QDialog()
        ui = create_lot.Ui_Dialog()
        ui.setupUi(Dialog)
        ui.table(product_id, price)
        Dialog.exec_()

    def save_and_close(self):
        self.lot_created.emit()
        self.Dialog.close()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.fill_product_table()
    Dialog.show()
    sys.exit(app.exec_())
