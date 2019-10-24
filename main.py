import sys
from PyQt5 import QtWidgets
from mainwindow import duck_window


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = duck_window()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
