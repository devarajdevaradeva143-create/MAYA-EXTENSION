import QtQuick
import QtQuick.Layouts

Item {
    id: root
    width: 600
    height: 56

    property var pinnedApps: ["firefox", "dolphin", "konsole", "code", "settings"]

    Rectangle {
        anchors.fill: parent
        radius: 18
        color: Qt.rgba(1,1,1,0.06)
        border.width: 1
        border.color: Qt.rgba(1,1,1,0.18)

        RowLayout {
            anchors.fill: parent
            anchors.margins: 8
            spacing: 6

            // search bar (left corner)
            Rectangle {
                Layout.preferredWidth: 180
                height: 36
                radius: 10
                color: Qt.rgba(1,1,1,0.08)
                border.width: 1
                border.color: Qt.rgba(1,1,1,0.18)
                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    Text { text: "🔍"; font.pixelSize: 14 }
                    Text { text: "Search…"; color: Qt.rgba(1,1,1,0.5); font.pixelSize: 12 }
                }
            }

            Item { Layout.fillWidth: true }

            // pinned apps (centered)
            Row {
                spacing: 4
                Layout.alignment: Qt.AlignHCenter
                Repeater {
                    model: root.pinnedApps
                    delegate: Rectangle {
                        width: 40; height: 40
                        radius: 10
                        color: mouse.containsMouse ? Qt.rgba(1,1,1,0.12) : "transparent"
                        Text {
                            anchors.centerIn: parent
                            text: "●"
                            color: "#FFFFFF"
                            font.pixelSize: 18
                        }
                        MouseArea { id: mouse; anchors.fill: parent; hoverEnabled: true }
                    }
                }
            }

            Item { Layout.fillWidth: true }

            // right side: settings, battery, date-time, notification
            Row {
                spacing: 8
                Text { text: "🔋"; font.pixelSize: 16; color: "#FFFFFF" }
                Text { text: "📶"; font.pixelSize: 16; color: "#FFFFFF" }
                Text { text: new Date().toLocaleTimeString(); color: "#FFFFFF"; font.pixelSize: 12 }
                Text { text: "🔔"; font.pixelSize: 16; color: "#FFFFFF" }
            }
        }
    }
}