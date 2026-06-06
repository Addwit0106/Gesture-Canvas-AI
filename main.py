# .\venv\Scripts\Activate.ps1

import cv2
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector

# =========================
# CAMERA SETUP
# =========================

cap = cv2.VideoCapture(0)

detector = HandDetector(
    detectionCon=0.8,
    maxHands=1
)

# =========================
# DRAWING VARIABLES
# =========================

saveMessage = False
saveTime = 0

xp, yp = 0, 0

drawColor = (255, 0, 255)
toolName = "Purple" 

brushThickness = 5
brushName = "Small"
eraserThickness = 40

toolbarVisible = False

# Get camera size once
success, img = cap.read()

h, w, c = img.shape

# Create drawing canvas
canvas = np.zeros((h, w, 3), np.uint8)

# =========================
# UNDO
# =========================

previousCanvas = canvas.copy()

# =========================
# SAVE FOLDER
# =========================

if not os.path.exists("saved_drawings"):
    os.makedirs("saved_drawings")

saveCount = 1

# =========================
# MAIN LOOP
# =========================

while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    # =========================
    # HEADER
    # =========================

    cv2.rectangle(
        img,
        (0, 0),
        (w, 55),
        (35, 35, 35),
        cv2.FILLED
    )

    cv2.putText(
        img,
        "Virtual Canvas AI",
        (20, 38),
        cv2.FONT_HERSHEY_DUPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        img,
        f"Tool: {toolName}",
        (420, 38),
        cv2.FONT_HERSHEY_DUPLEX,
        0.6,
        (255, 255, 255),
        2
    )
    cv2.putText(
        img,
        f"Brush: {brushName}",
        (420, 18),
        cv2.FONT_HERSHEY_DUPLEX,
        0.45,
        (255, 255, 255),
        1
    )

    # =========================
    # TOOLBAR
    # =========================

    if toolbarVisible:

        cv2.rectangle(
            img,
            (0, 55),
            (w, 110),
            (55, 55, 55),
            cv2.FILLED
        )

        # Purple
        cv2.circle(img, (80, 82), 15,
                (255, 0, 255), cv2.FILLED)
        if toolName == "Purple":
            cv2.circle(img, (80, 82), 22, (255, 255, 255), 2)

        # Green
        cv2.circle(img, (140, 82), 15,
                (0, 255, 0), cv2.FILLED)
        if toolName == "Green":
                cv2.circle(img, (140, 82), 22, (255, 255, 255), 2)
        # Blue
        cv2.circle(img, (200, 82), 15,
                (255, 0, 0), cv2.FILLED)
        if toolName == "Blue":
            cv2.circle(img, (200, 82), 22, (255, 255, 255), 2)

        # Gray
        cv2.circle(img, (260, 82), 15,
                (120, 120, 120), cv2.FILLED)
        if toolName == "Gray":
                cv2.circle(img, (260, 82), 22, (255, 255, 255), 2)
        # Eraser
        cv2.circle(img, (320, 82), 15,
                (255, 255, 255), cv2.FILLED)
        if toolName == "Eraser":
            cv2.circle(img, (320, 82), 22, (0, 255, 255), 2)
        cv2.putText(
            img,
            "E",
            (314, 88),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            2
        )

        # Clear
        cv2.circle(img, (380, 82), 15,
                (0, 0, 255), cv2.FILLED)

        cv2.putText(
            img,
            "C",
            (374, 88),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2
        )

    # =========================
    # BRUSH TOOLBAR
    # =========================

    cv2.rectangle(
        img,
        (20, 150),
        (90, 350),
        (45, 45, 45),
        cv2.FILLED
    )

    # Small
    cv2.circle(
        img,
        (55, 190),
        5,
        (255, 255, 255),
        cv2.FILLED
    )

    # Medium
    cv2.circle(
        img,
        (55, 250),
        10,
        (255, 255, 255),
        cv2.FILLED
    )

    # Large
    cv2.circle(
        img,
        (55, 320),
        15,
        (255, 255, 255),
        cv2.FILLED
    )      
    # Selected Brush Highlight

    if brushName == "Small":
        cv2.circle(
            img,
            (55,190),
            18,
            (0, 255, 255),
            2
        )

    elif brushName == "Medium":
        cv2.circle(
            img,
            (55, 250),
            22,
            (0, 255, 255),
            2
        )

    elif brushName == "Large":
        cv2.circle(
            img,
            (55, 320),
            28,
            (0, 255, 255),
            2
        ) 

    # =========================
    # SAVE MESSAGE
    # =========================

    if saveMessage:

        cv2.putText(
            img,
            "Drawing Saved",
            (220, 40),
            cv2.FONT_HERSHEY_DUPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        elapsed = (
            cv2.getTickCount() - saveTime
        ) / cv2.getTickFrequency()

        if elapsed > 2:
            saveMessage = False
    # =========================
    # HAND DETECTION
    # =========================

    hands, img = detector.findHands(img)

    if hands:

        hand = hands[0]

        lmList = hand["lmList"]

        x, y, z = lmList[8]

        fingers = detector.fingersUp(hand)

        # =========================
        # TOOLBAR SHOW / HIDE
        # =========================

        if fingers == [0, 1, 1, 0, 0]:
            toolbarVisible = True

        elif fingers == [0, 0, 0, 0, 0]:
            toolbarVisible = False

        # =========================
        # TOOL SELECTION
        # =========================

        if toolbarVisible and fingers == [0, 1, 1, 0, 0]:

            # Purple
            if ((x - 80) ** 2 + (y - 82) ** 2) ** 0.5 < 20:
                drawColor = (255, 0, 255)
                toolName = "Purple"

            # Green
            elif ((x - 140) ** 2 + (y - 82) ** 2) ** 0.5 < 20:
                drawColor = (0, 255, 0)
                toolName = "Green"

            # Blue
            elif ((x - 200) ** 2 + (y - 82) ** 2) ** 0.5 < 20:
                drawColor = (255, 0, 0)
                toolName = "Blue"

            # Gray
            elif ((x - 260) ** 2 + (y - 82) ** 2) ** 0.5 < 20:
                drawColor = (120, 120, 120)
                toolName = "Gray"

            # Eraser
            elif ((x - 320) ** 2 + (y - 82) ** 2) ** 0.5 < 20:
                drawColor = (0, 0, 0)
                toolName = "Eraser"

            # Clear Canvas
            elif ((x - 380) ** 2 + (y - 82) ** 2) ** 0.5 < 20:
                canvas = np.zeros((h, w, 3), np.uint8)
        # =========================
        # BRUSH SELECTION
        # =========================

        if fingers == [0, 1, 1, 0, 0]:

            # Small
            if ((x - 55) ** 2 + (y - 190) ** 2) ** 0.5 < 40:
                brushThickness = 5
                brushName = "Small"

            # Medium
            elif ((x - 55) ** 2 + (y - 250) ** 2) ** 0.5 < 40:
                brushThickness = 10
                brushName = "Medium"

            # Large
            elif ((x - 55) ** 2 + (y - 320) ** 2) ** 0.5 < 40:
                brushThickness = 20
                brushName = "Large"
        # =========================
        # CURSOR
        # =========================

        cv2.circle(
            img,
            (x, y),
            16,
            (255, 255, 255),
            2
        )

        cv2.circle(
            img,
            (x, y),
            12,
            drawColor,
            cv2.FILLED
        )

        # =========================
        # DRAW MODE
        # =========================

        if fingers == [0, 1, 0, 0, 0]:

            if xp == 0 and yp == 0:

                # Save state before drawing
                previousCanvas = canvas.copy()
                xp, yp = x, y

            thickness = brushThickness

            if toolName == "Eraser":
                thickness = eraserThickness

            cv2.line(
                canvas,
                (xp, yp),
                (x, y),
                drawColor,
                thickness
            )

            xp, yp = x, y

        # =========================
        # PALM ERASER
        # =========================

        elif fingers == [1, 1, 1, 1, 1]:

            cv2.putText(
                img,
                "ERASING",
                (250, 40),
                cv2.FONT_HERSHEY_DUPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            cv2.circle(
                canvas,
                (x, y),
                30,
                (0, 0, 0),
                cv2.FILLED
            )

            xp, yp = 0, 0

        else:

            xp, yp = 0, 0
    # =========================
    # MERGE CANVAS
    # =========================

    img = cv2.addWeighted(
        img,
        1,
        canvas,
        1,
        0
    )

    # =========================
    # DISPLAY
    # =========================

    cv2.imshow(
        "Virtual Canvas AI",
        img
    )

    key = cv2.waitKey(1) & 0xFF

    # Quit
    if key == ord("q"):
        break
    
    elif key == ord("u"):

        canvas = previousCanvas.copy()

        print("Undo Successful")
    
    # Save
    elif key == ord("s"):

        filename = f"saved_drawings/drawing_{saveCount}.png"

        cv2.imwrite(
            filename,
            canvas
        )

        print(f"Saved: {filename}")

        saveMessage = True
        saveTime = cv2.getTickCount()

        saveCount += 1
# =========================
# CLEANUP
# =========================

cap.release()
cv2.destroyAllWindows()