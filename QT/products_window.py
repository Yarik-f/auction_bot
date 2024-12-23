import functools

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QMessageBox
import product_child_window

from DataBase.database import db, item_is_not_editable


class Ui_Dialog(object):
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

        self.pushButton.clicked.connect(self.save_and_close)
        self.pushButton_2.clicked.connect(functools.partial(self.child_window, 'create'))
        self.pushButton_3.clicked.connect(self.delete_product)
        self.pushButton_4.clicked.connect(functools.partial(self.child_window, 'edit'))
        self.tableWidget.itemClicked.connect(self.get_lot)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "На главное"))
        self.pushButton_2.setText(_translate("Dialog", "Создать лот"))
        self.pushButton_3.setText(_translate("Dialog", "Удалить"))
        self.pushButton_4.setText(_translate("Dialog", "Редактировать"))

    def fill_lot_table(self):
        self.tableWidget.clearContents()
        products = db.get_lot_data()

        self.tableWidget.setRowCount(len(products))

        table_column = ["Название", "Описание", "Местоположение",  "Стартовая цена", 'Продавец',
                        'Начало аукциона', 'Конец аукциона', 'Тип документа', 'Ссылка на фото', 'Статус']

        self.tableWidget.setColumnCount(len(table_column))
        self.tableWidget.setHorizontalHeaderLabels(table_column)

        for i, product in enumerate(products):
            for j, value in enumerate(product):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))

        item_is_not_editable(self.tableWidget)
        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeColumnToContents(1)
        self.tableWidget.resizeColumnToContents(3)
        self.tableWidget.resizeColumnToContents(4)

    def get_lot(self):
        row = self.tableWidget.currentRow()
        if row != -1:
            title = self.tableWidget.item(row, 0).text()
            description = self.tableWidget.item(row, 1).text()
            location = self.tableWidget.item(row, 2).text()
            starting_price = self.tableWidget.item(row, 3).text()
            seller = self.tableWidget.item(row, 4).text()
            s_time = self.tableWidget.item(row, 5).text()
            e_time = self.tableWidget.item(row, 6).text()
            document_type = self.tableWidget.item(row, 7).text()
            image_path = self.tableWidget.item(row, 8).text()
            status = self.tableWidget.item(row, 9).text()
            lot_id = db.get_id_lot(title, description)

            return [lot_id, title, description, location, starting_price, seller, s_time, e_time, document_type, image_path, status]

    def child_window(self, check):
        selected_items = self.tableWidget.selectedItems()
        lot = self.get_lot()
        title = lot[1]
        description = lot[2]
        location = lot[3]
        starting_price = lot[4]
        seller = lot[5]
        s_time = lot[6]
        e_time = lot[7]
        document_type = lot[8]
        image_path = lot[9]
        status = lot[10]
        Dialog = QtWidgets.QDialog()
        ui = product_child_window.Ui_Dialog()

        if lot == None:
            ui.setupUi(Dialog, check)
        else:
            ui.setupUi(Dialog, check, lot[0])

        if check == 'create':
            ui.table()
            result = Dialog.exec_()
            if result == QtWidgets.QDialog.Accepted:
                self.fill_lot_table()
        elif check == 'edit' and selected_items and status != 'В процессе':
            ui.edit_table(title, description, location, starting_price, seller, s_time, e_time, document_type, image_path, status)
            result = Dialog.exec_()
            if result == QtWidgets.QDialog.Accepted:
                self.fill_lot_table()
        else:
            QMessageBox.warning(self.Dialog, "Ошибка", "Пожалуйста, выберите лот который не участвует в аукционе перед редактированием(Продан, Не продан).")

    def delete_product(self):
        selected_items = self.tableWidget.selectedItems()
        lot = self.get_lot()

        if selected_items and lot[10] != 'В процессе':
            db.delete_lot_and_images(lot[0])
            self.fill_lot_table()
        else:
            QMessageBox.warning(self.Dialog, "Ошибка", "Пожалуйста, выберите лот который не участвует в аукционе перед удалением(Продан, Не продан).")
    def save_and_close(self):
        self.Dialog.accept()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.fill_lot_table()
    Dialog.show()
    sys.exit(app.exec_())