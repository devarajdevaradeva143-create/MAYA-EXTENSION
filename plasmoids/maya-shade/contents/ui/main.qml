import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: root
    width: 360
    height: 600

    property bool wifiOn: true
    property bool bluetoothOn: true
    property int brightness: 70
    property int volume: 50
    property bool darkMode: true

    Rectangle {
        anchors.fill: parent
        radius: 18
        color: Qt.rgba(1,1,1,0.06)
        border.width: 1
        border.color: Qt.rgba(1,1,1,0.18)

        // glass blur backdrop (compositor)
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12

            Text { text: "✦ Quick Settings"; color: "#FFFFFF"; font.bold: true; font.pixelSize: 18 }

            // toggles grid
            GridLayout {
                columns: 2
                rowSpacing: 8; columnSpacing: 8
                Layout.fillWidth: true

                Repeater {
                    model: [
                        { label: "Wi-Fi", on: root.wifiOn },
                        { label: "Bluetooth", on: root.bluetoothOn },
                        { label: "Dark mode", on: root.darkMode },
                        { label: "Maya glass", on: true }
                    ]
                    delegate: Rectangle {
                        Layout.fillWidth: true
                        height: 56
                        radius: 12
                        color: modelData.on ? Qt.rgba(255,122,184,0.25) : Qt.rgba(1,1,1,0.06)
                        border.width: 1
                        border.color: Qt.rgba(1,1,1,0.18)
                        Column {
                            anchors.centerIn: parent
                            Text { text: modelData.label; color: "#FFFFFF"; font.pixelSize: 12; font.bold: true }
                            Text { text: modelData.on ? "On" : "Off"; color: Qt.rgba(1,1,1,0.6); font.pixelSize: 10 }
                        }
                        MouseArea { anchors.fill: parent; onClicked: {} }
                    }
                }
            }

            // sliders
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                Text { text: "Brightness"; color: "#FFFFFF"; font.pixelSize: 12 }
                Slider { from: 0; to: 100; value: root.brightness; Layout.fillWidth: true; onMoved: root.brightness = value }
                Text { text: "Volume"; color: "#FFFFFF"; font.pixelSize: 12 }
                Slider { from: 0; to: 100; value: root.volume; Layout.fillWidth: true; onMoved: root.volume = value }
            }

            // Maya quick actions
            Text { text: "Maya quick actions"; color: Qt.rgba(1,1,1,0.6); font.pixelSize: 11 }
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                Button { text: "Glass toggle"; Layout.fillWidth: true }
                Button { text: "Screenshot"; Layout.fillWidth: true }
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                Button { text: "Do not disturb"; Layout.fillWidth: true }
                Button { text: "Settings"; Layout.fillWidth: true }
            }
        }
    }
}