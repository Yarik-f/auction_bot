from PyQt5 import QtCore, QtGui, QtWidgets
import functools
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from DataBase.database import db
from main_window import Ui_MainWindow 

class Ui_Dialog(object):
    def __init__(self, n, t):
        self.n = n
        self.t = t[0]

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(392, 213)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 160, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 351, 121))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(functools.partial(self.OK, self.t)) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        
        self.textEdit.setReadOnly(True)
        self.textEdit.setPlainText(self.n)

        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit.setFont(font)
        #self.textEdit.setCurrentFont(QtGui.QFont())

    def OK (self, t):
        db.qwe(t)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        ui.auction()
        #app = QtWidgets.QApplication(sys.argv)
        #Window = QtWidgets.QDialog(flags=QtCore.Qt.WindowType.Dialog)
        #Window.close
        #Window.show()
        #sys.exit(app.exec_())
        

 
        
        
                
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
