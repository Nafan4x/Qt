import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: qsTr("My App")

    // Menu Bar
    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
        }
        Menu {
            title: qsTr("Edit")
        }
        Menu {
            title: qsTr("View")
        }
        Menu {
            title: qsTr("Image")
        }
        Menu {
            title: qsTr("Options")
        }
        Menu {
            title: qsTr("Help")
        }
    }

    // Horizontal Layout for buttons and canvas
    RowLayout {
        anchors.fill: parent
        anchors.margins: 10

        // Column for the left side buttons
        ColumnLayout {
            width: 60
            spacing: 5

            // A grid of buttons for the left side numbered 00, 01, ..., 111
            Repeater {
                model: 7
                ColumnLayout {
                    spacing: 5

                    Button {
                        text: qsTr("0%1").arg(index)
                    }
                    Button {
                        text: qsTr("%1%2").arg(index).arg(1)
                    }
                }
            }
        }

        // The canvas (middle part)
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "lightgrey"
            border.color: "black"
            border.width: 2
        }
    }
    
    

   
}
