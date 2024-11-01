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
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1111, 721))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 1081, 581))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(10, 630, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 630, 93, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 630, 131, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.tab)
        self.pushButton_4.setGeometry(QtCore.QRect(990, 630, 93, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 20, 1081, 581))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_5.setGeometry(QtCore.QRect(220, 630, 131, 31))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_6.setGeometry(QtCore.QRect(990, 630, 93, 31))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 630, 93, 31))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_8.setGeometry(QtCore.QRect(110, 630, 93, 31))
        self.pushButton_8.setObjectName("pushButton_8")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Добавить"))
        self.pushButton_2.setText(_translate("Dialog", "Удалить"))
        self.pushButton_3.setText(_translate("Dialog", "Редактировать"))
        self.pushButton_4.setText(_translate("Dialog", "Сохранить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Пользователи"))
        self.pushButton_5.setText(_translate("Dialog", "Редактировать"))
        self.pushButton_6.setText(_translate("Dialog", "Сохранить"))
        self.pushButton_7.setText(_translate("Dialog", "Добавить"))
        self.pushButton_8.setText(_translate("Dialog", "Удалить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Администраторы"))

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
    ui.fill_user_table()
    ui.fill_admin_table()
    Dialog.show()
    sys.exit(app.exec_())


