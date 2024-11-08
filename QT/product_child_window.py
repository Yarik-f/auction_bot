from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QDialog
from datetime import datetime, timedelta
from choose_image import Choose_Image
from DataBase.database import db


class Ui_Dialog(object):
    def setupUi(self, Dialog, check, lot_id=None):
        self.lot_id = lot_id
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


        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(1)
        self.combo_box = QtWidgets.QComboBox(self.Dialog)
        self.combo_box_2 = QtWidgets.QComboBox(self.Dialog)
        self.combo_box.addItems(["Стандартный", "Ювелирный", "Историч ценный"])
        self.combo_box_2.addItems(["В процессе", "Продан", "Не продан"])
        self.tableWidget.setCellWidget(0, 7, self.combo_box)
        self.tableWidget.setCellWidget(0, 9, self.combo_box_2)
        table_column = ["Название", "Описание", "Местоположение", "Стартовая цена", 'Продавец',
                        'Начало аукциона', 'Конец аукциона', 'Тип документа', 'Ссылка на фото', 'Статус']
        self.tableWidget.setHorizontalHeaderLabels(table_column)

        self.tableWidget.cellDoubleClicked.connect(self.choose_image)

        if self.check == 'create':
            self.pushButton.clicked.connect(self.create_lot)
        else:
            self.pushButton.clicked.connect(self.edit_lot_button)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        if self.check == 'create':
            self.pushButton.setText(_translate("Dialog", "Создать"))
        else:
            self.pushButton.setText(_translate("Dialog", "Сохранить"))



    def table(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(days=3)
        start_time = start_time.strftime('%Y-%m-%d %H:%M')
        print(start_time)
        end_time = end_time.strftime('%Y-%m-%d %H:%M')

        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(1)))
        self.tableWidget.setItem(0, 5, QTableWidgetItem(start_time))
        self.tableWidget.setItem(0, 6, QTableWidgetItem(end_time))




    def create_lot(self):
        row = self.tableWidget.currentRow()
        if row != -1:
            title = self.tableWidget.item(0, 0).text()
            description = self.tableWidget.item(0, 1).text()
            location = self.tableWidget.item(0, 2).text()
            starting_price = self.tableWidget.item(0, 3).text()
            seller = self.tableWidget.item(0, 4).text()
            s_time = self.tableWidget.item(0, 5).text()
            e_time = self.tableWidget.item(0, 6).text()
            document_type = self.combo_box.currentText()
            image_path = self.tableWidget.item(0, 8).text()
            status = self.combo_box_2.currentText()

            db.create_lot(title, description, location, starting_price, seller, s_time, e_time, document_type, status)
            lot_id = db.get_id_lot(title, description)
            db.add_lot_image(image_path, lot_id)
            self.Dialog.accept()


    def edit_table(self, title, description, location, starting_price, seller, s_time, e_time, document_type, image_path, status):
        self.tableWidget.setItem(0, 0, QTableWidgetItem(title))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(description))
        self.tableWidget.setItem(0, 2, QTableWidgetItem(location))
        self.tableWidget.setItem(0, 3, QTableWidgetItem(starting_price))
        self.tableWidget.setItem(0, 4, QTableWidgetItem(seller))
        self.tableWidget.setItem(0, 5, QTableWidgetItem(s_time))
        self.tableWidget.setItem(0, 6, QTableWidgetItem(e_time))
        self.tableWidget.setItem(0, 7, QTableWidgetItem(document_type))
        self.tableWidget.setItem(0, 8, QTableWidgetItem(image_path))
        self.tableWidget.setItem(0, 9, QTableWidgetItem(status))

        self.tableWidget.resizeColumnToContents(1)
        self.tableWidget.resizeColumnToContents(3)
        self.tableWidget.resizeColumnToContents(4)

    def edit_lot_button(self):
        title = self.tableWidget.item(0, 0).text()
        description = self.tableWidget.item(0, 1).text()
        location = self.tableWidget.item(0, 2).text()
        starting_price = self.tableWidget.item(0, 3).text()
        seller = self.tableWidget.item(0, 4).text()
        s_time = self.tableWidget.item(0, 5).text()
        e_time = self.tableWidget.item(0, 6).text()
        document_type = self.combo_box.currentText()
        image_path = self.tableWidget.item(0, 8).text()
        status = self.combo_box_2.currentText()

        seller_id = db.get_admin_id(seller)


        db.update_lot(self.lot_id, title=title, description=description, location=location, starting_price=starting_price,
                      seller_id=seller_id, start_time=s_time, end_time=e_time, document_type=document_type, status=status)

        db.update_lot_image(image_path, self.lot_id)

        self.Dialog.accept()


    def choose_image(self, row, column):
        if row == 0 and column == 8:
            choose_image = QtWidgets.QDialog()
            ui = Choose_Image()
            ui.setupUi(choose_image)
            if choose_image.exec_() == QDialog.Accepted:
                link = ui.get_link()
                if link:
                    self.tableWidget.setItem(row, column, QTableWidgetItem(link))


