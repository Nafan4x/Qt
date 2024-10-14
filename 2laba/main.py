import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from Joi import JoystickWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Joystick Demo")
        self.setGeometry(100, 100, 400, 400)

        # Создаем наш кастомный виджет джойстика
        self.joystick = JoystickWidget(self)

        # Кнопка для установки случайного положения джойстика
        self.set_position_button = QPushButton("Set Joystick Position", self)
        self.set_position_button.clicked.connect(self.set_random_position)

        # Кнопка для сброса джойстика
        self.reset_button = QPushButton("Reset Joystick", self)
        self.reset_button.clicked.connect(self.joystick.reset_joystick)

        # Layout для кнопок и виджета
        layout = QVBoxLayout()
        layout.addWidget(self.joystick)
        layout.addWidget(self.set_position_button)
        layout.addWidget(self.reset_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_random_position(self):
        # Устанавливаем положение джойстика (пример: угол 45 градусов, радиус 30)
        self.joystick.set_joystick_position(45, 30, True, False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
