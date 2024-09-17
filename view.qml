import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: qsTr("My App")

    // Основной фон
    Rectangle {
        anchors.fill: parent
        color: "#37200d" // Цвет фона приложения
    }

    // Menu Bar
    menuBar: MenuBar {
        Menu {
            title: qsTr("Menu")
        }
        Menu {
            title: qsTr("Allies")
        }
        Menu {
            title: qsTr("Quests")
        }
        Menu {
            title: qsTr("Chat")
        }
        Menu {
            title: qsTr("Options")
        }
        Menu {
            title: qsTr("Help")
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10

        // Прямоугольник с фоновым изображением
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            border.color: "black"
            border.width: 2

            // Устанавливаем фоновое изображение
            Image {
                source: "main.png" // Укажите путь к изображению
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop // Режим масштабирования изображения
            }
        }

        RowLayout {
            spacing: 10
            Rectangle {
                color: "lightgrey"
                border.color: "black"
                border.width: 2
                width: 200
                height: 200
                Image {
                source: "minimap.png" // Укажите путь к изображению
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop // Режим масштабирования изображения
            }
            }
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.maximumHeight: 200
                color: "#4b280a"
                border.color: "black"
                border.width: 2
            }
            Rectangle {
                Layout.preferredWidth: 200
                Layout.preferredHeight: 200
                color: "#4b280a"
                border.color: "black"
                

                // Вложенный Item для поддержки GridLayout
                Item {
                    anchors.fill: parent // Item заполняет прямоугольник
                    anchors.leftMargin: 5
                    anchors.topMargin: 5

                    GridLayout {
                        
                        columns: 3 // 3 колонки
                        rows: 3    // 3 строки
                        

                        // Заполняем ячейки прямоугольниками
                        Repeater {
                            model: 9 // 9 элементов в сетке (3x3)

                            Rectangle {
                                width: 60
                                height: 60
                                Button {
                                    background: Rectangle {
                                         color: "#37200d" // Цвет фона
                                         radius: 10
                                    }
                                    width: 60
                                    height: 60
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
