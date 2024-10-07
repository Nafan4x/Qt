import sys
import math
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QApplication, QHBoxLayout
)
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QPoint


class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Начальные параметры круга
        self.circle_center = QPoint(150, 150)  # Центр окружности
        self.radius = 50  # Радиус заполненного круга
        self.angle = 0  # Угол смещения
        self.circle_pos = QPoint(150, 150)  # Текущая позиция заполненного круга

        # QLabel для отображения состояний
        self.label_A = QLabel("A", self)
        self.label_B = QLabel("B", self)

        # Инициализация состояния кнопок
        self.button_A_state = False
        self.button_B_state = False

        # Настройка интерфейса
        layout = QVBoxLayout()
        labels_layout = QHBoxLayout()

        labels_layout.addWidget(self.label_A)
        labels_layout.addWidget(self.label_B)
        layout.addLayout(labels_layout)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Рисуем внешнюю окружность
        painter.setPen(Qt.black)
        painter.drawEllipse(self.circle_center, 100, 100)

        # Рисуем заполненный круг
        painter.setBrush(QBrush(Qt.blue))
        painter.drawEllipse(self.circle_pos, self.radius, self.radius)

    def update_circle_position(self, angle, distance, button_A_state, button_B_state):
        """Метод для обновления позиции круга и состояния кнопок"""
        self.angle = angle
        self.radius = distance
        self.button_A_state = button_A_state
        self.button_B_state = button_B_state

        # Рассчитываем новую позицию круга
        radians = math.radians(self.angle)
        x_offset = int(math.cos(radians) * self.radius)
        y_offset = int(math.sin(radians) * self.radius)

        self.circle_pos = QPoint(self.circle_center.x() + x_offset, self.circle_center.y() + y_offset)

        # Меняем цвет QLabel в зависимости от состояния кнопок
        self.label_A.setStyleSheet("background-color: red" if self.button_A_state else "background-color: none")
        self.label_B.setStyleSheet("background-color: green" if self.button_B_state else "background-color: none")

        self.update()  # Перерисовываем виджет

    def reset_circle_position(self):
        """Сброс позиции круга к исходному центру"""
        self.circle_pos = self.circle_center
        self.update()

    def get_circle_position_and_button_states(self):
        """Возвращает текущую позицию круга и состояния кнопок"""
        return {
            "position": (self.circle_pos.x(), self.circle_pos.y()),
            "button_A_state": self.button_A_state,
            "button_B_state": self.button_B_state
        }


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.circle_widget = CircleWidget()

        # Кнопки управления
        self.button_update = QPushButton("Обновить", self)
        self.button_reset = QPushButton("Сброс", self)

        self.button_update.clicked.connect(self.on_update_circle)
        self.button_reset.clicked.connect(self.on_reset_circle)

        # Общий макет
        layout = QVBoxLayout()
        layout.addWidget(self.circle_widget)
        layout.addWidget(self.button_update)
        layout.addWidget(self.button_reset)

        self.setLayout(layout)

    def on_update_circle(self):
        """Обработчик для обновления позиции круга"""
        # Здесь мы просто передаем тестовые данные.
        # В реальной ситуации можно передавать значения из других элементов интерфейса.
        self.circle_widget.update_circle_position(angle=45, distance=70, button_A_state=True, button_B_state=False)

    def on_reset_circle(self):
        """Обработчик для сброса круга"""
        self.circle_widget.reset_circle_position()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_win = MainWindow()
    main_win.setWindowTitle("Circle Widget Example")
    main_win.resize(400, 400)
    main_win.show()

    sys.exit(app.exec_())
