import QtQuick
import QtQuick.Layouts

Item {
    id: root
    width: 260
    height: 180

    property real cpu: 0
    property real ram: 0
    property real gpu: 0
    property real battery: 0

    Rectangle {
        anchors.fill: parent
        radius: 18
        color: Qt.rgba(1, 1, 1, 0.06)
        border.width: 1
        border.color: Qt.rgba(1, 1, 1, 0.18)

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 14
            spacing: 8

            Text { text: "✦ Maya Monitor"; color: "#FFFFFF"; font.bold: true; font.pixelSize: 14 }

            Repeater {
                model: [
                    { label: "CPU", value: root.cpu, color: "#FF7AB8" },
                    { label: "RAM", value: root.ram, color: "#A855F7" },
                    { label: "GPU", value: root.gpu, color: "#4ADE80" },
                    { label: "BAT", value: root.battery, color: "#FBBF24" }
                ]
                delegate: RowLayout {
                    Layout.fillWidth: true
                    Text { text: modelData.label; color: Qt.rgba(1,1,1,0.7); font.pixelSize: 11; width: 40 }
                    Rectangle {
                        Layout.fillWidth: true
                        height: 8
                        radius: 4
                        color: Qt.rgba(1,1,1,0.1)
                        Rectangle {
                            width: parent.width * (modelData.value / 100.0)
                            height: parent.height
                            radius: 4
                            color: modelData.color
                        }
                    }
                    Text { text: Math.round(modelData.value) + "%"; color: "#FFFFFF"; font.pixelSize: 11; width: 36; horizontalAlignment: Text.AlignRight }
                }
            }
        }
    }
}