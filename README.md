# mse_visual_map_editor_for_duckietown
Приложение, предназначенное для редактирования карт симулятора duckietown.

## Запуск приложения
### Необходимые пакеты
* python 3.5
* pyQt5 5.13
### Запуск
С помощью интерпритатора запустить main.py

## Сборка однопакетного приложения под конкретную ОС

## Перед сборкой приложения
Для корректной сборки приложения должен быть установлен python(версия 3.5).

Необходимо установить следующие библиотеки:
* для **linux** 
```bash
pip3 install pyinstaller
pip3 install PyQt5
```
* для **windows**:
```bash
pip3 install pyinstaller
pip3 install PyQt5
pip3 install pypiwin32
``` 


## Сборка и запуск приложения
В командной строке для **windows** \ в консоли для **linux** необходимо выполнить следующие действия:
```git
git clone https://github.com/moevm/mse_visual_map_editor_for_duckietown.git
``` 
Перейти в директорию репозитория и ввести команду:
```bash
pyinstaller --onefile --noconsole main.py
```
После этого в директории ```/dist``` будет сгенерирован исполняемый файл ```main.exe``` для Windows и ```main``` для Linux. Его можно запустить из консоли или по щелчку мыши.

В случае, если pyinstaller не сможет получить доступ к какой-либо библиотеке, необходимо выполнить команду 
```bash
pyinstaller --onefile --paths [path] --noconsole main.py
``` 
где ```[path]``` - путь до библиотеки,
например ```--paths D:\python35\Lib\site-packages\PyQt5\Qt\bin) ```.
