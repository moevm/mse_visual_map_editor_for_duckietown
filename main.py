import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator
from mainwindow import duck_window

LANG_DIR = './resources/lang/qw'

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Install translator
    translator = QTranslator(app)
    locale = sys.argv[1] if len(sys.argv) == 2 else 'en' 
    translator.load('{}/lang_{}.qm'.format(LANG_DIR, locale))
    app.installTranslator(translator)
    
    window = duck_window()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
