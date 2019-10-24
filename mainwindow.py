from PyQt5 import QtWidgets
import mapviewer
import map
from main_design import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from IOManager import open_map


class duck_window(QtWidgets.QMainWindow):
    tiles = None

    def __init__(self):
        super().__init__()
        self.tiles = map.DuckietownMap()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        viewer = mapviewer.MapViewer()
        viewer.setTiles(self.tiles)
        viewer.setMinimumSize(540, 540)
        self.ui.horizontalLayout.addWidget(viewer)
        viewer.repaint()
        self.initUi()

    def initUi(self):
        self.center()
        self.show()

        open_map = self.ui.open_map
        save_map = self.ui.save_map
        save_map_as = self.ui.save_map_as
        export_png = self.ui.export_png
        calc_param = self.ui.calc_param
        calc_materials = self.ui.calc_materials
        help_info = self.ui.help_info
        about_author = self.ui.about_author
        exit = self.ui.exit

        open_map.triggered.connect(self.open_map_triggered)
        save_map.triggered.connect(self.save_map_triggered)
        save_map_as.triggered.connect(self.save_map_as_triggered)
        export_png.triggered.connect(self.export_png_triggered)
        calc_param.triggered.connect(self.calc_param_triggered)
        calc_materials.triggered.connect(self.calc_materials_triggered)
        help_info.triggered.connect(self.help_info_triggered)
        about_author.triggered.connect(self.about_author_triggered)
        exit.triggered.connect(self.exit_triggered)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_map_triggered(self):
        #TODO Действия по открытию карты
        print("кнопка открыть файл нажата")
        open_map(self)


    def save_map_triggered(self):
        #TODO Сохранение карты
        print("кнопка сохранить файл нажата")

    def save_map_as_triggered(self):
        #TODO Сохранение карт с новым именем
        print("кнопка сохранить файл как нажата")

    def export_png_triggered(self):
        #TODO Экспорт в png
        pass

    def calc_param_triggered(self):
        #TODO Подсчёт характеристик карт
        pass

    def calc_materials_triggered(self):
        #TODO Расчёт требуемых материалов
        pass

    def help_info_triggered(self):
        #TODO Вывод справки по работе с программой
        pass

    def about_author_triggered(self):
        #TODO Информация о великих создателях
        pass

    def exit_triggered(self):
        reply = QMessageBox.question(self, "Выход из программы", "Вы точно хотите выйти?",
                                     QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QtCore.QCoreApplication.instance().quit()
