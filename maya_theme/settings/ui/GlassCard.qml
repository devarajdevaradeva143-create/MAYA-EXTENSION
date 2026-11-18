import QtQuick
import QtQuick.Controls

Rectangle {
    id: card
    property alias contentItem: content.data
    default property alias content: content.data

    color: Qt.rgba(1, 1, 1, 0.06)
    radius: 18
    border.width: 1
    border.color: Qt.rgba(1, 1, 1, 0.18)

    // top highlight
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

    Item {
        id: content
        anchors.fill: parent
        anchors.margins: 16
    }
}