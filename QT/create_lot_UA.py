from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import random, string

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
            self.pushButton_2 = QtWidgets.QPushButton(Dialog)
            self.pushButton_2.setGeometry(QtCore.QRect(50, 260, 50, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.pushButton_2.setFont(font)
            self.pushButton_2.setObjectName("pushButton_2")
            self.pushButton_3 = QtWidgets.QPushButton(Dialog)
            self.pushButton_3.setGeometry(QtCore.QRect(120, 260, 50, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.pushButton_3.setFont(font)
            self.pushButton_3.setObjectName("pushButton_3")
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
            self.pushButton_2.clicked.connect(self.plus)
            self.pushButton_3.clicked.connect(self.minus)

        elif self.k == 'addAdmin': 
            self.pushButton_2 = QtWidgets.QPushButton(Dialog)
            self.pushButton_2.setGeometry(QtCore.QRect(50, 260, 50, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.pushButton_2.setFont(font)
            self.pushButton_2.setObjectName("pushButton_2")
            self.pushButton_3 = QtWidgets.QPushButton(Dialog)
            self.pushButton_3.setGeometry(QtCore.QRect(120, 260, 50, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.pushButton_3.setFont(font)
            self.pushButton_3.setObjectName("pushButton_3")
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
            self.combo_box.addItems(['2', '3'])
            self.tableWidget.setCellWidget(0, 3, self.combo_box)
            self.pushButton_2.clicked.connect(self.plus)
            self.pushButton_3.clicked.connect(self.minus)

        elif self.k == 'edit':
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setRowCount(1)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(3, item)
            self.combo_box = QtWidgets.QComboBox(Dialog)
            self.combo_box.addItems(['0', '1'])
            self.combo_box_2 = QtWidgets.QComboBox(Dialog)
            self.combo_box_2.addItems(['0', '1'])
            self.combo_box_3 = QtWidgets.QComboBox(Dialog)
            self.combo_box_3.addItems(['user', 'admin'])
            self.tableWidget.setCellWidget(0, 3, self.combo_box)
            self.tableWidget.setCellWidget(0, 2, self.combo_box_2)
            self.tableWidget.setCellWidget(0, 0, self.combo_box_3)

        elif self.k == 'editAdmin':
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
            self.combo_box.addItems(['admin', 'root'])
            self.tableWidget.setCellWidget(0, 2, self.combo_box)

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
            self.pushButton_2.setText(_translate("Dialog", "+"))
            self.pushButton_3.setText(_translate("Dialog", "-"))

        elif self.k == 'addAdmin':
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Имя пользователя"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Пароль"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Баланс"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Роль"))
            item = self.tableWidget.horizontalHeaderItem(4)
            item.setText(_translate("MainWindow", "Комисия"))
            item = self.tableWidget.horizontalHeaderItem(5)
            item.setText(_translate("MainWindow", "Страйки"))
            self.pushButton_2.setText(_translate("Dialog", "+"))
            self.pushButton_3.setText(_translate("Dialog", "-"))

        elif self.k == 'edit':
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "роль"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Кол.успеш.ставок"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Авто ставка"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Бан"))
            #for s in range(len(self.p)-1):
                #if s < 1:
                    #self.tableWidget.setItem(0, s, QTableWidgetItem(self.p[s]))
                #else:
                    #self.tableWidget.setItem(0, s, QTableWidgetItem(self.p[s+1]))
            self.tableWidget.setItem(0, 1, QTableWidgetItem(self.p[3]))
            
        elif self.k == 'editAdmin':
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Телеграм админа"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Пароль"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "роль"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Комисия"))
            item = self.tableWidget.horizontalHeaderItem(4)
            item.setText(_translate("MainWindow", "Страйки"))
            for s in range(len(self.p)-1):
                if s < 3:
                    self.tableWidget.setItem(0, s, QTableWidgetItem(self.p[s]))
                else:
                    self.tableWidget.setItem(0, s, QTableWidgetItem(self.p[s+1]))
        self.tableWidget.resizeColumnsToContents()

    def plus(self):
        if self.k == 'add':
            rowPosition = self.tableWidget.rowCount() # Узнаем количества строк в таблице 
            self.tableWidget.insertRow(rowPosition)
            n = f"self.combo_box_{self.tableWidget.rowCount()+2}" 
            n = QtWidgets.QComboBox(self.Dialog)
            n.addItems(['0', '1'])
            self.tableWidget.setCellWidget(self.tableWidget.rowCount()-1, 3, n)
            n = f"self.combo_box_{self.tableWidget.rowCount()+3}" 
            n = QtWidgets.QComboBox(self.Dialog)
            n.addItems(['0', '1'])
            self.tableWidget.setCellWidget(self.tableWidget.rowCount()-1, 4, n)
        elif self.k == 'addAdmin':
            rowPosition = self.tableWidget.rowCount() # Узнаем количества строк в таблице 
            self.tableWidget.insertRow(rowPosition)
            f"self.combo_box_{self.tableWidget.rowCount()} = {QtWidgets.QComboBox(self.Dialog).addItems(['2', '3'])}"
            globals()['self.combo_box_%s' % rowPosition] = QtWidgets.QComboBox(self.Dialog)
            globals()['self.combo_box_%s' % rowPosition].addItems(['2', '3'])
            self.tableWidget.setCellWidget(self.tableWidget.rowCount()-1, 3, globals()['self.combo_box_%s' % rowPosition] )
            
    def minus(self):
        if self.tableWidget.currentRow() > 0:        
            row = self.tableWidget.currentRow() # Отслеживаем строчку нажатой ячейки 
            self.tableWidget.removeRow(row) # Удаляем строчку и все элементы выбраной ячейки
        
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
                        pe.append(self.tableWidget.item(s, s1).text()) # Добовляем информацию данной ячейкм в список 
                db.add_user_db(pe)  

        elif self.k == 'addAdmin': 
            for s in range(self.tableWidget.rowCount()):
                pe = [] # Добовляес в список информацию о ячейках в новой строчки 
                for s1 in range(self.tableWidget.columnCount()): # 
                    if s1 == 3:
                        #pe.append(self.tableWidget.item(s, s1).currentText())
                        #pe.append(self.combo_box.currentText())
                        if s == 0:
                            pe.append(self.combo_box.currentText())
                        else:
                            try:
                                pe.append(globals()['self.combo_box_%s' % s].currentText())
                            except RuntimeError:
                                None # Нужно придумать проверку для удаления строки посередине создания новых администраторов 
                    elif s1 == 2 or s1 == 4 or s1 == 5:
                        try:
                            n = int(self.tableWidget.item(s, s1).text())
                            pe.append(n) # Добовляем информацию данной ячейкм в список
                        except ValueError:
                            return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "Нужно ввести число")
                    else:
                        pe.append(self.tableWidget.item(s, s1).text()) # Добовляем информацию данной ячейкм в список 
                db.add_user_A_db(pe) 
                
        elif self.k == 'edit':
            pe = [] # Добавляем в список информацию о редакции ячейки  
            print(self.tableWidget.columnCount())
            for s1 in range(self.tableWidget.columnCount()): # 
                if s1 == 0:
                    if self.combo_box_3.currentText() == 'user':
                        pe.append(1)
                    else:
                        pe.append(2)
                elif s1 == 2:
                    pe.append(self.combo_box_2.currentText())
                elif s1 == 3:
                    pe.append(self.combo_box.currentText())
                else:
                    try:
                        n = int(self.tableWidget.item(0, s1).text())
                        pe.append(n) # Добовляем информацию данной ячейкм в список 
                    except ValueError:
                        return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "Нужно ввести число")
            if self.combo_box_3.currentText() != 'user':  
                l = string.ascii_letters + string.digits
                r = random.choices(l, k = 8)
                lr = "".join(r)
                pe.append(lr)
            print(pe)
            db.search_db(pe, self.p)

        elif self.k == 'editAdmin':
            pe = [] # Добавляем в список информацию о редакции ячейки  
            for s1 in range(self.tableWidget.columnCount()): # 
                if s1 == 2:
                    if self.combo_box.currentText() == 'admin':
                        pe.append(2)
                    else:
                        pe.append(3)
                elif s1 == 3 or s1 == 4:
                    try:
                        n = int(self.tableWidget.item(0, s1).text())
                        pe.append(n) # Добовляем информацию данной ячейкм в список
                    except ValueError:
                        return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "Нужно ввести число")
                else:
                    pe.append(self.tableWidget.item(0, s1).text()) # Добовляем информацию данной ячейкм в список 
            db.edit_Admin_db(pe, self.p)

        self.Dialog.close()
         
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())