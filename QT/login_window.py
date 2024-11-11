from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from DataBase.database import db

from main_window import Ui_MainWindow

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(1415, 856)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        Dialog.setMouseTracking(True)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setEnabled(True)
        self.frame.setGeometry(QtCore.QRect(540, 260, 301, 251))
        self.frame.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.frame.setMouseTracking(False)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(100, 190, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(52, 60, 181, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(50, 110, 181, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(50, 40, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(50, 90, 55, 16))
        self.label_2.setObjectName("label_2")

        self.input_username = self.lineEdit
        self.input_password = self.lineEdit_2
        self.input_password.setEchoMode(self.lineEdit_2.Password)

        self.pushButton.clicked.connect(self.check_login)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Войти"))
        self.label.setText(_translate("Dialog", "Login"))
        self.label_2.setText(_translate("Dialog", "Password"))

    def check_login(self):
        login = False
        root = False
        username = self.input_username.text()
        password = self.input_password.text()
        data = db.get_table_data('Admins')
        for i in range(0, len(data)):
            if username == data[i][1] and password == data[i][2]:
                if data[i][4] == 3:
                    root = True
                login = True
                break
        if login:
            print(root)
            Information = db.administratorInformation_db(username)
            self.open_main_window(root, Information)
        else:
            QMessageBox.warning(None, 'Error', 'Incorrect Username or Password')


    def open_main_window(self, root, Information):
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window, root, Information)
        self.ui.auction()
        self.main_window.show()
        self.Dialog.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
