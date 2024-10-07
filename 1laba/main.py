import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
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
        self.instr.setSpacing(0)
        #self.instr.setContentsMargins(0, 0, 0, 100)

        # Устанавливаем размеры и политику размера для кнопок в GridLayout
        for row1 in range(row):
            for col1 in range(col):
                button = QPushButton()
                button.setFixedSize(30, 30)
                button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                button.setIcon(QIcon('1860115.png'))
                button.clicked.connect(lambda checked, i=f'{row1}{col1}': self.show_message(f'Вы нажали кнопку {i}'))
                self.instr.addWidget(button, row1, col1)

        self.widget = QWidget()
        self.widget.setLayout(self.instr)
        self.widget.setFixedSize(80, 450)  # Размер окна зафиксирован

        tool_layout = QVBoxLayout()
        tool_layout.addWidget(self.widget)
        jb = QPushButton()
        jb.setFixedSize(80,50)
        jb.setStyleSheet(f"background-color: white; border: 1px solid black;")
        jb.clicked.connect(lambda checked, i=f'White': self.show_message(f'Вы нажали кнопку {i}'))
        jb1 = QPushButton()
        jb1.setFixedSize(80, 50)
        jb1.setStyleSheet(f"background-color: black; border: 1px solid black;")
        jb1.clicked.connect(lambda checked, i=f'Black': self.show_message(f'Вы нажали кнопку {i}'))

        tool_layout.addWidget(jb)
        tool_layout.addWidget(jb1)
        tool_widget = QWidget()
        tool_widget.setLayout(tool_layout)
        main_layout.addWidget(tool_widget)
        # Layout для Canvas и Color Palette
        second_layout = QVBoxLayout()

        # Canvas (Image Area)
        self.canvas_frame = QLabel(self)
        self.canvas_frame.setFrameShape(QFrame.Shape.Box)
        self.canvas_frame.setLineWidth(2)

        self.canvas_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Устанавливаем размеры
        self.canvas_frame.setMinimumSize(600, 400)
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

        color_widget = QWidget()
        color_widget.setLayout(self.color_palette)
        color_widget.setFixedSize(512,80)
        # Добавляем color_palette в second_layout
        second_layout.addWidget(color_widget)

        # Добавляем second_layout в основной layout
        main_layout.addLayout(second_layout)

    def set_image(self, image_path):
        """Устанавливает изображение и масштабирует его под размер canvas_frame."""
        pixmap = QPixmap(image_path)
        # Масштабируем изображение
        self.canvas_frame.setPixmap(pixmap.scaled(self.canvas_frame.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def resizeEvent(self, event):
        """Обрабатываем событие изменения размера."""
        if self.canvas_frame.pixmap():  # Проверяем, есть ли загруженное изображение
            self.canvas_frame.setPixmap(self.canvas_frame.pixmap().scaled(self.canvas_frame.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))


    def update_layout_margins(self, image_size):
        width, height = image_size.width(), image_size.height()

        # Пример изменения отступов в зависимости от размера изображения
        top_margin = max(10, height // 10)
        bottom_margin = max(80, height // 5)

        self.instr.setContentsMargins(0, top_margin, 0, bottom_margin)

    def show_message(self, message):
        # Действие при нажатии на кнопку
        print(message)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
