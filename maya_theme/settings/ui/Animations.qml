import QtQuick

// Maya animation helpers — 3D flip-in popup (420ms) + success bounce
// Usage:
//   FlipIn { id: flip; target: myPopup }
//   SuccessBounce { id: bounce; target: myButton }

import QtQuick

QtObject {
    // ---- 3D flip-in popup (420ms, ease-out-cubic) ----
    // Apply to a popup/window's transform + opacity.
    // Call flipIn.start() to trigger.

    property var target: null

    // We expose two animations the caller can attach:
    //   on show: flipIn.restart()
    //   flipIn animates: rotationY 90 -> 0, opacity 0 -> 1, scale 0.9 -> 1

    NumberAnimation {
        id: flipRotY
        target: parent.target
        property: "rotationY"
        from: 90
        to: 0
        duration: 420
        easing.type: Easing.OutCubic
    }
    NumberAnimation {
        id: flipOpacity
        target: parent.target
        property: "opacity"
        from: 0
        to: 1
        duration: 420
        easing.type: Easing.OutCubic
    }
    NumberAnimation {
        id: flipScale
        target: parent.target
        property: "scale"
        from: 0.9
        to: 1.0
        duration: 420
        easing.type: Easing.OutCubic
    }

    // Sequential trigger helper (call this)
    function flipIn() {
        if (flipRotY.target) flipRotY.restart();
        if (flipOpacity.target) flipOpacity.restart();
        if (flipScale.target) flipScale.restart();
    }

    // ---- Success bounce (scale 1.0 -> 1.05 -> 1.0) ----
    SequentialAnimation {
        id: successBounce
        NumberAnimation { target: parent.target; property: "scale"; to: 1.05; duration: 120; easing.type: Easing.OutQuad }
        NumberAnimation { target: parent.target; property: "scale"; to: 1.0;  duration: 160; easing.type: Easing.InOutQuad }
    }

    // ---- Hover (120-150ms) ----
    // Caller sets hover state; this animates scale/color via Behavior.
    // Use as: Behavior on scale { PropertyAnimation { duration: 140; easing.type: Easing.OutQuad } }

    // ---- Toggle slide (200ms) ----
    // For Switch components: Behavior on x { PropertyAnimation { duration: 200 } }

    // ---- Page transition (fade + slide, 200ms) ----
    // Apply to content items on index change:
    //   on currentIndexChanged: pageTransition.restart()
    ParallelAnimation {
        id: pageTransition
        NumberAnimation { target: parent.target; property: "opacity"; from: 0; to: 1; duration: 200 }
        NumberAnimation { target: parent.target; property: "x"; from: (parent.target ? parent.target.x + 20 : 0); to: (parent.target ? parent.target.x : 0); duration: 200; easing.type: Easing.OutCubic }
    }

    // ---- Shimmer (loading) ----
    // Gradient shimmer for loading states — caller animates a highlight Rectangle.

    // ---- Reduced motion check ----
    // Respect prefers-reduced-motion: disable 3D flip.
    property bool reducedMotion: false
    function flipInSafe() {
        if (reducedMotion) {
            // just fade, no flip
            if (flipOpacity.target) flipOpacity.restart();
            return;
        }
        flipIn();
    }
}