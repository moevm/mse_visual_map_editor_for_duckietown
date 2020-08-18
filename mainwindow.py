# -*- coding: utf-8 -*-
import codecs

import mapviewer
import map

from maptile import MapTile
from mapEditor import MapEditor
from main_design import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from IOManager import *
import functools, json , copy
from infowindow import info_window
from logger import get_logger

logger = get_logger()


# pyuic5 main_design.ui -o main_design.py

_translate = QtCore.QCoreApplication.translate

class duck_window(QtWidgets.QMainWindow):
    map = None
    mapviewer = None
    info_json = None
    editor = None
    drawState = ''
    copyBuffer = [[]]

    def __init__(self, locale='en', elem_info="doc/info.json"):
        super().__init__()
        # доп. окна для вывода информации
        self.author_window = info_window()
        self.param_window = info_window()
        self.mater_window = info_window()

        # кнопка для кисти и переопределение события закрытия
        self.brush_button = QtWidgets.QToolButton()
        self.closeEvent = functools.partial(self.quit_program_event)

        # Set locale
        self.locale = locale
        
        # Load element's info
        self.info_json = json.load(codecs.open(elem_info, "r", "utf-8"))

        self.map = map.DuckietownMap()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        viewer = mapviewer.MapViewer()
        self.editor = MapEditor(self.map, self.mapviewer)
        viewer.setMap(self.map)
        self.mapviewer = viewer
        viewer.setMinimumSize(540, 540)
        self.ui.horizontalLayout.addWidget(viewer)
        viewer.repaint()
        self.initUi()

        init_map(self)

    def get_translation(self, elem):
        """Gets info about the element based on self.locale
        If local doesn't exist, return locale='en'

        :param self
        :param elem: dict, information about elements (or category), that contains translation
        :return: dict(). Dict with translation based on the self.locale
        """
        if self.locale in elem['lang']:
            return elem['lang'][self.locale]
        else:
            logger.debug("duck_window.get_translation. No such locale: {}".format(self.locale))
            return elem['lang']['en']

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
        about_author = self.ui.about_author
        exit = self.ui.exit
        change_blocks = self.ui.change_blocks
        change_info = self.ui.change_info
        change_map = self.ui.change_map

        # инициализация плавающих блоков
        block_widget = self.ui.block_widget
        info_widget = self.ui.info_widget
        map_info_widget = self.ui.map_info_widget

        # сигнал от viewer'а
        self.mapviewer.selectionChanged.connect(self.selectionUpdate)

        # подключение действий к кнопкам
        create_map.triggered.connect(self.create_map_triggered)
        open_map.triggered.connect(self.open_map_triggered)
        save_map.triggered.connect(self.save_map_triggered)
        save_map_as.triggered.connect(self.save_map_as_triggered)
        export_png.triggered.connect(self.export_png_triggered)
        calc_param.triggered.connect(self.calc_param_triggered)
        calc_materials.triggered.connect(self.calc_materials_triggered)
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

        a1 = QtWidgets.QAction(QtGui.QIcon("img/icons/new.png"), _translate("MainWindow", "New map"), self)
        a2 = QtWidgets.QAction(QtGui.QIcon("img/icons/open.png"), _translate("MainWindow", "Open map"), self)
        a3 = QtWidgets.QAction(QtGui.QIcon("img/icons/save.png"), _translate("MainWindow", "Save map"), self)
        a4 = QtWidgets.QAction(QtGui.QIcon("img/icons/save_as.png"), _translate("MainWindow", "Save map as"), self)
        a5 = QtWidgets.QAction(QtGui.QIcon("img/icons/png.png"), _translate("MainWindow", "Export to PNG"), self)

        b1 = QtWidgets.QAction(QtGui.QIcon("img/icons/copy.png"), _translate("MainWindow", "Copy"), self)
        b2 = QtWidgets.QAction(QtGui.QIcon("img/icons/cut.png"), _translate("MainWindow", "Cut"), self)
        b3 = QtWidgets.QAction(QtGui.QIcon("img/icons/insert.png"), _translate("MainWindow", "Paste"), self)
        b4 = QtWidgets.QAction(QtGui.QIcon("img/icons/delete.png"), _translate("MainWindow", "Delete"), self)
        b5 = QtWidgets.QAction(QtGui.QIcon("img/icons/undo.png"), _translate("MainWindow", "Undo"), self)
        b1.setShortcut("Ctrl+C")
        b2.setShortcut("Ctrl+X")
        b3.setShortcut("Ctrl+V")
        b4.setShortcut("Delete")
        b5.setShortcut("Ctrl+Z")

        c1 = QtWidgets.QAction(QtGui.QIcon("img/icons/rotate.png"), _translate("MainWindow", "Rotate"), self)
        c2 = QtWidgets.QAction(QtGui.QIcon("img/icons/trim.png"), _translate("MainWindow", "Delete extreme empty blocks"), self)
        c1.setShortcut("Ctrl+R")
        c2.setShortcut("Ctrl+F")

        self.brush_button.setIcon(QtGui.QIcon("img/icons/brush.png"))
        self.brush_button.setCheckable(True)
        self.brush_button.setToolTip("Brush tool")
        self.brush_button.setShortcut("Ctrl+B")

        a1.triggered.connect(self.create_map_triggered)
        a2.triggered.connect(self.open_map_triggered)
        a3.triggered.connect(self.save_map_triggered)
        a4.triggered.connect(self.save_map_as_triggered)
        a5.triggered.connect(self.export_png_triggered)

        b1.triggered.connect(self.copy_button_clicked)
        b2.triggered.connect(self.cut_button_clicked)
        b3.triggered.connect(self.insert_button_clicked)
        b4.triggered.connect(self.delete_button_clicked)
        b5.triggered.connect(self.undo_button_clicked)

        c1.triggered.connect(self.rotateSelectedTiles)
        c2.triggered.connect(self.trimClicked)

        self.brush_button.clicked.connect(self.brush_mode)

        for elem in [[a1, a2, a3, a4, a5], [b1, b2, b3, b4, b5]]:
            for act in elem:
                tool_bar.addAction(act)
            tool_bar.addSeparator()
        tool_bar.addWidget(self.brush_button)
        tool_bar.addAction(c1)
        tool_bar.addAction(c2)

        # Настройка меню Блоки
        block_list_widget = self.ui.block_list
        block_list_widget.itemClicked.connect(self.item_list_clicked)
        block_list_widget.itemDoubleClicked.connect(self.item_list_double_clicked)

        # Настройка меню Редактор карты
        default_fill = self.ui.default_fill
        delete_fill = self.ui.delete_fill

        # Заполнение списка
        categories = self.info_json['categories']
        information = self.info_json['info']
        for group in categories:
            # add separator
            icon = "img/icons/galka.png"
            widget = QtWidgets.QListWidgetItem(QtGui.QIcon(icon), self.get_translation(group)['name'])
            widget.setData(0x0100, "separator")
            widget.setData(0x0101, group['id'])
            widget.setBackground(QtGui.QColor(169, 169, 169))
            block_list_widget.addItem(widget)
            # add elements
            for elem_id in group['elements']:
                widget = QtWidgets.QListWidgetItem(QtGui.QIcon(information[elem_id]['icon']), self.get_translation(information[elem_id])['name'])
                widget.setData(0x0100, elem_id)
                widget.setData(0x0101, group['id'])
                block_list_widget.addItem(widget)
                # add tiles to fill menu
                if group['id'] in ("road", "block"):
                    default_fill.addItem(QtGui.QIcon(information[elem_id]['icon']), self.get_translation(information[elem_id])['name'], elem_id)
                    delete_fill.addItem(QtGui.QIcon(information[elem_id]['icon']), self.get_translation(information[elem_id])['name'], elem_id)

        default_fill.setCurrentText(self.get_translation(information["grass"])['name'])
        delete_fill.setCurrentText(self.get_translation(information["empty"])['name'])

        set_fill = self.ui.set_fill
        set_fill.clicked.connect(self.set_default_fill)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Действие по созданию новой карты
    def create_map_triggered(self):
        new_map(self)
        logger.debug("Length - {}; Items - {}".format(len(self.map.tiles), self.map.items))
        self.mapviewer.offsetX = self.mapviewer.offsetY = 0
        self.mapviewer.scene().update()
        logger.debug("Creating a new map")

    # Действия по открытию карты
    def open_map_triggered(self):
        self.editor.save(self.map)
        open_map(self)
        self.mapviewer.offsetX = self.mapviewer.offsetY = 0
        self.mapviewer.scene().update()

    # Сохранение карты
    def save_map_triggered(self):
        save_map(self)
        logger.debug("Save")

    # Сохранение карт с новым именем
    def save_map_as_triggered(self):
        save_map_as(self)

    # Экспорт в png
    def export_png_triggered(self):
        export_png(self)

    # Подсчёт характеристик карт
    def calc_param_triggered(self):

        text = get_map_specifications(self)
        self.show_info(self.param_window, _translate("MainWindow", "Map characteristics"), text)

    # Расчёт требуемых материалов
    def calc_materials_triggered(self):
        text = get_map_materials(self)
        self.show_info(self.mater_window, _translate("MainWindow", "Map material"), text)

    # Вывод справки по работе с программой
    def about_author_triggered(self):
        text = "Authors:\n alskaa;\n dihindee;\n ovc-serega;\n HardonCollider.\n\n Contact us on github!"
        self.show_info(self.author_window, "About", text)

    # Выход из программы
    def exit_triggered(self):
        ret = self.quit_MessageBox()
        if ret == QMessageBox.Cancel:
            return
        if ret == QMessageBox.Save:
            save_map(self)
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

    # MessageBox для выхода
    def quit_MessageBox(self):
        reply = QMessageBox(self)
        reply.setIcon(QMessageBox.Question)
        reply.setWindowTitle(_translate("MainWindow", "Exit"))
        reply.setText(_translate("MainWindow", "Exit"))
        reply.setInformativeText(_translate("MainWindow", "Save and exit?"))
        reply.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        reply.setDefaultButton(QMessageBox.Save)
        ret = reply.exec()
        return ret

    # Событие выхода из программы
    def quit_program_event(self, event):
        ret = self.quit_MessageBox()
        if ret == QMessageBox.Cancel:
            event.ignore()
            return
        if ret == QMessageBox.Save:
            save_map(self)

        # закрытие доп. диалоговых окон
        self.author_window.exit()
        self.param_window.exit()
        self.mater_window.exit()

        event.accept()

    # обработка клика по элементу из списка списку
    def item_list_clicked(self):
        list = self.ui.block_list
        name = list.currentItem().data(0x0100)
        type = list.currentItem().data(0x0101)

        if name == "separator":
            list.currentItem().setSelected(False)

            for i in range(list.count()):
                elem = list.item(i)
                if type == elem.data(0x0101):
                    if name == elem.data(0x0100):
                        icon = QtGui.QIcon("img/icons/galka.png") if list.item(i + 1).isHidden() else \
                            QtGui.QIcon("img/icons/galka_r.png")
                        elem.setIcon(icon)
                    else:
                        elem.setHidden(not elem.isHidden())
        else:
            elem = self.info_json['info'][name]
            info_browser = self.ui.info_browser
            info_browser.clear()
            text = "{}:\n {}\n{}:\n{}".format(_translate("MainWindow", "Name"), list.currentItem().text(), _translate("MainWindow", "Description"), self.get_translation(elem)['info'])
            if elem["type"] == "block":
                text += "\n\n{}: {} {}".format(_translate("MainWindow", "Road len"), elem["length"], _translate("MainWindow", "sm"))
                text += " Tape:\n"
                text += " {}: {} {}\n".format(_translate("MainWindow", "Red"), elem["red"], _translate("MainWindow", "sm"))
                text += " {}: {} {}\n".format(_translate("MainWindow", "Yellow"), elem["yellow"], _translate("MainWindow", "sm"))
                text += " {}: {} {}\n".format(_translate("MainWindow", "White"), elem["white"], _translate("MainWindow", "sm"))
            info_browser.setText(text)

    # 2й клик также перехватывается одинарным
    def item_list_double_clicked(self):
        list = self.ui.block_list
        name = list.currentItem().data(0x0100)
        type = list.currentItem().data(0x0101)

        if name == "separator":
            list.currentItem().setSelected(False)
        else:
            # TODO Добавление блока на карту по 2 клику
            logger.debug("Name: {}".format(name))

    # Установка значений по умолчанию
    def set_default_fill(self):
        default_fill = self.ui.default_fill.currentData()
        delete_fill = self.ui.delete_fill.currentData()
        # TODO установка занчений по умолчанию
        logger.debug("{}; {}".format(default_fill, delete_fill))

    # Вызов функции копирования
    def copy_button_clicked(self):
        if self.brush_button.isChecked():
            self.brush_button.click()
        self.drawState = 'copy'
        self.copyBuffer = copy.copy(self.mapviewer.tileSelection)
        logger.debug("Copy")

    # Вызов функции вырезания
    def cut_button_clicked(self):
        if self.brush_button.isChecked():
            self.brush_button.click()
        self.drawState = 'cut'
        self.copyBuffer = copy.copy(self.mapviewer.tileSelection)
        logger.debug("Cut")

    # Вызов функции вставки
    def insert_button_clicked(self):
        if len(self.copyBuffer) == 0:
            return
        self.editor.save(self.map)
        if self.drawState == 'copy':
            self.editor.copySelection(self.copyBuffer, self.mapviewer.tileSelection[0], self.mapviewer.tileSelection[1],
                                      MapTile(self.ui.delete_fill.currentData()))
        elif self.drawState == 'cut':
            self.editor.moveSelection(self.copyBuffer, self.mapviewer.tileSelection[0], self.mapviewer.tileSelection[1],
                                      MapTile(self.ui.delete_fill.currentData()))
        self.mapviewer.scene().update()

    # Вызов функции удаления
    def delete_button_clicked(self):
        self.editor.save(self.map)
        self.editor.deleteSelection(self.mapviewer.tileSelection, MapTile(self.ui.delete_fill.currentData()))
        self.mapviewer.scene().update()

    # Вызов функции отката
    def undo_button_clicked(self):
        self.editor.undo()
        self.mapviewer.scene().update()

    # Включение режима кисти
    def brush_mode(self):
        if self.brush_button.isChecked():
            self.drawState = 'brush'
        else:
            self.drawState = ''


    def rotateSelectedTiles(self):
        self.editor.save(self.map)
        selection = self.mapviewer.tileSelection
        if selection:
            for i in range(max(selection[1], 0), min(selection[3], len(self.map.tiles))):
                for j in range(max(selection[0], 0), min(selection[2], len(self.map.tiles[0]))):
                    self.map.tiles[i][j].rotation = (self.map.tiles[i][j].rotation + 90) % 360
            self.mapviewer.scene().update()

    def trimClicked(self):
        self.editor.save(self.map)
        self.editor.trimBorders(True,True,True,True,MapTile(self.ui.delete_fill.currentData()))
        self.mapviewer.scene().update()

    def selectionUpdate(self):
        selection = self.mapviewer.tileSelection
        filler = MapTile(self.ui.default_fill.currentData())
        if self.drawState == 'brush':
            self.editor.save(self.map)
            self.editor.extendToFit(selection, selection[0], selection[1], MapTile(self.ui.delete_fill.currentData()))
            if selection[0] < 0:
                delta = -selection[0]
                selection[0] = 0
                selection[2] += delta
            if selection[1] < 0:
                delta = -selection[1]
                selection[3] += delta
            for i in range(max(selection[0], 0), min(selection[2], len(self.map.tiles[0]))):
                for j in range(max(selection[1], 0), min(selection[3], len(self.map.tiles))):
                    self.map.tiles[j][i] = copy.copy(filler)
        self.mapviewer.scene().update()

    # функция создания доп. информационного окна
    def show_info(self, name, title, text):
        name.set_window_name(title)
        name.set_text(text)
        name.show()
