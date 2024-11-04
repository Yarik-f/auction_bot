from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QDialog
from datetime import datetime, timedelta
from choose_image import Choose_Image
from DataBase.database import db

start_time = datetime.now()
end_time = start_time + timedelta(days=3)
start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
class Ui_Dialog(object):
    def setupUi(self, Dialog, check, product_id=None):
        self.product_id = product_id
        self.check = check
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(1117, 308)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 1081, 211))
        self.tableWidget.setObjectName("tableWidget")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(970, 260, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        if self.check == 'create':
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setRowCount(1)
            self.combo_box = QtWidgets.QComboBox(self.Dialog)
            self.combo_box_2 = QtWidgets.QComboBox(self.Dialog)
            self.combo_box.addItems(["Стандартный", "Ювелирный", "Историч ценный"])
            self.combo_box_2.addItems(["В процессе", "Продан", "Не продан"])
            self.tableWidget.setCellWidget(0, 5, self.combo_box)
            self.tableWidget.setCellWidget(0, 6, self.combo_box_2)
            table_column = ["ID Товара", "Стартовая цена", "ID Admin", "Начало аукциона", "Конец аукциона",
                            'Тип документа', 'Статус']
            self.tableWidget.setHorizontalHeaderLabels(table_column)

            self.pushButton.clicked.connect(self.create)
        else:
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setRowCount(1)
            table_column = ["Название", "Описание", "Цена", "Количество", "Местоположение", 'Ссылка на фото']
            self.tableWidget.setHorizontalHeaderLabels(table_column)

            self.tableWidget.cellDoubleClicked.connect(self.choose_image)
            if self.check == 'add':
                self.pushButton.clicked.connect(self.add_product_button)
            else:
                self.pushButton.clicked.connect(self.edit_product_button)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        if self.check == 'create':
            self.pushButton.setText(_translate("Dialog", "Создать"))
        else:
            if self.check == 'add':
                self.pushButton.setText(_translate("Dialog", "Добавить"))
            else:
                self.pushButton.setText(_translate("Dialog", "Сохранить"))



    def table(self, price):

        self.tableWidget.setItem(0,0, QTableWidgetItem(str(self.product_id)))
        self.tableWidget.setItem(0,1, QTableWidgetItem(price))
        self.tableWidget.setItem(0,2, QTableWidgetItem(str(1)))
        self.tableWidget.setItem(0,3, QTableWidgetItem(start_time))
        self.tableWidget.setItem(0,4, QTableWidgetItem(end_time))

        self.tableWidget.resizeColumnToContents(3)
        self.tableWidget.resizeColumnToContents(4)
    def create(self):
        row = self.tableWidget.currentRow()
        if row != -1:
            product_id = self.tableWidget.item(0, 0).text()
            starting_price = self.tableWidget.item(0, 1).text()
            seller_id = self.tableWidget.item(0, 2).text()
            start_time = self.tableWidget.item(0, 3).text()
            end_time = self.tableWidget.item(0, 4).text()

            document_type = self.combo_box.currentText()
            status = self.combo_box_2.currentText()

            db.create_lot(product_id, starting_price, seller_id, start_time, end_time, document_type, status)

            self.Dialog.close()

    def add_product_button(self):
        row = self.tableWidget.currentRow()
        if row != -1:
            title = self.tableWidget.item(0, 0).text()
            description = self.tableWidget.item(0, 1).text()
            price = self.tableWidget.item(0, 2).text()
            quantity = self.tableWidget.item(0, 3).text()
            location = self.tableWidget.item(0, 4).text()
            image_path = self.tableWidget.item(0, 5).text()
            db.add_product(title, description, price, quantity, location)
            product_id = db.get_id_product(title, description)
            db.add_product_image(image_path, product_id)
            self.Dialog.accept()


    def edit_table(self, title, description, price, quantity, location, image_path):
        self.tableWidget.setItem(0, 0, QTableWidgetItem(title))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(description))
        self.tableWidget.setItem(0, 2, QTableWidgetItem(price))
        self.tableWidget.setItem(0, 3, QTableWidgetItem(quantity))
        self.tableWidget.setItem(0, 4, QTableWidgetItem(location))
        self.tableWidget.setItem(0, 5, QTableWidgetItem(image_path))

    def edit_product_button(self):
            title = self.tableWidget.item(0, 0).text()
            description = self.tableWidget.item(0, 1).text()
            price = self.tableWidget.item(0, 2).text()
            quantity = self.tableWidget.item(0, 3).text()
            location = self.tableWidget.item(0, 4).text()
            image_path = self.tableWidget.item(0, 5).text()

            db.update_product(self.product_id, title=title, description=description, price=price, quantity=quantity,
                              location=location)

            db.update_product_image(image_path, self.product_id)

            self.Dialog.accept()


    def choose_image(self, row, column):
        if row == 0 and column == 5:
            choose_image = QtWidgets.QDialog()
            ui = Choose_Image()
            ui.setupUi(choose_image)
            if choose_image.exec_() == QDialog.Accepted:
                link = ui.get_link()
                if link:
                    self.tableWidget.setItem(row, column, QTableWidgetItem(link))


