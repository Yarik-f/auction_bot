from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from DataBase.database import db



class Ui_Dialog(object):
    def __init__(self, id, sign): # 
        self.id = id
        self.sign = sign

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(582, 150)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(370, 110, 75, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(470, 110, 75, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(40, 60, 501, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(240, 20, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.pushButton.clicked.connect(self.OK)
        self.pushButton_2.clicked.connect(self.cancellation)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "OK"))
        self.pushButton_2.setText(_translate("Dialog", "Омена"))
        self.label.setText(_translate("Dialog", "TextLabel"))

    def cancellation(self):        
        self.Dialog.close()

    def OK(self):
        if self.sign == 'plus':
            try:
                textSearch = float(self.lineEdit.displayText())
                newBalance = db.adminBalance_db(self.id) + textSearch
                print(newBalance)
                db.addBalanceMain(newBalance, self.id)
            except ValueError:
                return QMessageBox.warning(self.Dialog, "Ошибка", "Нужно ввести число")
            self.Dialog.accept()
        else:
            try:
                textSearch = float(self.lineEdit.displayText())
                newBalance = db.adminBalance_db(self.id) - textSearch
                if newBalance >= 0:
                    db.addBalanceMain(newBalance, self.id)
                else:
                    return QMessageBox.warning(self.Dialog, "Ошибка", "Недостаточно средств!!!")
            except ValueError:
                return QMessageBox.warning(self.Dialog, "Ошибка", "Нужно ввести число")
            self.Dialog.accept()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
