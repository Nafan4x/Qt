import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, \
    QGridLayout, QFrame, QSizePolicy


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("My App")

        # Меню
        menubar = self.menuBar()
        menubar.addMenu('&File')
        menubar.addMenu('&Edit')
        menubar.addMenu('&View')
        menubar.addMenu('&Image')
        menubar.addMenu('&Options')
        menubar.addMenu('&Help')

        # Центральный виджет и основной layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # GridLayout для кнопок
        row = 12
        col = 2
        self.instr = QGridLayout()
        self.instr.setSpacing(2)
        self.instr.setContentsMargins(0, 10, 0, 80)

        # Устанавливаем размеры и политику размера для кнопок в GridLayout
        for row1 in range(row):
            for col1 in range(col):
                button = QPushButton(f'{row1}{col1}')
                button.setFixedSize(30, 30)
                button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                button.clicked.connect(lambda checked, i=f'{row1}{col1}': self.show_message(f'Вы нажали кнопку {i}'))
                self.instr.addWidget(button, row1, col1)
        main_layout.addLayout(self.instr)

        # Layout для Canvas и Color Palette
        second_layout = QVBoxLayout()

        # Canvas (Image Area)
        self.canvas_frame = QLabel(self)
        self.canvas_frame.setFrameShape(QFrame.Shape.Box)
        self.canvas_frame.setLineWidth(2)
        self.set_image("/mnt/data/image.png")
        self.canvas_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Добавляем canvas_frame в second_layout
        second_layout.addWidget(self.canvas_frame)

        # Palette
        self.color_palette = QGridLayout()
        self.color_palette.setSpacing(1)
        #color_palette.setContentsMargins(50, 0, 0, 0)
        colors = [
            "black", "gray", "maroon", "red", "orange", "yellow", "lime", "green",
            "teal", "cyan", "blue", "navy", "purple", "magenta", "white", "silver",
            "black", "gray", "maroon", "red", "orange", "yellow", "lime", "green",
            "teal", "cyan", "blue", "navy", "purple", "magenta", "white", "silver"
        ]
        row = 0
        col = 0

        for i, color in enumerate(colors):
            color_label = QPushButton()
            color_label.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            color_label.setFixedSize(30, 30)
            color_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            color_label.clicked.connect(lambda checked, i=color: self.show_message(f'Вы нажали кнопку {i}'))
            self.color_palette.addWidget(color_label, row, col)
            col += 1
            if i == 15:
                row = 1
                col = 0

        # Добавляем color_palette в second_layout
        second_layout.addLayout(self.color_palette)

        # Добавляем second_layout в основной layout
        main_layout.addLayout(second_layout)

    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.canvas_frame.setPixmap(pixmap.scaled(600, 400, Qt.AspectRatioMode.KeepAspectRatio))
        self.update_layout_margins(pixmap.size())

    def update_layout_margins(self, image_size):
        width, height = image_size.width(), image_size.height()

        # Пример изменения отступов в зависимости от размера изображения
        top_margin = max(10, height // 10)
        bottom_margin = max(80, height // 5)

        self.instr.setContentsMargins(0, top_margin, 0, bottom_margin)

    def show_message(self, message):
        # Действие при нажатии на кнопку
        print(message)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Получаем текущие размеры окна
        width = self.width()
        height = self.height()
        a = int(height/3.5)
        #b = int(width-290)
        #print(a, b)
        self.instr.setContentsMargins(0,10,0,a)
        self.instr.setContentsMargins(0,0,0,10)

        #print(f"Window resized to width={width}, height={height}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
