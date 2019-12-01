from PyQt5 import QtWidgets
import mapviewer
import map
from main_design import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from IOManager import open_map, save_map_as, save_map, export_png, new_map
import functools


# pyuic5 main_design.ui -o main_design.py

class duck_window(QtWidgets.QMainWindow):
    map = None
    mapviewer = None

    def __init__(self):
        super().__init__()
        self.brush_button = QtWidgets.QToolButton()
        self.closeEvent = functools.partial(self.quit_program_event)
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

        self.brush_button.clicked.connect(self.bruch_mode)

        tool_bar.addAction(a1)
        tool_bar.addAction(a2)
        tool_bar.addAction(a3)
        tool_bar.addAction(a4)
        tool_bar.addAction(a5)
        tool_bar.addSeparator()
        tool_bar.addAction(b1)
        tool_bar.addAction(b2)
        tool_bar.addAction(b3)
        tool_bar.addAction(b4)
        tool_bar.addAction(b5)
        tool_bar.addSeparator()
        tool_bar.addWidget(self.brush_button)

        # Настройка меню Блоки
        block_list_widget = self.ui.block_list
        block_list_widget.itemClicked.connect(self.item_list_clicked)
        block_list_widget.itemDoubleClicked.connect(self.item_list_double_clicked)

        # Заполнение списка
        blocks_list = [
            ("empty", "img/tiles/empty.png"),
            ("straight", "img/tiles/straight.png"),
            ("curve_left", "img/tiles/curve_left.png"),
            ("curve_right", "img/tiles/curve_right.png"),
            ("3way_left", "img/tiles/three_way_left.png"),
            ("3way_right", "img/tiles/three_way_left.png"),
            ("4way", "img/tiles/four_way_center.png"),
            ("asphalt", "img/tiles/asphalt.png"),
            ("grass", "img/tiles/grass.png"),
            ("floor", "img/tiles/floor.png")
        ]

        for name, icon in blocks_list:
            widget = QtWidgets.QListWidgetItem(QtGui.QIcon(icon), name)
            block_list_widget.addItem(widget)

        # Настройка меню Редактор карты
        default_fill = self.ui.default_fill
        delete_fill = self.ui.delete_fill
        for name, icon in blocks_list:
            default_fill.addItem(QtGui.QIcon(icon), name)
            delete_fill.addItem(QtGui.QIcon(icon), name)
        default_fill.setCurrentText("grass")
        delete_fill.setCurrentText("empty")

        set_fill = self.ui.set_fill
        set_fill.clicked.connect(self.set_default_fill)


        # new = mapviewer.small_wigget()
        #
        # #self.ui.horizontal_layout.addSpacing(QtWidgets.QSpacerItem.)
        # self.ui.horizontal_layout.addWidget(new)



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Действие по созданию новой карты
    def create_map_triggered(self):
        new_map(self)
        print(self.map.tiles, self.map.items)
        self.mapviewer.scene().update()
        print("создание новой карты")

    # Действия по открытию карты
    def open_map_triggered(self):
        open_map(self)
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
        event.accept()

    # обработка клика по элементу из списка списку
    def item_list_clicked(self):
        name = self.ui.block_list.currentItem().text()
        # TODO Отрисовка блока на поле доп. информации по 1 клику( файл с информацией tiles.yaml)


        print(name)

    # 2й клик также перехватывается одинарным
    def item_list_double_clicked(self):
        name = self.ui.block_list.currentItem().text()
        # TODO Добавление блока на карту по 2 клику
        print(name)

    # Установка значений по умолчанию
    def set_default_fill(self):
        default_fill = self.ui.default_fill.currentText()
        delete_fill = self.ui.delete_fill.currentText()
        # TODO установка занчений по умолчанию
        print(default_fill, delete_fill)

    # Вызов функции копирования
    def copy_button_clicked(self):
        # TODO кнопка копирования
        print("copy")

    # Вызов функции вырезания
    def cut_button_clicked(self):
        # TODO Кновку вырезания
        print("cut")

    # Вызов функции вставки
    def insert_button_clicked(self):
        # TODO Кнопка вставки
        print("insert")

    # Вызов функции удаления
    def delete_button_clicked(self):
        # TODO Кнопка удаления
        print("delete")

    # Вызов функции отката
    def undo_button_clicked(self):
        #  TODO Кнопка возврата
        print("undo")

    # Включение режима кисти
    def bruch_mode(self):
        if self.brush_button.isChecked():
            print(True)
            #  TODO Кисть активна
        else:
            print(False)
