from setuptools import setup

# Чтение зависимостей из requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

APP = ['main.py']  # Замените 'main.py' на имя вашего основного файла
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5'],
    'includes': ['PyQt5.QtWidgets', 'PyQt5.QtCore', 'PyQt5.QtGui'],  # Включите все модули, которые вы используете
    'excludes': ['tkinter'],  # Исключите модули, которые вам не нужны
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)