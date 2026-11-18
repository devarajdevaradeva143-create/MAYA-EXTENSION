import QtQuick
import QtQuick.Controls

Item {
    id: root
    property string label: ""
    property string icon: ""
    property bool active: false
    signal clicked()

    height: 44
    width: parent ? parent.width : 240

    Rectangle {
        anchors.fill: parent
        anchors.margins: 4
        radius: 10
        color: root.active ? Qt.rgba(1, 1, 1, 0.12) : (mouse.containsMouse ? Qt.rgba(1, 1, 1, 0.06) : "transparent")
        border.width: root.active ? 1 : 0
        border.color: Qt.rgba(1, 1, 1, 0.18)

        // left accent bar
        Rectangle {
            visible: root.active
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            width: 3
            height: 20
            radius: 2
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#FF7AB8" }
                GradientStop { position: 1.0; color: "#A855F7" }
            }
        }

        Row {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 14
            spacing: 10
            Text {
                text: root.icon
                font.pixelSize: 18
                color: root.active ? "#FF7AB8" : Qt.rgba(1, 1, 1, 0.7)
            }
            Text {
                text: root.label
                font.pixelSize: 14
                color: root.active ? "#FFFFFF" : Qt.rgba(1, 1, 1, 0.85)
                font.bold: root.active
            }
        }
    }

    MouseArea {
        id: mouse
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: root.clicked()
    }
}