import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# =========================
# CAMERA SETUP
# =========================

cap = cv2.VideoCapture(0)

detector = HandDetector(
    detectionCon=0.8,
    maxHands=1
)

success, img = cap.read()

if not success:
    print("Camera not found!")
    exit()

h, w, c = img.shape

# =========================
# DRAWING SETTINGS
# =========================

canvas = np.zeros((h, w, 3), np.uint8)

drawColor = (255, 0, 255)  # Purple

brushThickness = 5
toolbarVisible = False

xp, yp = 0, 0

# =========================
# MENU SETTINGS
# =========================



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

        distance = ((x - menuX) ** 2 + (y - menuY) ** 2) ** 0.5

        # Cursor
        cv2.circle(
            img,
            (x, y),
            12,
            drawColor,
            cv2.FILLED
        )

        # =========================
       
        # MENU MODE
        # =========================

        if fingers[1] == 1 and fingers[2] == 1:

            xp, yp = 0, 0

            cv2.putText(
                img,
                "MENU MODE",
                (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            # MENU BUTTON CLICK
            if abs(x - menuX) < 60 and abs(y - menuY) < 25:
                menuOpen = not menuOpen
                cv2.waitKey(300)

            # TOOL SELECTION
            if menuOpen:

                cv2.rectangle(
                img,
                (0, 80),
                (w, 130),
                (50, 50, 50),
                cv2.FILLED
            )

            # Purple
            cv2.circle(img, (120, 105), 18,
                    (255, 0, 255), cv2.FILLED)

            # Green
            cv2.circle(img, (190, 105), 18,
                    (0, 255, 0), cv2.FILLED)

            # Blue
            cv2.circle(img, (260, 105), 18,
                    (255, 0, 0), cv2.FILLED)

            # Gray
            cv2.circle(img, (330, 105), 18,
                    (120,120,120), cv2.FILLED)

            # Eraser
            cv2.circle(img, (400, 105), 18,
                    (255,255,255), cv2.FILLED)

            cv2.putText(
                img,
                "E",
                (393,112),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,0,0),
                2
            )

            # Clear
            cv2.circle(img, (470, 105), 18,
                    (0,0,255), cv2.FILLED)

            cv2.putText(
                img,
                "C",
                (463,112),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2
            )

        # =========================
        # DRAW MODE
        # =========================

        elif fingers == [0, 1, 0, 0, 0]:

            cv2.putText(
                img,
                "DRAW MODE",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            if xp == 0 and yp == 0:
                xp, yp = x, y

            cv2.line(
                canvas,
                (xp, yp),
                (x, y),
                drawColor,
                brushThickness
            )

            xp, yp = x, y

        else:
            xp, yp = 0, 0


    cv2.rectangle(
        img,
        (0, 0),
        (w, 80),
        (40, 40, 40),
        cv2.FILLED
    )
   # HEADER BAR

    cv2.rectangle(
        img,
        (0, 0),
        (w, 130),
        (35, 35, 35),
        cv2.FILLED
    )

    cv2.putText(
        img,
        "Gesture Canvas AI",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        2
    )

    # MENU BUTTON

    cv2.rectangle(
        img,
        (w - 100, 15),
        (w - 15, 65),
        (70,70,70),
        cv2.FILLED
    )

    buttonText = "CLOSE" if menuOpen else "MENU"

    cv2.putText(
        img,
        buttonText,
        (w - 92, 47),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )
    # =========================
    # MENU ITEMS
    # =========================

    if menuOpen:

        cv2.circle(img, (300, 40), 18, (255, 0, 255), cv2.FILLED)

        cv2.circle(img, (370, 40), 18, (0, 255, 0), cv2.FILLED)

        cv2.circle(img, (440, 40), 18, (255, 0, 0), cv2.FILLED)

        cv2.circle(img, (510, 40), 18, (120, 120, 120), cv2.FILLED)

        cv2.circle(img, (580, 40), 18, (255,255,255), cv2.FILLED)
        cv2.putText(img, "E", (573,47),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0,0,0), 2)

        cv2.circle(img, (650, 40), 18, (0,0,255), cv2.FILLED)
        cv2.putText(img, "C", (643,47),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255,255,255), 2)
        cv2.putText(img, "E", (454,47),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0,0,0), 2)

        cv2.circle(img, (520, 40), 18, (0,0,255), cv2.FILLED)
        cv2.putText(img, "C", (514,47),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255,255,255), 2)
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

    cv2.imshow(
        "Gesture Canvas AI",
        img
    )

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

