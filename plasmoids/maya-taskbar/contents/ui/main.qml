import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: root
    width: 600
    height: 56

    property var pinnedApps: [
        { name: "firefox", icon: "🌐", running: false },
        { name: "dolphin", icon: "📁", running: false },
        { name: "konsole", icon: "⌨", running: true },
        { name: "code", icon: "💻", running: false },
        { name: "settings", icon: "⚙", running: false }
    ]
    property real iconSize: 40
    property bool showRunningIndicator: true
    property bool enableGrouping: true
    property bool enableHover: true

    signal appLaunch(string name)
    signal appFocus(string name)
    signal searchActivated()

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
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.searchActivated()
                }
            }

            Item { Layout.fillWidth: true }

            // pinned apps (centered)
            Row {
                spacing: 4
                Layout.alignment: Qt.AlignHCenter

                Repeater {
                    model: root.pinnedApps
                    delegate: Item {
                        width: root.iconSize
                        height: root.iconSize + (root.showRunningIndicator ? 4 : 0)

                        Rectangle {
                            id: appIcon
                            anchors.top: parent.top
                            anchors.horizontalCenter: parent.horizontalCenter
                            width: root.iconSize
                            height: root.iconSize
                            radius: 10
                            color: {
                                if (!root.enableHover) return "transparent"
                                if (mouse.containsMouse) return Qt.rgba(1,1,1,0.12)
                                return "transparent"
                            }
                            border.width: modelData.running && root.showRunningIndicator ? 1 : 0
                            border.color: Qt.rgba(255,122,184,0.6)

                            Text {
                                anchors.centerIn: parent
                                text: modelData.icon
                                font.pixelSize: 18
                            }

                            // hover scale effect
                            scale: mouse.containsMouse && root.enableHover ? 1.1 : 1.0
                            Behavior on scale {
                                PropertyAnimation { duration: 140; easing.type: Easing.OutQuad }
                            }
                        }

                        // running app indicator (bottom dot)
                        Rectangle {
                            visible: modelData.running && root.showRunningIndicator
                            anchors.top: appIcon.bottom
                            anchors.horizontalCenter: parent.horizontalCenter
                            width: 6
                            height: 3
                            radius: 1.5
                            color: "#FF7AB8"
                        }

                        MouseArea {
                            id: mouse
                            anchors.fill: parent
                            hoverEnabled: root.enableHover
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                if (modelData.running) {
                                    root.appFocus(modelData.name)
                                } else {
                                    root.appLaunch(modelData.name)
                                }
                            }
                        }
                    }
                }
            }

            Item { Layout.fillWidth: true }

            // right side: settings, battery, date-time, notification
            Row {
                spacing: 8
                Text { text: "🔋"; font.pixelSize: 16; color: "#FFFFFF" }
                Text { text: "📶"; font.pixelSize: 16; color: "#FFFFFF" }
                Text {
                    text: new Date().toLocaleTimeString(Qt.localeSystem(), "hh:mm")
                    color: "#FFFFFF"
                    font.pixelSize: 12
                }
                Text { text: "🔔"; font.pixelSize: 16; color: "#FFFFFF" }
            }
        }
    }
}