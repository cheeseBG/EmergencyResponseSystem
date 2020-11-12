import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QImage, QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

## ==> SPLASH SCREEN
from ui_splash_screen import Ui_SplashScreen

## ==> MAIN WINDOW
from ui_main import Ui_MainWindow

## ==> GLOBALS
counter = 0

# YOUR APPLICATION
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.logic_rc = False
        self.logic_dr = False

        self.case = 0;

        # 버튼을 누르면 함수 실행
        self.ui.pushButton.clicked.connect(self.rcClicked)
        self.ui.pushButton_2.clicked.connect(self.drClicked)

        # set warning
        self.ui.warning1.setVisible(False)
        self.ui.warning2.setVisible(False)

        # # MAIN WINDOW LABEL
        # QtCore.QTimer.singleShot(1500, lambda: self.ui.label.setText("<strong>THANKS</strong> FOR WATCHING"))
        # QtCore.QTimer.singleShot(1500, lambda: self.setStyleSheet("background-color: #222; color: #FFF"))

        # ## REMOVE TITLE BAR
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def start(self):
        hands = mp_hands.Hands(
            min_detection_confidence=0.7, min_tracking_confidence=0.5)
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            if success:
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
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                self.displayImage(image)

                if self.logic_rc == True:
                    self.displayImage1(image)
                if self.logic_dr == True:
                    self.displayImage2(image)

                if cv2.waitKey(5) & 0xFF == 27:
                    break

        hands.close()
        cap.release()
        cv2.destroyAllWindows()

    def rcClicked(self):
        if self.logic_rc == True:
            self.logic_rc = False
            self.ui.rccarCam.setPixmap(None)
            self.case += 1
            self.ui.lcdNumber.display(self.case)
            self.ui.warning1.setVisible(False)
        else:
            self.logic_rc = True
            self.ui.warning1.setVisible(True)

    def drClicked(self):
        if self.logic_dr == True:
            self.logic_dr = False
            self.ui.droneCam.setPixmap(None)
            self.case += 1
            self.ui.lcdNumber.display(self.case)
            self.ui.warning2.setVisible(False)
        else:
            self.logic_dr = True
            self.ui.warning2.setVisible(True)

    def displayImage(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.ui.handSign.setPixmap(QPixmap.fromImage(img))
        # 가운데 맞춤
        self.ui.handSign.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        # self.ui.situation1.setPixmap(QPixmap.fromImage(img))
        # # 가운데 맞춤
        # self.ui.situation1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        # self.ui.situation2.setPixmap(QPixmap.fromImage(img))
        # # 가운데 맞춤
        # self.ui.situation2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def displayImage1(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.ui.rccarCam.setPixmap(QPixmap.fromImage(img))
        # 가운데 맞춤
        self.ui.rccarCam.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def displayImage2(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.ui.droneCam.setPixmap(QPixmap.fromImage(img))
        # 가운데 맞춤
        self.ui.droneCam.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

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


        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

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
        counter += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    try:
        sys.exit(app.exec_())
    except:
        print('exciting')