V_NAME=.venv

# 1. Установить библиотеку python-tk
# apt install python-tk
# 2. Установить virtualenv
# pip2 install virtualenv

virtualenv -p python2.7 $V_NAME
source $V_NAME/bin/activate
pip2 install -r requirements.txt

#vscode: в Python: Venv Folders добавить имя из переменной V_NAME

# Запуск пространства: source $V_NAME/bin/activate
# Выход из пространства: deactivate
# Установка пакета: pip2 install <package_name>
# Список пакетов: pip2 list
# Выгрузка пакетов в файл: python2.7 -m pip freeze > requirements.txt

