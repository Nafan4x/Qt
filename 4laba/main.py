from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QListView
import random
import sys

class Request:
    def __init__(self, start_floor, target_floor, time_created):
        self.start_floor = start_floor
        self.target_floor = target_floor
        self.time_created = time_created
        self.elevator_id = None  # Присваивается, когда запрос обрабатывается лифтом

class Elevator(QObject):
    def __init__(self, elevator_id, max_floor, capacity=5):
        super().__init__()
        self.elevator_id = elevator_id
        self.current_floor = 0
        self.direction = 0  # 1 - вверх, -1 - вниз, 0 - на месте
        self.capacity = capacity
        self.requests = []
        self.completed_requests = []

    def add_request(self, request):
        if len(self.requests) < self.capacity:
            self.requests.append(request)
            request.elevator_id = self.elevator_id
            return True
        return False

    def move(self):
        if not self.requests:
            self.direction = 0
            return

        # Определяем направление движения
        self.direction = 1 if self.current_floor < self.requests[0].target_floor else -1
        self.current_floor += self.direction

        # Проверяем, есть ли запрос на текущем этаже
        for request in list(self.requests):
            if request.target_floor == self.current_floor:
                self.requests.remove(request)
                self.completed_requests.append(request)

        # Меняем направление, если все запросы в текущем направлении выполнены
        if not any(req.target_floor > self.current_floor for req in self.requests):
            self.direction = -1
        elif not any(req.target_floor < self.current_floor for req in self.requests):
            self.direction = 1


class ElevatorSystem(QObject):
    def __init__(self, num_elevators, num_floors, request_probability):
        super().__init__()
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]
        self.num_floors = num_floors
        self.request_probability = request_probability
        self.active_requests = []
        self.completed_requests = []

    def generate_request(self, current_time):
        if random.random() < self.request_probability:
            start_floor = random.randint(0, self.num_floors - 1)
            target_floor = random.randint(0, self.num_floors - 1)
            if start_floor != target_floor:
                new_request = Request(start_floor, target_floor, current_time)
                self.assign_request(new_request)

    def assign_request(self, request):
        # Найти ближайший доступный лифт для запроса
        closest_elevator = min(self.elevators, key=lambda el: abs(el.current_floor - request.start_floor))
        if closest_elevator.add_request(request):
            self.active_requests.append(request)

    def update(self):
        for elevator in self.elevators:
            elevator.move()
            for req in elevator.completed_requests:
                if req in self.active_requests:
                    self.active_requests.remove(req)
                    self.completed_requests.append(req)

class ElevatorRequestModel(QAbstractListModel):
    def __init__(self, requests):
        super().__init__()
        self.requests = requests

    def rowCount(self, parent=QModelIndex()):
        return len(self.requests)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            request = self.requests[index.row()]
            return f"Запрос с {request.start_floor} на {request.target_floor}, Лифт: {request.elevator_id}"

class ElevatorSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Симуляция Лифтовой Системы")
        self.system = ElevatorSystem(num_elevators=3, num_floors=10, request_probability=0.3)

        layout = QVBoxLayout()
        self.requests_view = QListView()
        self.requests_model = ElevatorRequestModel(self.system.active_requests)
        self.requests_view.setModel(self.requests_model)

        layout.addWidget(QLabel("Активные Запросы:"))
        layout.addWidget(self.requests_view)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system)
        self.timer.start(1000)  # Обновление каждую секунду

    def update_system(self):
        current_time = self.timer.remainingTime()
        self.system.generate_request(current_time)
        self.system.update()
        self.requests_model.layoutChanged.emit()  # Обновление отображения

if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulator = ElevatorSimulator()
    simulator.show()
    sys.exit(app.exec())
