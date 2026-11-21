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
    property bool glassEnabled: true

    // Maya quick actions — call into the theme via DBus/CLI
    // These would be wired to maya_theme via a DBus interface or
    // QProcess calling the CLI. For now, emit signals.

    signal glassToggle()
    signal screenshot()
    signal doNotDisturb()
    signal openSettings()
    signal voiceCommand(string cmd)

    Rectangle {
        anchors.fill: parent
        radius: 18
        color: Qt.rgba(1,1,1,0.06)
        border.width: 1
        border.color: Qt.rgba(1,1,1,0.18)

        // 0.5px inner highlight
        Rectangle {
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            height: 1
            color: Qt.rgba(1,1,1,0.14)
        }

        // top highlight gradient
        Rectangle {
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            height: parent.height * 0.35
            radius: parent.radius
            gradient: Gradient {
                GradientStop { position: 0.0; color: Qt.rgba(1, 1, 1, 0.14) }
                GradientStop { position: 1.0; color: "transparent" }
            }
        }

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
                        { label: "Wi-Fi", on: root.wifiOn, action: "wifi" },
                        { label: "Bluetooth", on: root.bluetoothOn, action: "bluetooth" },
                        { label: "Dark mode", on: root.darkMode, action: "dark" },
                        { label: "Maya glass", on: root.glassEnabled, action: "glass" }
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
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                if (modelData.action === "glass") {
                                    root.glassEnabled = !root.glassEnabled
                                    root.glassToggle()
                                } else if (modelData.action === "dark") {
                                    root.darkMode = !root.darkMode
                                    root.voiceCommand(root.darkMode ? "dark mode" : "light mode")
                                }
                            }
                        }
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
                Button {
                    text: "Glass toggle"
                    Layout.fillWidth: true
                    onClicked: { root.glassEnabled = !root.glassEnabled; root.glassToggle() }
                }
                Button {
                    text: "Screenshot"
                    Layout.fillWidth: true
                    onClicked: root.screenshot()
                }
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                Button {
                    text: "Do not disturb"
                    Layout.fillWidth: true
                    onClicked: root.doNotDisturb()
                }
                Button {
                    text: "Settings"
                    Layout.fillWidth: true
                    onClicked: root.openSettings()
                }
            }

            // voice input
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                TextField {
                    id: voiceInput
                    Layout.fillWidth: true
                    placeholderText: "Maya, dark mode..."
                    color: "#FFFFFF"
                    background: Rectangle {
                        color: Qt.rgba(1,1,1,0.06)
                        radius: 10
                        border.width: 1
                        border.color: Qt.rgba(1,1,1,0.18)
                    }
                    onAccepted: {
                        root.voiceCommand(text)
                        text = ""
                    }
                }
                Button {
                    text: "Send"
                    onClicked: {
                        root.voiceCommand(voiceInput.text)
                        voiceInput.text = ""
                    }
                }
            }
        }
    }
}