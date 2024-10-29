import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QComboBox, QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt

# Путь к файлу данных
DATA_FILE = "components.json"


class ConfiguratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конфигурация компьютера")
        self.setGeometry(100, 100, 600, 400)

        self.components_data = self.load_data()
        self.selected_components = {}

        self.initUI()

    def load_data(self):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            # Данные по умолчанию, если файл не найден
            return {
                "categories": {
                    "CPU": [{"name": "Intel i5", "price": 200}, {"name": "AMD Ryzen 5", "price": 180}],
                    "GPU": [{"name": "NVIDIA GTX 1660", "price": 300}, {"name": "AMD RX 580", "price": 250}],
                    "RAM": [{"name": "8GB DDR4", "price": 50}, {"name": "16GB DDR4", "price": 90}],
                    "Storage": [{"name": "1TB HDD", "price": 40}, {"name": "512GB SSD", "price": 60}],
                    "PSU": [{"name": "500W", "price": 40}, {"name": "650W", "price": 60}]
                }
            }

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.components_data, file, indent=4)

    def initUI(self):
        layout = QVBoxLayout()

        # Поле для имени конфигурации
        self.config_name_input = QLineEdit(self)
        self.config_name_input.setPlaceholderText("Введите имя конфигурации")
        layout.addWidget(self.config_name_input)

        # Списки комплектующих
        self.combo_boxes = {}
        for category, items in self.components_data["categories"].items():
            hbox = QHBoxLayout()
            label = QLabel(f"{category}:")
            combo = QComboBox()
            combo.addItem("Не выбрано", 0)
            for item in items:
                combo.addItem(f"{item['name']} - ${item['price']}", item['price'])
            combo.currentIndexChanged.connect(self.update_total_price)
            self.combo_boxes[category] = combo
            hbox.addWidget(label)
            hbox.addWidget(combo)
            layout.addLayout(hbox)

        # Итоговая цена
        self.total_price_label = QLabel("Итоговая цена: $0")
        layout.addWidget(self.total_price_label)

        # Кнопки
        save_button = QPushButton("Сохранить конфигурацию")
        save_button.clicked.connect(self.save_configuration)
        load_button = QPushButton("Загрузить конфигурацию")
        load_button.clicked.connect(self.load_configuration)
        add_component_button = QPushButton("Добавить комплектующее")
        add_component_button.clicked.connect(self.open_add_component_dialog)

        layout.addWidget(save_button)
        layout.addWidget(load_button)
        layout.addWidget(add_component_button)

        # Основной виджет и центральный виджет
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def update_total_price(self):
        total_price = sum(
            combo.currentData() for combo in self.combo_boxes.values()
            if combo.currentData() is not None
        )
        self.total_price_label.setText(f"Итоговая цена: ${total_price}")

    def save_configuration(self):
        config_name = self.config_name_input.text()
        if not config_name:
            QMessageBox.warning(self, "Ошибка", "Введите имя конфигурации!")
            return

        config = {
            "name": config_name,
            "components": {cat: combo.currentText() for cat, combo in self.combo_boxes.items()},
            "total_price": sum(combo.currentData() for combo in self.combo_boxes.values())
        }

        save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить конфигурацию", "", "JSON Files (*.json)")
        if save_path:
            with open(save_path, "w") as file:
                json.dump(config, file, indent=4)
            QMessageBox.information(self, "Успех", "Конфигурация сохранена.")

    def load_configuration(self):
        load_path, _ = QFileDialog.getOpenFileName(self, "Загрузить конфигурацию", "", "JSON Files (*.json)")
        if load_path:
            with open(load_path, "r") as file:
                config = json.load(file)

            for category, combo in self.combo_boxes.items():
                for i in range(combo.count()):
                    if combo.itemText(i).startswith(config["components"].get(category, "")):
                        combo.setCurrentIndex(i)
                        break
            self.update_total_price()
            QMessageBox.information(self, "Успех", "Конфигурация загружена.")

    def open_add_component_dialog(self):
        # Открываем диалоговое окно добавления комплектующего
        dialog = AddComponentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            category, name, price = dialog.get_component_data()
            if category and name and price is not None:
                self.components_data["categories"][category].append({"name": name, "price": price})
                self.save_data()
                self.update_combo_boxes(category)

    def update_combo_boxes(self, category):
        # Обновляем выпадающий список для указанной категории
        combo = self.combo_boxes.get(category)
        combo.clear()
        combo.addItem("Не выбрано", 0)
        for item in self.components_data["categories"][category]:
            combo.addItem(f"{item['name']} - ${item['price']}", item['price'])
        self.update_total_price()


class AddComponentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить комплектующее")

        layout = QVBoxLayout()

        # Поле для выбора категории
        self.category_combo = QComboBox(self)
        self.category_combo.addItems(parent.components_data["categories"].keys())
        layout.addWidget(QLabel("Категория:"))
        layout.addWidget(self.category_combo)

        # Поле для ввода названия
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Название комплектующего")
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.name_input)

        # Поле для ввода цены
        self.price_input = QLineEdit(self)
        self.price_input.setPlaceholderText("Цена")
        layout.addWidget(QLabel("Цена:"))
        layout.addWidget(self.price_input)

        # Кнопки добавления и отмены
        button_box = QHBoxLayout()
        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(add_button)
        button_box.addWidget(cancel_button)

        layout.addLayout(button_box)
        self.setLayout(layout)

    def get_component_data(self):
        category = self.category_combo.currentText()
        name = self.name_input.text()
        try:
            price = float(self.price_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректное значение для цены.")
            return None, None, None
        return category, name, price


# Запуск приложения
app = QApplication(sys.argv)
window = ConfiguratorApp()
window.show()
sys.exit(app.exec())
