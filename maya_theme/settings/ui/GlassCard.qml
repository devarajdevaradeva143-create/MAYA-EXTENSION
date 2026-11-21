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

    // 0.5px inner highlight (top edge)
    Rectangle {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 1
        color: Qt.rgba(1, 1, 1, 0.14)
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

    // noise grain overlay (2-3% grain, subtle)
    Rectangle {
        anchors.fill: parent
        radius: parent.radius
        opacity: 0.03
        // procedural noise: tile pattern of tiny dots
        Tile {
            id: noiseTile
            width: 4
            height: 4
            Rectangle { width: 1; height: 1; color: "#FFFFFF"; opacity: 0.5 }
            Rectangle { x: 2; y: 2; width: 1; height: 1; color: "#FFFFFF"; opacity: 0.3 }
        }
        // use Canvas for actual grain
        Canvas {
            anchors.fill: parent
            onPaint: {
                var ctx = getContext("2d");
                ctx.reset();
                ctx.fillStyle = Qt.rgba(1, 1, 1, 0.02);
                for (var i = 0; i < width; i += 3) {
                    for (var j = 0; j < height; j += 3) {
                        if ((i + j) % 2 === 0) {
                            ctx.fillRect(i, j, 1, 1);
                        }
                    }
                }
            }
        }
    }

    // soft shadow (rendered as outer glow via drop shadow effect)
    // Note: true box-shadow requires QtGraphicalEffects; kept as visual hint

    Item {
        id: content
        anchors.fill: parent
        anchors.margins: 16
    }
}