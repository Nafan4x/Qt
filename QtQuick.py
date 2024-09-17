import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

def main():
    app = QApplication(sys.argv)

    # Используем QQmlApplicationEngine
    engine = QQmlApplicationEngine()
    engine.load("view.qml")

    # Проверяем, успешно ли загружен QML файл
    if not engine.rootObjects():
        print("Ошибка: не удалось загрузить QML файл.")
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
