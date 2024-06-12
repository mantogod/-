from PyQt5 import QtWidgets, QtGui, QtCore

from UI import Ui_Form

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setup_control()
        
    def setup_control(self):   
        self.ui.pushButton.clicked.connect(self.buttonClicked)
        self.ui.pushButton.move(100, 50)
   
    def buttonclicked(self):
        COIN = self.ui.lineEdit.text()
        Time = self.ui.lineEdit_2.text()
        