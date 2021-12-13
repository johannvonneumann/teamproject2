import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
# pyrcc5 ./Asiae_AI_GUI/image/파일이름.qrc -o 파일이름.py

form_window = uic.loadUiType('./mainwidget.ui')[0]
class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())

