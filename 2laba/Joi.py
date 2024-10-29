from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QPointF, pyqtSlot
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor
import math


class JoystickWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.angle = 0  # Угол поворота джойстика
        self.radius = 0  # Радиус отклонения джойстика
        self.button_a_state = False  # Состояние кнопки A
        self.button_b_state = False  # Состояние кнопки B

        self.circle_radius = 50  # Радиус окружности джойстика
        self.joystick_radius = 15  # Радиус перемещаемого кружка

        # Создаем QLabel для отображения состояния кнопок
        self.label_a = QLabel("A", self)
        self.label_b = QLabel("B", self)
        self.label_a.setFixedSize(80, 30)
        self.label_b.setFixedSize(80, 30)

        self.label_a.setStyleSheet("background-color: red")
        self.label_b.setStyleSheet("background-color: red")

        layout = QVBoxLayout()
        layout.addWidget(self.label_a)
        layout.addWidget(self.label_b)
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Рисуем окружность джойстика
        center = self.rect().center()
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.setBrush(QBrush(Qt.GlobalColor.white))
        painter.drawEllipse(center, self.circle_radius, self.circle_radius)

        # Вычисляем положение смещенного круга
        offset_x = self.radius * math.cos(math.radians(self.angle))
        offset_y = self.radius * math.sin(math.radians(self.angle))
        joystick_pos = QPointF(center.x() + offset_x, center.y() - offset_y)

        # Рисуем перемещаемый круг
        painter.setBrush(QBrush(Qt.GlobalColor.black))
        painter.drawEllipse(joystick_pos, self.joystick_radius, self.joystick_radius)

    @pyqtSlot(float, float, bool, bool)
    def set_joystick_position(self, angle, radius, button_a_state, button_b_state):
        """Слот для установки положения джойстика и состояния кнопок"""
        self.angle = angle
        self.radius = min(radius, self.circle_radius)  # Ограничиваем радиус
        self.button_a_state = button_a_state
        self.button_b_state = button_b_state

        if self.button_a_state:
            self.label_a.setStyleSheet("background-color: green")
        else:
            self.label_a.setStyleSheet("background-color: red")

        if self.button_b_state:
            self.label_b.setStyleSheet("background-color: green")
        else:
            self.label_b.setStyleSheet("background-color: red")


        self.update()  # Перерисовываем виджет

    @pyqtSlot()
    def reset_joystick(self):
        """Слот для сброса положения джойстика в центр"""
        self.angle = 0
        self.radius = 0

        self.label_a.setStyleSheet("background-color: red")
        self.label_a.setStyleSheet("background-color: red")

        self.update()

    def get_joystick_state(self):
        """Метод для получения текущего положения и состояния кнопок"""
        return {
            'angle': self.angle,
            'radius': self.radius,
            'button_a_state': self.button_a_state,
            'button_b_state': self.button_b_state
        }
