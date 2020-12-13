# import urllib.request as urllib
import cv2
import numpy as np

cv2.VideoCapture("http://192.168.0.152:81/stream")
#
# stream = urllib.urlopen('http://172.30.1.37:81/stream')
#
# bytes = bytes()
# while True:
#     bytes += stream.read(1024)
#     a = bytes.find(b'\xff\xd8')
#     b = bytes.find(b'\xff\xd9')
#     if a != -1 and b != -1:
#         jpg = bytes[a:b + 2]
#         bytes = bytes[b + 2:]
#         i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)
#         cv2.imshow('i', i)
#         if cv2.waitKey(1) == 27:
#             exit(0)
# import cv2 as cv
# import numpy as np
# from urllib.request import urlopen
# from socket import *
#
# clientSock = socket(AF_INET, SOCK_STREAM)
# url = '192.168.0.152'
# clientSock.connect((url, 80))
#
# # change to your ESP32-CAM ip
# # url = "http://192.168.0.152:81/stream"
# stream = clientSock.recv(4096)
# # stream = urlopen(url)
# bts = b''
# i = 0
# while True:
#     try:
#         bts += stream
#         jpghead = bts.find(b'\xff\xd8')
#         jpgend = bts.find(b'\xff\xd9')
#         if jpghead > -1 and jpgend > -1:
#             jpg = bts[jpghead:jpgend + 2]
#             bts = bts[jpgend + 2:]
#             img = cv.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv.IMREAD_UNCHANGED)
#             img = cv.resize(img, (640, 480))
#             cv.imshow("a", img)
#         k = cv.waitKey(1)
#     except Exception as e:
#         print("Error:" + str(e))
#         bts = b''
#         stream = urlopen(url)
#         continue
#
#     k = cv.waitKey(1)
#     if k & 0xFF == ord('a'):
#         cv.imwrite(str(i) + ".jpg", img)
#         i = i + 1
#     if k & 0xFF == ord('q'):
#         break
# cv.destroyAllWindows()
