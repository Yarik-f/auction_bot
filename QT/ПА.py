
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)


from DataBase.database import db, item_is_not_editable




class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1117, 723)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(70, 70, 981, 231))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget_2 = QtWidgets.QTableWidget(Dialog)
        self.tableWidget_2.setGeometry(QtCore.QRect(80, 400, 981, 231))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(530, 25, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(530, 350, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(180, 320, 121, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 660, 111, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Пользователь"))
        self.label_2.setText(_translate("Dialog", "Администратор"))
        self.pushButton.setText(_translate("Dialog", "Сохранить"))
        self.pushButton_2.setText(_translate("Dialog", "Сохранить"))



    def fill_user_table(self):
        users = db.get_user_data()

        self.tableWidget.setRowCount(len(users))

        table_column = ["Телеграм пользователя", "Роль", "Баланс", "Кол. Успеш. ставок", "Авто. ставка", "Бан"]

        self.tableWidget.setColumnCount(len(table_column))
        self.tableWidget.setHorizontalHeaderLabels(table_column)

        for i, user in enumerate(users):
            for j, value in enumerate(user):
                if j == 4 or j == 5:
                    if value == 0:
                        self.tableWidget.setItem(i, j, QTableWidgetItem('Нет'))
                    else:
                        self.tableWidget.setItem(i, j, QTableWidgetItem('Да'))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))

        item_is_not_editable(self.tableWidget)

        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeColumnToContents(3)

    def fill_admin_table(self):
        admins = db.get_admin_data()

        self.tableWidget_2.setRowCount(len(admins))

        table_column = ["Телеграм админа", 'Пароль', "Роль", "Баланс", "Коммисия", "Страйки"]

        self.tableWidget_2.setColumnCount(len(table_column))
        self.tableWidget_2.setHorizontalHeaderLabels(table_column)

        for i, admin in enumerate(admins):
            for j, value in enumerate(admin):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(value)))

        item_is_not_editable(self.tableWidget_2)

        self.tableWidget_2.resizeColumnToContents(0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.fill_admin_table()
    ui.fill_user_table()
    Dialog.show()
    sys.exit(app.exec_())
