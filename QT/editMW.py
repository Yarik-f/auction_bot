from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import datetime

from main_window import editMW
from choose_image import Choose_Image
from DataBase.database import db

class Ui_Dialog(object):
    def __init__(self, k, p): 
        self.k = k
        self.p = p
    
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(1117, 308)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 1081, 211))
        self.tableWidget.setObjectName("tableWidget")
        if self.k == 'editMWT1':
            self.pushButton = QtWidgets.QPushButton(Dialog)
            self.pushButton.setGeometry(QtCore.QRect(970, 260, 121, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.pushButton.setFont(font)
            self.pushButton.setObjectName("pushButton")
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setRowCount(1)
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
            self.pushButton.clicked.connect(self.save)

        elif self.k == 'editMWT2':
            self.pushButton = QtWidgets.QPushButton(Dialog)
            self.pushButton.setGeometry(QtCore.QRect(970, 260, 121, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.pushButton.setFont(font)
            self.pushButton.setObjectName("pushButton")
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(1)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(2, item)
            self.pushButton.clicked.connect(self.save)

        elif self.k == 'editMWT22':
            self.pushButton_2 = QtWidgets.QPushButton(Dialog)
            self.pushButton_2.setGeometry(QtCore.QRect(900, 260, 200, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.pushButton_2.setFont(font)
            self.pushButton_2.setObjectName("pushButton")
            self.tableWidget.setColumnCount(8)
            self.tableWidget.setRowCount(1)
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
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(7, item)
            self.combo_box = QtWidgets.QComboBox(Dialog)
            self.combo_box.addItems(["Стандартный", "Ювелирный", "Историч ценный"])
            self.tableWidget.setCellWidget(0, 6, self.combo_box)
            self.pushButton_2.clicked.connect(self.addItemToAuction)

        
        self.tableWidget.cellDoubleClicked.connect(self.choose_image)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        if self.k == 'editMWT1':
            self.pushButton.setText(_translate("Dialog", "Изменить"))
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Описание и доп.информация"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Фото товара"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Стартовая цена товара"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Время начала аукцеона"))
            item = self.tableWidget.horizontalHeaderItem(4)
            item.setText(_translate("MainWindow", "Время окончания аукциона"))
            for s in range(len(self.p)):
                if s != 0:
                    self.tableWidget.setItem(0, s-1, QTableWidgetItem(self.p[s]))

        elif self.k == 'editMWT2':
            self.pushButton.setText(_translate("Dialog", "Изменить"))
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Описание и доп.информация"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Фото товара"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Стартовая цена товара"))
            for s in range(len(self.p)):
                if s != 0:
                    self.tableWidget.setItem(0, s-1, QTableWidgetItem(self.p[s]))

        elif self.k == 'editMWT22':
            self.pushButton_2.setText(_translate("Dialog", "Выставить лот на торги"))
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Название"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Описание и доп.информация")) 
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Место нахождения"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Стартовая цена товара"))
            item = self.tableWidget.horizontalHeaderItem(4)
            item.setText(_translate("MainWindow", "Время начала аукциона"))
            item = self.tableWidget.horizontalHeaderItem(5)
            item.setText(_translate("MainWindow", "Время окончания аукциона"))
            item = self.tableWidget.horizontalHeaderItem(6)
            item.setText(_translate("MainWindow", "Тип документа"))
            item = self.tableWidget.horizontalHeaderItem(7)
            item.setText(_translate("MainWindow", "Ссылка на фото"))
            p1, p2 = self.p[0], self.p[1]
            print((p1), (p2))
            self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(p1[0])))
            self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(p1[1])))
            self.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(p1[2])))
            self.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(str(p1[3])))
            self.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(str(p1[5])))
            self.tableWidget.setItem(0, 5, QtWidgets.QTableWidgetItem(str(p1[6])))
            self.tableWidget.setItem(0, 7, QtWidgets.QTableWidgetItem(str(p2[0])))

        self.tableWidget.resizeColumnsToContents()

    def addItemToAuction(self):
        pe = [self.p[0][4]] # Добовляес в список информацию о ячейках в новой строчки 
        for s1 in range(self.tableWidget.columnCount()): # 
            if s1 == 3:
                try:
                    pe.append(float(self.tableWidget.item(0, s1).text()))
                except ValueError:
                    return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "В столбец (Стартовая цена товара) нужно ввести число")
            elif s1 == 4:
                    try:
                        p = datetime.datetime.strptime(self.tableWidget.item(0, 4).text(), '%Y-%m-%d %H:%M')
                        dt_now = datetime.datetime.today()
                        if p >= dt_now:
                            pe.append(self.tableWidget.item(0, s1).text())
                        else:
                            return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "Введенное время Должно быть больше или равное настоящему")
                    except ValueError:
                        return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "Неверный способ заполнения времени \nпример (2000-01-01 00:00)")
            elif s1 == 5:
                    try:
                        p = datetime.datetime.strptime(self.tableWidget.item(0, 5).text(), '%Y-%m-%d %H:%M')
                        if p > (datetime.datetime.strptime(self.tableWidget.item(0, 4).text(),'%Y-%m-%d %H:%M')) + datetime.timedelta(days=3):
                            pe.append(self.tableWidget.item(0, s1).text())
                        else:
                            return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "Длительность аукциона должна быть минимум три дня")
                    except ValueError:
                        return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "Неверный способ заполнения времени \nпример (2000-01-01 00:00)")
            elif s1 == 6:
                pe.append(self.combo_box.currentText())
            else:
                pe.append(self.tableWidget.item(0, s1).text()) # Добовляем информацию данной ячейкм в список 
        db.addItemToAuction(pe)
        self.Dialog.close()
        
    def save(self):                
        if self.k == 'editMWT1':
            pe = [self.p[0]] # Добавляем в список информацию о редакции ячейки  
            for s1 in range(self.tableWidget.columnCount()): # Количество столбцов в таблице
                if s1 == 2:
                    try:
                        pe.append(float(self.tableWidget.item(0, s1).text()))
                    except ValueError:
                        return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "В столбец (Стартовая цена товара) нужно ввести число")
                elif s1 == 3 or s1 == 4:
                    try:
                        p = datetime.datetime.strptime(self.tableWidget.item(0, s1).text(),'%Y-%m-%d %H:%M')
                        pe.append(self.tableWidget.item(0, s1).text())
                    except ValueError:
                        return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "Неверный способ заполнения времени \nпример (2000-01-01 00:00)")
                else:
                    pe.append(self.tableWidget.item(0, s1).text()) # Добовляем информацию данной ячейкм в список 
            db.edit_MW1_db(pe)

        elif self.k == 'editMWT2':
            pe = [self.p[0]] # Добавляем в список информацию о редакции ячейки  
            for s1 in range(self.tableWidget.columnCount()): # 
                pe.append(self.tableWidget.item(0, s1).text()) # Добовляем информацию данной ячейкм в список 
            db.edit_MW2_db(pe)
           
        self.Dialog.close()

    def choose_image(self, row, column):
        if self.k == 'editMWT22':
            if row == 0 and column == 7:
                choose_image = QtWidgets.QDialog()
                ui = Choose_Image()
                ui.setupUi(choose_image)
                if choose_image.exec_() == QtWidgets.QDialog.Accepted:
                    link = ui.get_link()
                    if link:
                        self.tableWidget.setItem(row, column, QTableWidgetItem(link))
        else:
            if row == 0 and column == 1:
                choose_image = QtWidgets.QDialog()
                ui = Choose_Image()
                ui.setupUi(choose_image)
                if choose_image.exec_() == QtWidgets.QDialog.Accepted:
                    link = ui.get_link()
                    if link:
                        self.tableWidget.setItem(row, column, QTableWidgetItem(link))
        
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
