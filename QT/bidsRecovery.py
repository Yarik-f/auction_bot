from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys, os, datetime
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from DataBase.database import db
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(390, 120)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 85, 100, 35))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, -70, 350, 160))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(78, 30, 234, 56))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.OK) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.label.setText('Укажите диапазон времени для восстановления торгов!')
        self.label.setWordWrap(True)
        
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Начальное время"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Конечное время"))
        self.tableWidget.resizeColumnsToContents()

    def OK (self):
        try:
            startOfTimeRange = datetime.datetime.strptime(self.tableWidget.item(0, 0).text(), '%Y-%m-%d %H:%M') # Переводим строковый формат записи времени из конкретной ячейки таблицы в формат datetime 
            endOfTimeRange = datetime.datetime.strptime(self.tableWidget.item(0, 1).text(), '%Y-%m-%d %H:%M') # Переводим строковый формат записи времени из конкретной ячейки таблицы в формат datetime 
            if endOfTimeRange > startOfTimeRange: # Сравниваем два времени, начальное должно быть меньше конечного 
                db.bidsRecovery_db(startOfTimeRange, endOfTimeRange)
            else:
                return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "Конечное время должно быть больше начального!!!")
        except ValueError:
            return QMessageBox.warning(self.Dialog, "Запрет к редактированию!!!", "Неверный способ заполнения времени \nпример (2000-01-01 00:00)")
        self.Dialog.accept()
