#!/usr/bin/env python3

import cv2
import mediapipe as mp
import time
import multiprocessing
from playsound import playsound

max = lambda a, b: a if a > b else b
min = lambda a, b: a if a < b else b

def overlaps(r1, r2):
    xmin = max(r1.xmin, r2.xmin)
    ymin = max(r1.ymin, r2.ymin)
    xmax = min(r1.xmax, r2.xmax)
    ymax = min(r1.ymax, r2.ymax)

    return (max(0, xmax - xmin) * max(0, ymax - ymin)) > 0

class Rect:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def __str__(self):
        return f"{{xmin: {self.xmin}, ymin: {self.ymin}, xmax: {self.xmax}, ymax: {self.ymax}}}"

class Crisis:
    def play(self):
        while True:
            playsound("police.mp3", block=True)

    def toggle(self, active):
        if active:
            self.sound = multiprocessing.Process(target=self.play)
            self.sound.start()
        else:
            self.sound.terminate()

class BigBrother:
    def __init__(self):
        self.crisis = Crisis()
        self.cap = cv2.VideoCapture(0)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.mpFace = mp.solutions.face_mesh
        self.face = self.mpFace.FaceMesh()

        self.mpDraw = mp.solutions.drawing_utils

        self.pTime = 0
        self.cTime = 0
        self.isoverlapping = False

        self.faceRect = None
        self.handsRect = None

    def processface(self):
        xmin = self.w
        ymin = self.h
        xmax = 0
        ymax = 0

        for faceLms in self.faceResult.multi_face_landmarks:
            for i in range(0, 468):
                pt1 = faceLms.landmark[i]
                x = int(pt1.x * self.w)
                y = int(pt1.y * self.h)

                xmax = max(xmax, x)
                ymax = max(ymax, y)
                xmin = min(xmin, x)
                ymin = min(ymin, y)

                cv2.circle(self.img, (x, y), 5, (100, 100, 0), -1)

        self.faceRect = Rect(xmin, ymin, xmax, ymax)
        cv2.rectangle(self.img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    def processhands(self):
        xmin = self.w
        ymin = self.h
        xmax = 0
        ymax = 0

        for handLms in self.handsResult.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                x, y = int(lm.x * self.w), int(lm.y * self.h)
                cv2.circle(self.img, (x, y), 3, (255, 0, 255), cv2.FILLED)

                xmax = max(xmax, x)
                ymax = max(ymax, y)
                xmin = min(xmin, x)
                ymin = min(ymin, y)

            self.mpDraw.draw_landmarks(self.img, handLms, self.mpHands.HAND_CONNECTIONS)

        self.handsRect = Rect(xmin, ymin, xmax, ymax)
        cv2.rectangle(self.img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)

    def watch(self):
        while True:
            self.faceRect = None
            self.handsRect = None

            _, self.img = self.cap.read()
            imgRGB = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.handsResult = self.hands.process(imgRGB)
            self.faceResult = self.face.process(imgRGB)

            self.h, self.w, _ = self.img.shape

            if self.faceResult.multi_face_landmarks:
                self.processface()

            if self.handsResult.multi_hand_landmarks:
                self.processhands()

            if self.handsRect and self.faceRect:
                tmp = overlaps(self.handsRect, self.faceRect)
                if tmp != self.isoverlapping:
                    if tmp:
                        self.crisis.toggle(True)
                    else:
                        self.crisis.toggle(False)

                self.isoverlapping = tmp
            else:
                if self.isoverlapping:
                    self.crisis.toggle(False)
                    self.isoverlapping = False

            self.cTime = time.time()
            fps = 1 / (self.cTime - self.pTime)
            self.pTime = self.cTime

            cv2.putText(self.img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            cv2.imshow("The Big Brother", self.img)
            cv2.waitKey(1)

if __name__ == "__main__":
    bb = BigBrother()
    bb.watch()