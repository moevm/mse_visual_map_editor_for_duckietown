from PyQt5 import QtWidgets
import mapviewer
import map
from main_design import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from IOManager import open_map, save_map_as, save_map, export_png
import functools


# pyuic5 main_design.ui -o main_design.py

class duck_window(QtWidgets.QMainWindow):
    map = None
    mapviewer = None

    def __init__(self):
        super().__init__()
        self.map = map.DuckietownMap()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        viewer = mapviewer.MapViewer()
        viewer.setMap(self.map)
        self.mapviewer = viewer
        viewer.setMinimumSize(540, 540)
        self.ui.horizontalLayout.addWidget(viewer)
        viewer.repaint()
        self.initUi()

    def initUi(self):
        self.center()
        self.show()

        # инициализация объектов кнопок
        create_map = self.ui.create_new
        open_map = self.ui.open_map
        save_map = self.ui.save_map
        save_map_as = self.ui.save_map_as
        export_png = self.ui.export_png
        calc_param = self.ui.calc_param
        calc_materials = self.ui.calc_materials
        help_info = self.ui.help_info
        about_author = self.ui.about_author
        exit = self.ui.exit
        change_blocks = self.ui.change_blocks
        change_info = self.ui.change_info
        change_map = self.ui.change_map

        # инициализация плавающих блоков
        block_widget = self.ui.block_widget
        info_widget = self.ui.info_widget
        map_info_widget = self.ui.map_info_widget

        # подключение действий к кнопкам
        create_map.triggered.connect(self.create_map_triggered)
        open_map.triggered.connect(self.open_map_triggered)
        save_map.triggered.connect(self.save_map_triggered)
        save_map_as.triggered.connect(self.save_map_as_triggered)
        export_png.triggered.connect(self.export_png_triggered)
        calc_param.triggered.connect(self.calc_param_triggered)
        calc_materials.triggered.connect(self.calc_materials_triggered)
        help_info.triggered.connect(self.help_info_triggered)
        about_author.triggered.connect(self.about_author_triggered)
        exit.triggered.connect(self.exit_triggered)

        change_blocks.toggled.connect(self.change_blocks_toggled)
        change_info.toggled.connect(self.change_info_toggled)
        change_map.toggled.connect(self.change_map_toggled)

        block_widget.closeEvent = functools.partial(self.blocks_event)
        info_widget.closeEvent = functools.partial(self.info_event)
        map_info_widget.closeEvent = functools.partial(self.map_event)

        # настройка QToolBar
        tool_bar = self.ui.tool_bar

        a1 = QtWidgets.QAction(QtGui.QIcon("img/icons/new.png"), 'Новая карта', self)
        a2 = QtWidgets.QAction(QtGui.QIcon("img/icons/open.png"), 'Открыть карту', self)
        a3 = QtWidgets.QAction(QtGui.QIcon("img/icons/save.png"), 'Сохранить карту', self)
        a4 = QtWidgets.QAction(QtGui.QIcon("img/icons/save_as.png"), 'Сохранить карту как', self)
        a5 = QtWidgets.QAction(QtGui.QIcon("img/icons/png.png"), 'Экспортировать в png', self)

        a1.triggered.connect(self.create_map_triggered)
        a2.triggered.connect(self.open_map_triggered)
        a3.triggered.connect(self.save_map_triggered)
        a4.triggered.connect(self.save_map_as_triggered)
        a5.triggered.connect(self.export_png_triggered)

        tool_bar.addAction(a1)
        tool_bar.addAction(a2)
        tool_bar.addAction(a3)
        tool_bar.addAction(a4)
        tool_bar.addAction(a5)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Действие по созданию новой карты
    def create_map_triggered(self):
        # TODO Действие по созданию новой карты
        print("создание новой карты")
        pass

    # Действия по открытию карты
    def open_map_triggered(self):
        # TODO Действия по открытию карты
        print("кнопка открыть файл нажата")
        open_map(self)
        self.mapviewer.scene().update()

    # Сохранение карты
    def save_map_triggered(self):
        save_map(self)
        print("кнопка сохранить файл нажата")

    # Сохранение карт с новым именем
    def save_map_as_triggered(self):
        save_map_as(self)
        print("кнопка сохранить файл как нажата")

    # Экспорт в png
    def export_png_triggered(self):
        export_png(self)
        print("кнопка сохранить в png")

    # Подсчёт характеристик карт
    def calc_param_triggered(self):
        # TODO Подсчёт характеристик карт
        pass

    # Расчёт требуемых материалов
    def calc_materials_triggered(self):
        # TODO Расчёт требуемых материалов
        pass

    # Вывод справки по работе с программой
    def help_info_triggered(self):
        # TODO Вывод справки по работе с программой
        pass

    # Вывод справки по работе с программой
    def about_author_triggered(self):
        # TODO Информация о великих создателях
        pass

    # Выход из программы
    def exit_triggered(self):
        reply = QMessageBox.question(self, "Выход из программы", "Вы точно хотите выйти?",
                                     QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QtCore.QCoreApplication.instance().quit()

    # скрытие меню о блоках
    def change_blocks_toggled(self):
        block = self.ui.block_widget
        if self.ui.change_blocks.isChecked():
            block.show()
            block.setFloating(False)
        else:
            block.close()

    # изменение состояния кнопки при закрытии
    def blocks_event(self, event):
        self.ui.change_blocks.setChecked(False)
        event.accept()

    # скрытие меню информации
    def change_info_toggled(self):
        block = self.ui.info_widget
        if self.ui.change_info.isChecked():
            block.show()
            block.setFloating(False)
        else:
            block.close()

    # изменение состояния кнопки при закрытии
    def info_event(self, event):
        self.ui.change_info.setChecked(False)
        event.accept()

    # скрытие меню о свойствах карты
    def change_map_toggled(self):
        block = self.ui.map_info_widget
        if self.ui.change_map.isChecked():
            block.show()
            block.setFloating(False)
        else:
            block.close()

    # изменение состояния кнопки при закрытии
    def map_event(self, event):
        self.ui.change_map.setChecked(False)
        event.accept()
