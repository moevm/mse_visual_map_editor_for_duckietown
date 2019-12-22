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


# pyuic5 main_design.ui -o main_design.py

class duck_window(QtWidgets.QMainWindow):
    map = None
    mapviewer = None
    info_json = None
    editor = None
    drawState = ''
    copyBuffer = [[]]

    def __init__(self):
        super().__init__()
        # доп. окна для вывода информации
        self.author_window = info_window()
        self.param_window = info_window()
        self.mater_window = info_window()

        # кнопка для кисти и переопределение события закрытия
        self.brush_button = QtWidgets.QToolButton()
        self.closeEvent = functools.partial(self.quit_program_event)

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


        read_file = codecs.open("doc/info.json", "r", "utf-8")
        self.info_json = json.load(read_file)

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

        a1 = QtWidgets.QAction(QtGui.QIcon("img/icons/new.png"), 'Новая карта', self)
        a2 = QtWidgets.QAction(QtGui.QIcon("img/icons/open.png"), 'Открыть карту', self)
        a3 = QtWidgets.QAction(QtGui.QIcon("img/icons/save.png"), 'Сохранить карту', self)
        a4 = QtWidgets.QAction(QtGui.QIcon("img/icons/save_as.png"), 'Сохранить карту как', self)
        a5 = QtWidgets.QAction(QtGui.QIcon("img/icons/png.png"), 'Экспортировать в png', self)

        b1 = QtWidgets.QAction(QtGui.QIcon("img/icons/copy.png"), 'Копировать', self)
        b2 = QtWidgets.QAction(QtGui.QIcon("img/icons/cut.png"), 'Вырезать', self)
        b3 = QtWidgets.QAction(QtGui.QIcon("img/icons/insert.png"), 'Вставить', self)
        b4 = QtWidgets.QAction(QtGui.QIcon("img/icons/delete.png"), 'Удалить', self)
        b5 = QtWidgets.QAction(QtGui.QIcon("img/icons/undo.png"), 'Откатить изменение', self)
        b1.setShortcut("Ctrl+C")
        b2.setShortcut("Ctrl+X")
        b3.setShortcut("Ctrl+V")
        b4.setShortcut("Delete")
        b5.setShortcut("Ctrl+Z")

        c1 = QtWidgets.QAction(self)
        c1.setShortcut("R")
        c1.triggered.connect(self.rotateSelectedTiles)
        self.addAction(c1)
        c2 = QtWidgets.QAction(self)
        c2.setShortcut("Ctrl+R")
        c2.triggered.connect(self.rotateSelected)
        self.addAction(c2)
        c3 = QtWidgets.QAction(self)
        c3.setShortcut('Ctrl+F')
        c3.triggered.connect(self.trimClicked)
        self.addAction(c3)

        self.brush_button.setIcon(QtGui.QIcon("img/icons/brush.png"))
        self.brush_button.setCheckable(True)
        self.brush_button.setToolTip("Режим кисти")
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

        self.brush_button.clicked.connect(self.brush_mode)

        for elem in [[a1, a2, a3, a4, a5], [b1, b2, b3, b4, b5]]:
            for act in elem:
                tool_bar.addAction(act)
            tool_bar.addSeparator()
        tool_bar.addWidget(self.brush_button)

        # Настройка меню Блоки
        block_list_widget = self.ui.block_list
        block_list_widget.itemClicked.connect(self.item_list_clicked)
        block_list_widget.itemDoubleClicked.connect(self.item_list_double_clicked)

        # Заполнение списка
        blocks_list = [
            ("Куски дороги", "separator", "road", "img/icons/galka.png"),
            ("Дорога", "straight", "road", "img/tiles/straight.png"),
            ("Левый поворот", "curve_left", "road", "img/tiles/curve_left.png"),
            ("Правый поворот", "curve_right", "road", "img/tiles/curve_right.png"),
            ("T-образный левый перекрёсток", "3way_left", "road", "img/tiles/three_way_left.png"),
            ("T-образный правый перекрёсток", "3way_right", "road", "img/tiles/three_way_left.png"),
            ("Перекрёсток", "4way", "road", "img/tiles/four_way_center.png"),

            ("Блоки заполнения", "separator", "block", "img/icons/galka.png"),
            ("Пустой блок", "empty", "block", "img/tiles/empty.png"),
            ("Асфальт", "asphalt", "block", "img/tiles/asphalt.png"),
            ("Трава", "grass", "block", "img/tiles/grass.png"),
            ("Плитка", "floor", "block", "img/tiles/floor.png")
        ]

        signs_list = [
            ("Запрещающие знаки", "separator", "ban", "img/icons/galka.png"),
            ("Стоп", "sign_stop", "ban", "img/signs/sign_stop.png"),
            ("Уступи дорогу", "sign_yield", "ban", "img/signs/sign_yield.png"),
            ("Поворот направо запрещён", "sign_no_right_turn", "ban", "img/signs/sign_no_right_turn.png"),
            ("Поворот налево запрещён", "sign_no_left_turn", "ban", "img/signs/sign_no_left_turn.png"),
            ("Кирпич", "sign_do_not_enter", "ban", "img/signs/sign_do_not_enter.png"),

            ("Информационные знаки", "separator", "info", "img/icons/galka.png"),
            ("Односторонее движении направо", "sign_oneway_right", "info", "img/signs/sign_oneway_right.png"),
            ("Односторонее движении налево", "sign_oneway_left", "info", "img/signs/sign_oneway_left.png"),
            ("Перекрёсток", "sign_4_way_intersect", "info", "img/signs/sign_4_way_intersect.png"),
            ("T-образный правый перекрёсток", "sign_right_T_intersect", "info", "img/signs/sign_right_T_intersect.png"),
            ("T-образный левый перекрёсток", "sign_left_T_intersect", "info", "img/signs/sign_left_T_intersect.png"),
            ("T-образный перекрёсток", "sign_T_intersection", "info", "img/signs/sign_T_intersection.png"),

            ("Специальные знаки", "separator", "spec", "img/icons/galka.png"),
            ("Пешеход", "sign_pedestrian", "spec", "img/signs/sign_pedestrian.png"),
            ("Светофор", "sign_t_light_ahead", "spec", "img/signs/sign_t_light_ahead.png"),
            ("Уточки", "sign_duck_crossing", "spec", "img/signs/sign_duck_crossing.png"),
            ("Парковка", "sign_parking", "spec", "img/signs/sign_parking.png")
        ]

        object_list = [
            ("Городские объекты", "separator", "objects", "img/icons/galka.png"),
            ("Светофор","trafficlight","objects","img/objects/trafficlight.png"),
            ("Барьер", "barrier", "objects", "img/objects/barrier.png"),
            ("Конус", "cone", "objects", "img/objects/cone.png"),
            ("Уточка", "duckie", "objects", "img/objects/duckie.png"),
            ("Уточка-бот", "duckiebot", "objects", "img/objects/duckiebot.png"),
            ("Дерево", "tree", "objects", "img/objects/tree.png"),
            ("Дом", "house", "objects", "img/objects/house.png"),
            ("Грузовик(в стиле доставки)", "truck", "objects", "img/objects/truck.png"),
            ("Автобус", "bus", "objects", "img/objects/bus.png"),
            ("Здание(многоэтажное)", "building", "objects", "img/objects/building.png"),
        ]

        for elem in [blocks_list, signs_list, object_list]:
            for name, data, categ, icon in elem:
                widget = QtWidgets.QListWidgetItem(QtGui.QIcon(icon), name)
                widget.setData(0x0100, data)
                widget.setData(0x0101, categ)
                if data == "separator": widget.setBackground(QtGui.QColor(169, 169, 169))
                block_list_widget.addItem(widget)

        # Настройка меню Редактор карты
        default_fill = self.ui.default_fill
        delete_fill = self.ui.delete_fill
        for name, data, categ, icon in blocks_list:
            if data != "separator":
                default_fill.addItem(QtGui.QIcon(icon), name, data)
                delete_fill.addItem(QtGui.QIcon(icon), name, data)

        default_fill.setCurrentText("Трава")
        delete_fill.setCurrentText("Пустой блок")

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
        print(self.map.tiles, self.map.items)
        self.mapviewer.offsetX = self.mapviewer.offsetY = 0
        self.mapviewer.scene().update()
        print("создание новой карты")

    # Действия по открытию карты
    def open_map_triggered(self):
        open_map(self)
        self.mapviewer.offsetX = self.mapviewer.offsetY = 0
        self.mapviewer.scene().update()

    # Сохранение карты
    def save_map_triggered(self):
        save_map(self)

    # Сохранение карт с новым именем
    def save_map_as_triggered(self):
        save_map_as(self)

    # Экспорт в png
    def export_png_triggered(self):
        export_png(self)

    # Подсчёт характеристик карт
    def calc_param_triggered(self):

        text = get_map_specifications(self)
        self.show_info(self.param_window, "Характеристики карты", text)

    # Расчёт требуемых материалов
    def calc_materials_triggered(self):
        text = get_map_materials(self)
        self.show_info(self.mater_window, "Необходимые материалы", text)

    # Вывод справки по работе с программой
    def about_author_triggered(self):
        text = "Авторы:\n alskaa;\n dihindee; \n ovc-serega.\n\n Ищите нас на github!"
        self.show_info(self.author_window, "Об авторах", text)

    # Выход из программы
    def exit_triggered(self):
        ret = self.quit_MessageBox()
        if ret == QMessageBox.Cancel:
            return
        if ret == QMessageBox.Save:
            save_map(self)
        self.info.close()
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
        reply.setWindowTitle("Выход")
        reply.setText("Выход из программы")
        reply.setInformativeText("Выйти и сохранить?")
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
            elem = self.info_json[name]
            info_browser = self.ui.info_browser
            info_browser.clear()
            text = "Название:\n " + list.currentItem().text() \
                   + "\n\nОписание:\n " + elem["info"]
            if elem["type"] == "block":
                text += "\n\nДлина дороги: " + str(elem["length"]) + " см\n"
                text += "\nИзолента:\n"
                text += " Красная: " + str(elem["red"]) + " см\n"
                text += " Желтая: " + str(elem["yellow"]) + " см\n"
                text += " Белая: " + str(elem["white"]) + " см"
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
            print(name)

    # Установка значений по умолчанию
    def set_default_fill(self):
        default_fill = self.ui.default_fill.currentData()
        delete_fill = self.ui.delete_fill.currentData()
        # TODO установка занчений по умолчанию
        print(default_fill, delete_fill)

    # Вызов функции копирования
    def copy_button_clicked(self):
        if self.brush_button.isChecked():
            self.brush_button.click()
        self.drawState = 'copy'
        self.copyBuffer = copy.copy(self.mapviewer.tileSelection)
        print("copy")

    # Вызов функции вырезания
    def cut_button_clicked(self):
        if self.brush_button.isChecked():
            self.brush_button.click()
        self.drawState = 'cut'
        self.copyBuffer = copy.copy(self.mapviewer.tileSelection)
        print("cut")

    # Вызов функции вставки
    def insert_button_clicked(self):
        if len(self.copyBuffer) == 0:
            return
        if self.drawState == 'copy':
            self.editor.copySelection(self.copyBuffer, self.mapviewer.tileSelection[0], self.mapviewer.tileSelection[1],
                                      MapTile(self.ui.delete_fill.currentData()))
        elif self.drawState == 'cut':
            self.editor.moveSelection(self.copyBuffer, self.mapviewer.tileSelection[0], self.mapviewer.tileSelection[1],
                                      MapTile(self.ui.delete_fill.currentData()))
        self.mapviewer.scene().update()

    # Вызов функции удаления
    def delete_button_clicked(self):
        self.editor.deleteSelection(self.mapviewer.tileSelection, MapTile(self.ui.delete_fill.currentData()))
        self.mapviewer.scene().update()

    # Вызов функции отката
    def undo_button_clicked(self):
        #  TODO Кнопка возврата
        print("undo")

    # Включение режима кисти
    def brush_mode(self):
        # print('bruh click')
        if self.brush_button.isChecked():
            self.drawState = 'brush'
            #  TODO Кисть активна[4, 4, 8, 7]
        else:
            self.drawState = ''
    def rotateSelected(self):
        # TODO
        print("rotate selected rect")

    def rotateSelectedTiles(self):
        selection = self.mapviewer.tileSelection
        for i in range(selection[0], selection[2]):
            for j in range(selection[1], selection[3]):
                self.map.tiles[j][i].rotation = (self.map.tiles[j][i].rotation + 90) % 360
        self.mapviewer.scene().update()

    def trimClicked(self):
        print('trim clicked')
        self.editor.trimBorders(True,True,True,True,MapTile(self.ui.delete_fill.currentData()))

    def selectionUpdate(self):
        selection = self.mapviewer.tileSelection
        filler = MapTile(self.ui.default_fill.currentData())
        if self.drawState == 'brush':
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
                    self.map.tiles[j][i] = filler

    # функция создания доп. информационного окна
    def show_info(self, name, title, text):
        name.set_window_name(title)
        name.set_text(text)
        name.show()
