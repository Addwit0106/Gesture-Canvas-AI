import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# =========================
# SETTINGS
# =========================

menuOpen = False

menuX = 550
menuY = 50

drawColor = (255, 0, 255)
brushThickness = 5
eraserThickness = 35
toolName = "Purple"

# =========================
# CAMERA
# =========================

cap = cv2.VideoCapture(0)

detector = HandDetector(
    detectionCon=0.8,
    maxHands=1
)

success, img = cap.read()

h, w, c = img.shape

canvas = np.zeros((h, w, 3), np.uint8)

xp, yp = 0, 0

# =========================
# MAIN LOOP
# =========================

while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    if hands:

        hand = hands[0]

        lmList = hand["lmList"]

        x, y, z = lmList[8]

        fingers = detector.fingersUp(hand)

        # Cursor
        cv2.circle(img, (x, y), 18, (255, 255, 255), 2)
        cv2.circle(img, (x, y), 15, drawColor, cv2.FILLED)

        # =========================
        # DRAW MODE
        # =========================

        if fingers == [0, 1, 0, 0, 0]:

            cv2.putText(
                img,
                "DRAW MODE",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            if xp == 0 and yp == 0:
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
        # SELECTION MODE
        # =========================

        distance = ((x - menuX) ** 2 + (y - menuY) ** 2) ** 0.5

        if distance < 30:
            menuOpen = not menuOpen

        elif fingers[1] == 1 and fingers[2] == 1:

            cv2.putText(
                img,
                "SELECT MODE",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            xp, yp = 0, 0

            if y < 80:

                # Purple
                if 25 < x < 75:
                    drawColor = (255, 0, 255)
                    toolName = "Purple"

                # Green
                elif 95 < x < 145:
                    drawColor = (0, 255, 0)
                    toolName = "Green"

                # Blue
                elif 165 < x < 215:
                    drawColor = (255, 0, 0)
                    toolName = "Blue"

               # Gray
                elif 235 < x < 285:
                    drawColor = (100,100,100)
                    toolName = "Gray"
                # Eraser
                elif 305 < x < 355:
                    drawColor = (0, 0, 0)
                    toolName = "Eraser"

                # Clear Canvas
                elif 375 < x < 425:
                    canvas = np.zeros((h, w, 3), np.uint8)

        else:
            xp, yp = 0, 0

    # =========================
    # TOOLBAR
    # =========================

    # Floating Menu Button
    if menuOpen:

        cv2.circle(img, (menuX - 70, menuY), 20,
               (255,0,255), cv2.FILLED)

        cv2.circle(img, (menuX - 140, menuY), 20,
               (0,255,0), cv2.FILLED)

        cv2.circle(img, (menuX - 210, menuY), 20,
               (255,0,0), cv2.FILLED)
        cv2.circle(
            img,
            (menuX, menuY),
            30,
            (50, 50, 50),
            cv2.FILLED
    )

    cv2.putText(
        img,
        "+",
        (menuX - 10, menuY + 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        3
    )

    # =========================
    # SELECTED TOOL HIGHLIGHT
    # =========================

    # Floating Menu Button
    cv2.circle(
        img,
        (menuX, menuY),
        30,
        (50, 50, 50),
        cv2.FILLED
    )

    cv2.putText(
        img,
        "+",
        (menuX - 10, menuY + 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        3
    )

    # =========================
    # TOOL NAME
    # =========================

    cv2.putText(
        img,
        f"Tool: {toolName}",
        (470, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # =========================
    # MERGE CANVAS
    # =========================

    img = cv2.addWeighted(img, 1, canvas, 1, 0)

    cv2.imshow("Virtual Canvas", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()