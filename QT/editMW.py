from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

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
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(970, 260, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 1081, 211))
        self.tableWidget.setObjectName("tableWidget")
        if self.k == 'editMWT1':
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

        elif self.k == 'editMWT2':
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(1)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(2, item)

        self.pushButton.clicked.connect(self.save)
        self.tableWidget.cellDoubleClicked.connect(self.choose_image)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Изменить"))
        if self.k == 'editMWT1':
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
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Описание и доп.информация"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Фото товара"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Стартовая цена товара"))
            for s in range(len(self.p)):
                if s != 0:
                    self.tableWidget.setItem(0, s-1, QTableWidgetItem(self.p[s]))

        self.tableWidget.resizeColumnsToContents()
        
    def save(self):                
        if self.k == 'editMWT1':
            pe = [self.p[0]] # Добавляем в список информацию о редакции ячейки  
            for s1 in range(self.tableWidget.columnCount()): # 
                pe.append(self.tableWidget.item(0, s1).text()) # Добовляем информацию данной ячейкм в список 
            db.edit_MW1_db(pe)

        elif self.k == 'editMWT2':
            pe = [self.p[0]] # Добавляем в список информацию о редакции ячейки  
            for s1 in range(self.tableWidget.columnCount()): # 
                pe.append(self.tableWidget.item(0, s1).text()) # Добовляем информацию данной ячейкм в список 
            db.edit_MW2_db(pe)
           
        self.Dialog.close()

    def choose_image(self, row, column):
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
