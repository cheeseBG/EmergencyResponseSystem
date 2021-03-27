# -*- coding: utf-8 -*-

import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import cv2
import mediapipe as mp
import re
import _init_paths

from gesture import define_gesture, find_gesture, handedness
from selenium import webdriver
from SR_edsr import sr_work
import time



import threading

from socket import *

# Create Socket
clientSock = socket(AF_INET, SOCK_STREAM)
url = '192.168.43.145'
clientSock.connect((url, 2000))

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

## ==> SPLASH SCREEN
from ui_splash_screen import Ui_SplashScreen
## ==> MAIN WINDOW
from ui_main import Ui_MainWindow

## ==> GLOBALS
counter = 0
hands = None
cap_hand = None
cap_situ = None
right_prev = None
left_prev = None
left_count = 0

#Camera Command
camera_left = 0
camera_right = 0
camera_center = 0


# YOUR APPLICATION
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.logic_btn = False
        # self.logic_dr = False

        self.case = 0

        # 버튼을 누르면 함수 실행
        self.ui.pushButton.clicked.connect(self.btnClicked)
        # self.ui.pushButton_2.clicked.connect(self.drClicked)

        # set warning
        self.ui.warning.setVisible(False)
        # self.ui.warning.setVisible(False)

        # set wait
        self.ui.wait.setVisible(False)


    def start(self):
        global cap_hand
        global cap_situ
        global hands
        global right_prev
        global left_prev
        global left_count
        global camera_center
        global camera_left
        global camera_right
        turn_on_esp = 0

        while cap_hand.isOpened():
            success, image = cap_hand.read()
            success2, image2 = cap_situ.read()

            if not success:
                break
            if not success2:
                break

            if success:
                if turn_on_esp == 0:
                    esp_trd = threading.Thread(target=esp32_video, name="[Daemon2]", args=())
                    esp_trd.setDaemon(True)
                    esp_trd.start()
                    turn_on_esp += 1


                # Resize Image
                image = cv2.resize(image, dsize=(800, 600))
                # Flip the image horizontally for a later selfie-view display, and convert
                # the BGR image to RGB.
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                landmark = []
                landmark_list = []
                cnt = 0
                cnt2 = 0

                # Count number of loop when left hand gesture is not used
                left_count += 1

                # Interpret Hand Gesture & Control RC Car
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        for i in str(hand_landmarks).split():
                            is_num = bool(re.findall('\d+', i))
                            # Extract landmarks
                            if is_num is True:
                                if cnt < 3 and cnt2 == 0:
                                    landmark.append(float(i))
                                    cnt += 1
                                elif cnt == 3 and cnt2 == 0:
                                    cnt2 = 1
                                elif cnt == 3 and cnt2 == 1:
                                    cnt = 0
                                    cnt2 = 0
                            if len(landmark) == 3:
                                landmark_list.append(landmark)
                                landmark = []

                        # Right Hand Gesture Controls
                        if find_gesture(define_gesture(landmark_list),
                                        handedness(landmark_list[0], landmark_list[1])) != "None" and\
                                handedness(landmark_list[0], landmark_list[1]) == 'right':
                            cmd = find_gesture(define_gesture(landmark_list),
                                               handedness(landmark_list[0], landmark_list[1]))
                            if right_prev != cmd:
                                right_prev = cmd

                                # Create Thread
                                t = threading.Thread(target=url_command_right, name="[Daemon]", args=(cmd,))
                                t.setDaemon(True)
                                t.start()

                        # Left Hand Gesture Controls
                        if find_gesture(define_gesture(landmark_list),
                                        handedness(landmark_list[0], landmark_list[1])) != "None" and\
                                handedness(landmark_list[0], landmark_list[1]) == 'left':
                            cmd = find_gesture(define_gesture(landmark_list),
                                               handedness(landmark_list[0], landmark_list[1]))
                            # Camera Command
                            if cmd == "Camera_LEFT" or cmd == "Camera_RIGHT" or cmd == "Camera_CENTER":
                                if cmd == "Camera_LEFT" and camera_left == 0:
                                    left_prev = cmd
                                    left_count = 0
                                    camera_left = 1
                                    camera_right = 0
                                    camera_center = 0

                                    # Create Thread
                                    t = threading.Thread(target=url_command_left, name="[Daemon5]", args=(cmd,))
                                    t.setDaemon(True)
                                    t.start()

                                elif cmd == "Camera_RIGHT" and camera_right == 0:
                                    left_prev = cmd
                                    left_count = 0
                                    camera_left = 0
                                    camera_right = 1
                                    camera_center = 0

                                    # Create Thread
                                    t = threading.Thread(target=url_command_left, name="[Daemon6]", args=(cmd,))
                                    t.setDaemon(True)
                                    t.start()

                                elif cmd == "Camera_CENTER" and camera_center == 0:
                                    left_prev = cmd
                                    left_count = 0
                                    camera_left = 0
                                    camera_right = 0
                                    camera_center = 1

                                    # Create Thread
                                    t = threading.Thread(target=url_command_left, name="[Daemon7]", args=(cmd,))
                                    t.setDaemon(True)
                                    t.start()



                            if cmd == "Capture" and left_count > 3:
                                left_prev = cmd
                                left_count = 0

                                img_name = 'image/input.png'
                                cv2.imwrite(img_name, image2)

                            # SR Command
                            if left_prev != cmd and (cmd != "Camera_LEFT" or cmd != "Camera_RIGHT" or cmd != "Capture"):
                                left_prev = cmd

                                if cmd == "Work SR Engine":
                                    t = threading.Thread(target=sr_work, name="[Daemon4]", args=())
                                    t.setDaemon(True)
                                    t.start()
                                    self.ui.wait.setVisible(True)

                                if cmd == "SR Done":
                                    self.ui.wait.setVisible(False)


                        print(find_gesture(define_gesture(landmark_list),
                                           handedness(landmark_list[0], landmark_list[1])))
                        print(handedness(landmark_list[0], landmark_list[1]))

                        self.ui.cmd.setText(f"{find_gesture(define_gesture(landmark_list), handedness(landmark_list[0], landmark_list[1]))}\n"
                                              f"{handedness(landmark_list[0], landmark_list[1])}")
                        self.ui.cmd.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        self.ui.cmd.repaint()
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                self.displayHandSign(image)
                self.displayCCTV(image2)
                #self.displayRCCAR(image2)
                self.displayCaptureImg()
                self.displaySRImg()

                #Keyboard
                k = cv2.waitKey(0)
                if k % 256 == 27:
                    # esc pressed --> break
                    break
                elif k % 256 == 32:
                    # space pressed --> capture
                    img_name = '../../image/input.png'
                    cv2.imwrite(img_name, image)

        hands.close()
        cap_hand.release()
        cap_situ.release()
        cv2.destroyAllWindows()

    def btnClicked(self):
        if self.logic_btn == True:
            self.logic_btn = False
            # self.ui.rccarCam.setPixmap(None)
            self.case += 1
            self.ui.lcdNumber.display(self.case)
            self.ui.warning.setVisible(False)
            # self.ui.wait.setVisible(False)
            # space pressed --> capture
        else:
            self.logic_btn = True
            self.ui.warning.setVisible(True)
            # self.ui.wait.setVisible(True)

    def displayHandSign(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()

        w = self.ui.handSign.width()
        h = self.ui.handSign.height()

        self.ui.handSign.setPixmap(QPixmap.fromImage(img).scaled(w, h, Qt.KeepAspectRatioByExpanding))
        # self.ui.handSign.setPixmap(QPixmap.fromImage(img))
        # 가운데 맞춤
        self.ui.handSign.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def displayRCCAR(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()

        w = self.ui.handSign.width()
        h = self.ui.handSign.height()

        self.ui.cctv.setPixmap(QPixmap.fromImage(img).scaled(w, h, Qt.KeepAspectRatioByExpanding))
        # self.ui.cctv.setPixmap(QPixmap.fromImage(img))
        # 가운데 맞춤
        self.ui.cctv.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        # self.ui.situation2.setPixmap(QPixmap.fromImage(img))
        # # 가운데 맞춤
        # self.ui.situation2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def displayCCTV(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()

        w = self.ui.handSign.width()
        h = self.ui.handSign.height()

        self.ui.rccarCam.setPixmap(QPixmap.fromImage(img).scaled(w, h, Qt.KeepAspectRatioByExpanding))
        # self.ui.rccarCam.setPixmap(QPixmap.fromImage(img))
        # 가운데 맞춤
        self.ui.rccarCam.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def displayCaptureImg(self):
        img = QPixmap.fromImage('../../image/input.png')
        w = self.ui.cap_img.width()
        h = self.ui.cap_img.height()
        self.ui.cap_img.setPixmap(img.scaled(w, h, Qt.KeepAspectRatioByExpanding))
        # 가운데 맞춤
        self.ui.cap_img.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def displaySRImg(self):
        img = QPixmap.fromImage('../../image/upscaled.png')
        w = self.ui.sr_img.width()
        h = self.ui.sr_img.height()
        self.ui.sr_img.setPixmap(img.scaled(w, h, Qt.KeepAspectRatioByExpanding))
        # 가운데 맞춤
        self.ui.sr_img.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)




# SPLASH SCREEN
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        ## REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # # Change Texts
        # QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        # QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))

        ## SHOW ==> MAIN WINDOW
        self.show()

    ## ==> APP FUNCTIONS
    def progress(self):

        global counter
        global hands
        global cap_hand
        global cap_situ

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        if hands is None:
            self.ui.label_loading.setText("load mediapipe...")
            self.ui.label_loading.repaint()
            hands = mp_hands.Hands(
                min_detection_confidence=0.7, min_tracking_confidence=0.5)
            cap_hand = cv2.VideoCapture(0)
            cap_situ = cv2.VideoCapture(1)
            counter = 20
            self.ui.label_loading.setText("loading...")

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = MainWindow()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

            # START MAIN SCREEN
            self.main.start()

        # INCREASE COUNTER
        counter += 4


def url_command_right(cmd):
    try:
        clientSock.send(cmd.encode('utf-8'))
    except:
        print("\n\n\n\nException Occur\n\n\n\n")


def url_command_left(cmd):
    try:
        clientSock.send(cmd.encode('utf-8'))
        time.sleep(10)
    except:
        print("\n\n\n\nException Occur\n\n\n\n")


def esp32_video():
    # change to your ESP32-CAM ip
    wd = webdriver.Chrome(r'C:\Users\jji44\Desktop\chromedriver.exe')
    url = 'http://192.168.43.159:81/stream'

    wd.set_window_size(400, 400)
    #wd.set
    wd.get(url)
    # url = "http://192.168.0.152:81/stream"
    # CAMERA_BUFFRER_SIZE = 4096#4096
    # stream = urlopen(url)
    # bts = b''
    #
    # while True:
    #     try:
    #         bts += stream.read(CAMERA_BUFFRER_SIZE)
    #         jpghead = bts.find(b'\xff\xd8')
    #         jpgend = bts.find(b'\xff\xd9')
    #         if jpghead > -1 and jpgend > -1:
    #             jpg = bts[jpghead:jpgend + 2]
    #             bts = bts[jpgend + 2:]
    #             image3 = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    #             image3 = cv2.resize(image3, (640, 480))
    #             MainWindow.displayRCCAR(window.main, image3)
    #     except Exception as e:
    #         print("Error:" + str(e))
    #         bts = b''
    #         stream = urlopen(url)
    #         continue



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    try:
        sys.exit(app.exec_())
    except:
        print('exciting')