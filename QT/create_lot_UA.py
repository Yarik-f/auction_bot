from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

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
        if self.k == 'add': 
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
            self.combo_box = QtWidgets.QComboBox(Dialog)
            self.combo_box.addItems(['0', '1'])
            self.combo_box_2 = QtWidgets.QComboBox(Dialog)
            self.combo_box_2.addItems(['0', '1'])
            self.tableWidget.setCellWidget(0, 3, self.combo_box)
            self.tableWidget.setCellWidget(0, 4, self.combo_box_2)
        elif self.k == 'edit':
            self.tableWidget.setColumnCount(6)
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
            self.combo_box = QtWidgets.QComboBox(Dialog)
            self.combo_box.addItems(['0', '1'])
            self.combo_box_2 = QtWidgets.QComboBox(Dialog)
            self.combo_box_2.addItems(['0', '1'])
            self.combo_box_3 = QtWidgets.QComboBox(Dialog)
            self.combo_box_3.addItems(['user'])
            self.tableWidget.setCellWidget(0, 4, self.combo_box)
            self.tableWidget.setCellWidget(0, 5, self.combo_box_2)
            self.tableWidget.setCellWidget(0, 1, self.combo_box_3)


        self.pushButton.clicked.connect(self.save)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Создать"))
        if self.k == 'add':
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Имя пользователя"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Баланс"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Кол.успеш.ставок"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Авто ставка"))
            item = self.tableWidget.horizontalHeaderItem(4)
            item.setText(_translate("MainWindow", "Бан"))
        elif self.k == 'edit':
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Телеграм пользователя"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "роль"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Баланс"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Кол.успеш.ставок"))
            item = self.tableWidget.horizontalHeaderItem(4)
            item.setText(_translate("MainWindow", "Авто ставка"))
            item = self.tableWidget.horizontalHeaderItem(5)
            item.setText(_translate("MainWindow", "Бан"))
            for s in range(len(self.p)):
                self.tableWidget.setItem(0, s, QTableWidgetItem(self.p[s]))


        self.tableWidget.resizeColumnsToContents()
    
    
        

    def save(self):
        if self.k == 'add': 
            for s in range(self.tableWidget.rowCount()):
                pe = [] # Добовляес в список информацию о ячейках в новой строчки 
                for s1 in range(self.tableWidget.columnCount()): # 
                    if s1 == 3:
                        pe.append(self.combo_box.currentText())
                    elif s1 == 4:
                        pe.append(self.combo_box_2.currentText())
                    else:
                        #print(self.tableWidget.item(s, s1).text())
                        pe.append(self.tableWidget.item(s, s1).text()) # Добовляем информацию данной ячейкм в список 
                db.add_user_db(pe)  
        elif self.k == 'edit':
            pe = [] # Добавляем в список информацию о редакции ячейки  
            for s1 in range(self.tableWidget.columnCount()): # 
                if s1 == 1:
                    pe.append(self.combo_box_3.currentText())
                elif s1 == 4:
                    pe.append(self.combo_box.currentText())
                elif s1 == 5:
                    pe.append(self.combo_box_2.currentText())
                else:
                    #print(self.tableWidget.item(s, s1).text())
                    pe.append(self.tableWidget.item(0, s1).text()) # Добовляем информацию данной ячейкм в список 
            db.edit_User_db(pe, self.p)
           

        self.Dialog.close()
        
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
