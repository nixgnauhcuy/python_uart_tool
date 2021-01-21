import os
import sys

from Ui_uart_tool_ui import Ui_MainWindow
from PyQt5.QtWidgets import (QApplication, QMainWindow)


class MyPyQT_Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
