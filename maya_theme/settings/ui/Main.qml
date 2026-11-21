import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: win
    visible: true
    width: 1080
    height: 720
    minimumWidth: 400
    title: "✦ Maya Settings"
    color: "#0B0F19"

    property int currentIndex: 0
    property string searchText: ""
    // responsive: <768px → bottom tabs, single column (no sidebar)
    property bool compactMode: win.width < 768
    onWidthChanged: win.compactMode = win.width < 768

    // background gradient
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#0B0F19" }
            GradientStop { position: 1.0; color: "#131826" }
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // ---- Sidebar (hidden in compact mode) ----
        Rectangle {
            Layout.preferredWidth: 240
            Layout.fillHeight: true
            visible: !win.compactMode
            color: Qt.rgba(1, 1, 1, 0.04)
            border.width: 1
            border.color: Qt.rgba(1, 1, 1, 0.08)

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 4

                // logo
                Row {
                    spacing: 8
                    Layout.bottomMargin: 8
                    Text {
                        text: "✦"
                        font.pixelSize: 22
                        color: "#FF7AB8"
                    }
                    Column {
                        Text { text: "Maya AI"; font.pixelSize: 16; font.bold: true; color: "#FFFFFF" }
                        Text { text: "local only • your assistant"; font.pixelSize: 10; color: Qt.rgba(1,1,1,0.5) }
                    }
                }

                // search
                TextField {
                    id: searchField
                    Layout.fillWidth: true
                    placeholderText: "Search settings…"
                    color: "#FFFFFF"
                    background: Rectangle {
                        color: Qt.rgba(1,1,1,0.06)
                        radius: 10
                        border.width: 1
                        border.color: Qt.rgba(1,1,1,0.18)
                    }
                    onTextChanged: win.searchText = text
                }

                Item { height: 4 }

                // nav items
                SidebarItem { label: "Glass"; icon: "✦"; active: win.currentIndex === 0; onClicked: win.currentIndex = 0 }
                SidebarItem { label: "Theme"; icon: "🎨"; active: win.currentIndex === 1; onClicked: win.currentIndex = 1 }
                SidebarItem { label: "Scope"; icon: "🧩"; active: win.currentIndex === 2; onClicked: win.currentIndex = 2 }
                SidebarItem { label: "Performance"; icon: "⚡"; active: win.currentIndex === 3; onClicked: win.currentIndex = 3 }
                SidebarItem { label: "Monitor"; icon: "📊"; active: win.currentIndex === 4; onClicked: win.currentIndex = 4 }
                SidebarItem { label: "Wallpaper"; icon: "🖼"; active: win.currentIndex === 5; onClicked: win.currentIndex = 5 }
                SidebarItem { label: "Privacy"; icon: "🔒"; active: win.currentIndex === 6; onClicked: win.currentIndex = 6 }
                SidebarItem { label: "About"; icon: "ℹ"; active: win.currentIndex === 7; onClicked: win.currentIndex = 7 }

                Item { Layout.fillHeight: true }

                // version
                Text {
                    text: "v0.1.0"
                    font.pixelSize: 10
                    color: Qt.rgba(1,1,1,0.4)
                }
            }
        }

        // ---- Content ----
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            contentWidth: availableWidth

            ColumnLayout {
                width: parent.width - 40
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 16
                anchors.topMargin: 24
                anchors.bottomMargin: 24

                // Title
                Text {
                    text: ["Glass", "Theme", "Scope", "Performance", "Monitor", "Wallpaper", "Privacy", "About"][win.currentIndex]
                    font.pixelSize: 22
                    font.bold: true
                    color: "#FFFFFF"
                }
                Text {
                    text: "Adjust and apply instantly. Undo available."
                    font.pixelSize: 12
                    color: Qt.rgba(1,1,1,0.55)
                }

                // ---- Glass page ----
                ColumnLayout {
                    visible: win.currentIndex === 0
                    spacing: 16
                    Layout.fillWidth: true

                    GlassCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 260
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 12
                            Text { text: "Liquid Glass"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 16 }

                            RowLayout {
                                Text { text: "Enable glass"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.glassEnabled; onToggled: settings.glassEnabled = checked }
                            }
                            RowLayout {
                                Text { text: "Blur radius"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Slider {
                                    from: 0; to: 40; stepSize: 1
                                    value: settings.glassBlur
                                    onMoved: settings.glassBlur = value
                                    Layout.preferredWidth: 220
                                }
                                Text { text: settings.glassBlur + "px"; color: Qt.rgba(1,1,1,0.6); width: 40 }
                            }
                            RowLayout {
                                Text { text: "Transparency (dark)"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Slider {
                                    from: 0.4; to: 0.9; stepSize: 0.01
                                    value: settings.transpDark
                                    onMoved: settings.transpDark = value
                                    Layout.preferredWidth: 220
                                }
                                Text { text: Math.round(settings.transpDark*100) + "%"; color: Qt.rgba(1,1,1,0.6); width: 40 }
                            }
                            RowLayout {
                                Text { text: "Transparency (light)"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Slider {
                                    from: 0.2; to: 0.7; stepSize: 0.01
                                    value: settings.transpLight
                                    onMoved: settings.transpLight = value
                                    Layout.preferredWidth: 220
                                }
                                Text { text: Math.round(settings.transpLight*100) + "%"; color: Qt.rgba(1,1,1,0.6); width: 40 }
                            }
                        }
                    }

                    GlassCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 120
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 8
                            Text { text: "Live Preview"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 16 }
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 60
                                radius: 12
                                color: settings.themeMode === "dark"
                                       ? Qt.rgba(1,1,1,settings.transpDark)
                                       : Qt.rgba(1,1,1,settings.transpLight)
                                border.width: 1
                                border.color: Qt.rgba(1,1,1,0.18)
                                Text {
                                    anchors.centerIn: parent
                                    text: "Frosted glass card"
                                    color: settings.themeMode === "dark" ? "#FFFFFF" : "#1F2937"
                                }
                            }
                        }
                    }
                }

                // ---- Theme page ----
                ColumnLayout {
                    visible: win.currentIndex === 1
                    spacing: 16
                    Layout.fillWidth: true

                    GlassCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 220
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 12
                            Text { text: "Color & Mode"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 16 }

                            RowLayout {
                                Text { text: "Mode"; color: "#FFFFFF"; Layout.fillWidth: true }
                                ComboBox {
                                    model: ["dark", "light", "auto"]
                                    currentIndex: ["dark","light","auto"].indexOf(settings.themeMode)
                                    onActivated: settings.themeMode = model[currentIndex]
                                    Layout.preferredWidth: 160
                                }
                            }
                            RowLayout {
                                Text { text: "Accent start"; color: "#FFFFFF"; Layout.fillWidth: true }
                                TextField {
                                    text: settings.accentStart
                                    onEditingFinished: settings.accentStart = text
                                    Layout.preferredWidth: 160
                                    color: "#FFFFFF"
                                    background: Rectangle { color: Qt.rgba(1,1,1,0.06); radius: 8; border.width:1; border.color: Qt.rgba(1,1,1,0.18) }
                                }
                            }
                            RowLayout {
                                Text { text: "Accent end"; color: "#FFFFFF"; Layout.fillWidth: true }
                                TextField {
                                    text: settings.accentEnd
                                    onEditingFinished: settings.accentEnd = text
                                    Layout.preferredWidth: 160
                                    color: "#FFFFFF"
                                    background: Rectangle { color: Qt.rgba(1,1,1,0.06); radius: 8; border.width:1; border.color: Qt.rgba(1,1,1,0.18) }
                                }
                            }
                        }
                    }
                }

                // ---- Scope page ----
                ColumnLayout {
                    visible: win.currentIndex === 2
                    spacing: 16
                    Layout.fillWidth: true

                    GlassCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 300
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 8
                            Text { text: "Apply glass to"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 16 }

                            RowLayout {
                                Layout.fillWidth: true
                                Text { text: "KWin compositor (blur)"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.scopeKwin; onToggled: settings.scopeKwin = checked }
                            }
                            RowLayout {
                                Layout.fillWidth: true
                                Text { text: "Qt applications"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.scopeQt; onToggled: settings.scopeQt = checked }
                            }
                            RowLayout {
                                Layout.fillWidth: true
                                Text { text: "GTK applications"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.scopeGtk; onToggled: settings.scopeGtk = checked }
                            }
                            RowLayout {
                                Layout.fillWidth: true
                                Text { text: "Panels & taskbar"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.scopePanels; onToggled: settings.scopePanels = checked }
                            }
                            RowLayout {
                                Layout.fillWidth: true
                                Text { text: "Notifications"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.scopeNotifs; onToggled: settings.scopeNotifs = checked }
                            }
                        }
                    }
                }

                // ---- Performance page ----
                ColumnLayout {
                    visible: win.currentIndex === 3
                    spacing: 16
                    Layout.fillWidth: true

                    GlassCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 280
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 12
                            Text { text: "Performance"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 16 }

                            RowLayout {
                                Text { text: "Preset"; color: "#FFFFFF"; Layout.fillWidth: true }
                                ComboBox {
                                    model: ["quality", "balanced", "battery"]
                                    currentIndex: ["quality","balanced","battery"].indexOf(settings.perfPreset)
                                    onActivated: settings.perfPreset = model[currentIndex]
                                    Layout.preferredWidth: 160
                                }
                            }
                            RowLayout {
                                Text { text: "Auto-reduce blur on low battery"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.autoReduceBlur; onToggled: settings.autoReduceBlur = checked }
                            }

                            Item { height: 8 }

                            // Live usage display
                            Text { text: "Live usage"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 14 }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 16
                                Text { text: "CPU"; color: Qt.rgba(1,1,1,0.6); font.pixelSize: 11 }
                                Rectangle {
                                    Layout.fillWidth: true
                                    height: 8
                                    radius: 4
                                    color: Qt.rgba(1,1,1,0.1)
                                    Rectangle {
                                        width: parent.width * Math.min(1.0, settings.perfCpu / 100.0)
                                        height: parent.height
                                        radius: 4
                                        color: settings.perfCpu > 5 ? "#F87171" : "#4ADE80"
                                    }
                                }
                                Text { text: Math.round(settings.perfCpu) + "%"; color: "#FFFFFF"; font.pixelSize: 11; width: 40 }
                            }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 16
                                Text { text: "RAM"; color: Qt.rgba(1,1,1,0.6); font.pixelSize: 11 }
                                Rectangle {
                                    Layout.fillWidth: true
                                    height: 8
                                    radius: 4
                                    color: Qt.rgba(1,1,1,0.1)
                                    Rectangle {
                                        width: parent.width * Math.min(1.0, settings.perfRam / 150.0)
                                        height: parent.height
                                        radius: 4
                                        color: settings.perfRam > 120 ? "#FBBF24" : "#4ADE80"
                                    }
                                }
                                Text { text: Math.round(settings.perfRam) + "MB"; color: "#FFFFFF"; font.pixelSize: 11; width: 50 }
                            }
                            Text {
                                text: "Budget: CPU <2% · RAM <150MB. If exceeded for 30s, Maya suggests 'Balanced' mode."
                                color: Qt.rgba(1,1,1,0.5)
                                font.pixelSize: 10
                                wrapMode: Text.WordWrap
                                Layout.fillWidth: true
                            }
                        }
                    }
                }

                // ---- Monitor page ----
                ColumnLayout {
                    visible: win.currentIndex === 4
                    spacing: 16
                    Layout.fillWidth: true

                    GlassCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 200
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 12
                            Text { text: "System Monitor"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 16 }

                            RowLayout {
                                Text { text: "Enable monitor widget"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.monitorEnabled; onToggled: settings.monitorEnabled = checked }
                            }
                            RowLayout {
                                Text { text: "Update interval (s)"; color: "#FFFFFF"; Layout.fillWidth: true }
                                ComboBox {
                                    model: [1, 2, 5]
                                    currentIndex: [1,2,5].indexOf(settings.monitorInterval)
                                    onActivated: settings.monitorInterval = model[currentIndex]
                                    Layout.preferredWidth: 160
                                }
                            }
                        }
                    }
                }

                // ---- Wallpaper page ----
                ColumnLayout {
                    visible: win.currentIndex === 5
                    spacing: 16
                    Layout.fillWidth: true

                    GlassCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 280
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 10
                            Text { text: "Wallpaper"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 16 }

                            RowLayout {
                                Text { text: "Type"; color: "#FFFFFF"; Layout.fillWidth: true }
                                ComboBox {
                                    id: wpTypeCombo
                                    model: ["static", "animated", "slideshow"]
                                    currentIndex: ["static","animated","slideshow"].indexOf(settings.wallpaperType)
                                    onActivated: settings.wallpaperType = model[currentIndex]
                                    Layout.preferredWidth: 160
                                }
                            }
                            RowLayout {
                                Text { text: "Glass blur on wallpaper"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.wallpaperGlassBlur; onToggled: settings.wallpaperGlassBlur = checked }
                            }
                            RowLayout {
                                Text { text: "Parallax effect"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.wallpaperParallax; onToggled: settings.wallpaperParallax = checked }
                            }
                            RowLayout {
                                Text { text: "Auto light/dark switch"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.wallpaperAutoSwitch; onToggled: settings.wallpaperAutoSwitch = checked }
                            }
                            Item { height: 8 }
                            RowLayout {
                                spacing: 8
                                Button {
                                    text: "Set wallpaper…"
                                    onClicked: settings.pickWallpaper()
                                }
                                Button {
                                    text: "Next slideshow"
                                    onClicked: settings.nextWallpaper()
                                }
                                Button {
                                    text: "Generate themed pack"
                                    onClicked: settings.generateWallpaperPack()
                                }
                            }
                            Text {
                                text: "Supports static images, animated video wallpapers (mp4/webm), and Maya-themed SVG packs."
                                color: Qt.rgba(1,1,1,0.5)
                                font.pixelSize: 11
                                wrapMode: Text.WordWrap
                                Layout.fillWidth: true
                            }
                        }
                    }
                }

                // ---- Privacy page ----
                ColumnLayout {
                    visible: win.currentIndex === 6
                    spacing: 16
                    Layout.fillWidth: true

                    GlassCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 160
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 10
                            Text { text: "Privacy"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 16 }
                            RowLayout {
                                Text { text: "Update checks (opt-in)"; color: "#FFFFFF"; Layout.fillWidth: true }
                                Switch { checked: settings.updateChecks; onToggled: settings.updateChecks = checked }
                            }
                            Text { text: "No telemetry. No cloud calls by default. Logs stay local."; color: Qt.rgba(1,1,1,0.6); font.pixelSize: 11 }
                        }
                    }
                }

                // ---- About page ----
                ColumnLayout {
                    visible: win.currentIndex === 7
                    spacing: 16
                    Layout.fillWidth: true

                    GlassCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 260
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 8
                            Text { text: "✦ Maya Extension"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 20 }
                            Text { text: "v0.1.0 — premium liquid glass theme for Fedora KDE"; color: Qt.rgba(1,1,1,0.6); font.pixelSize: 12 }
                            Text { text: "Tagline: local only • your assistant"; color: Qt.rgba(1,1,1,0.6); font.pixelSize: 12 }
                            Item { height: 6 }
                            Button {
                                text: "Apply theme now"
                                onClicked: settings.applyTheme()
                                background: Rectangle {
                                    radius: 10
                                    gradient: Gradient {
                                        GradientStop { position: 0; color: "#FF7AB8" }
                                        GradientStop { position: 1; color: "#A855F7" }
                                    }
                                }
                                contentItem: Text { text: parent.text; color: "#FFFFFF"; font.bold: true; horizontalAlignment: Text.AlignHCenter }
                            }
                            Button {
                                text: "Create backup"
                                onClicked: settings.createBackup()
                            }
                            Button {
                                text: "Reset to defaults"
                                onClicked: settings.resetDefaults()
                            }
                        }
                    }

                    GlassCard {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 120
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 6
                            Text { text: "Compatibility"; font.bold: true; color: "#FFFFFF"; font.pixelSize: 16 }
                            Text {
                                text: settings.compatReport()
                                color: Qt.rgba(1,1,1,0.7)
                                font.pixelSize: 11
                                font.family: "monospace"
                                wrapMode: Text.WordWrap
                                Layout.fillWidth: true
                            }
                        }
                    }
                }

                Item { height: 20 }
            }
        }
    }

    // ---- Bottom tab bar (compact mode < 768px) ----
    Rectangle {
        visible: win.compactMode
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: 56
        color: Qt.rgba(1, 1, 1, 0.08)
        border.width: 1
        border.color: Qt.rgba(1, 1, 1, 0.18)
        z: 10

        RowLayout {
            anchors.fill: parent
            anchors.margins: 4
            spacing: 0

            Repeater {
                model: [
                    { label: "Glass", icon: "✦" },
                    { label: "Theme", icon: "🎨" },
                    { label: "Scope", icon: "🧩" },
                    { label: "Perf", icon: "⚡" },
                    { label: "Monitor", icon: "📊" },
                    { label: "Wall", icon: "🖼" },
                    { label: "Privacy", icon: "🔒" },
                    { label: "About", icon: "ℹ" }
                ]
                delegate: Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Column {
                        anchors.centerIn: parent
                        spacing: 2
                        Text {
                            text: modelData.icon
                            font.pixelSize: 18
                            color: win.currentIndex === index ? "#FF7AB8" : Qt.rgba(1,1,1,0.6)
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                        Text {
                            text: modelData.label
                            font.pixelSize: 9
                            color: win.currentIndex === index ? "#FFFFFF" : Qt.rgba(1,1,1,0.5)
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: win.currentIndex = index
                    }
                }
            }
        }
    }

    // ---- Status bar ----
    Rectangle {
        anchors.bottom: win.compactMode ? undefined : parent.bottom
        anchors.bottomMargin: win.compactMode ? 56 : 0
        anchors.left: parent.left
        anchors.right: parent.right
        height: 36
        color: Qt.rgba(0,0,0,0.35)
        RowLayout {
            anchors.fill: parent
            anchors.margins: 8
            Text { text: "Ready"; color: Qt.rgba(1,1,1,0.6); font.pixelSize: 11 }
            Item { Layout.fillWidth: true }
            Button {
                text: "Undo"
                onClicked: settings.undo()
            }
            Button {
                text: "Redo"
                onClicked: settings.redo()
            }
            Button {
                text: "Apply"
                onClicked: settings.applyTheme()
            }
            Button {
                text: "Export"
                onClicked: settings.exportConfig()
            }
        }
    }
}