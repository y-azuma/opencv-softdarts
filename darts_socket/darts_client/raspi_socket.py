# -*- coding: utf-8 -*-
import numpy as np
import picamera
import pyaudio
import time
import cv2
import socket
import sys
import imageprocessor


def socket_connect(host, port, interval, retries):
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for x in xrange(retries):
        try:
            c_socket.connect((host, port))
            return c_socket
        except socket.error:
            print("wait"+str(interval)+"s")
            time.sleep(interval)
    c_socket.close()
    return None

def main(senddata):
    c_socket = socket_connect(HOSTNAME, PORT, INTERVAL, RETRYTIMES)

    if c_socket is None:
        print("system exit")
        sys.exit
    c_socket.send(senddata)


class Raspberrypi:
    '''
    ダーツ音を感知し、闢値を超えていたならカメラを撮り、画像情報を送る。
    '''

    def __init__(self):
        self.chunk = 512
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.threshold = 0.04

    def take_pictures(self):
        self. p = pyaudio.PyAudio()
        self.stream = self.p.open(
                 format=self.FORMAT,
                 channels = self.CHANNELS,
                 rate = self.RATE,
                 input = True,
                 frames_per_buffer = self.chunk
        )
        self.n = 0


        while True:
            self.data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.x = np.frombuffer(self.data, dtype="int16")/32768.0
            if self.x.max() > self.threshold:
                print("take a picture")
                print(self.x.max())
                with picamera.PiCamera() as camera:
                 camera.resolution = (1024,768)
                 camera.start_preview()
                 time.sleep(2)
                 camera.capture('darts_picture.jpg')
                 img1 = cv2.imread('darts_picture.jpg')
                 frag=image_proc.image_scan(img1)
                 photoorder = image_proc.photoorder
                 round_total = image_proc.round_total
                 first_throw = image_proc.first_throw
                 second_throw = image_proc.second_throw
                 third_throw = image_proc.third_throw
                 bull_data = str(frag) + "," + str(photoorder) + "," + str(round_total) + "," + str(first_throw) + "," + str(second_throw) + "," + str(third_throw)
                 bull_data1 = bull_data.encode('utf-8')

                 main(bull_data1)


        self.stream.close()
        self.p.terminate()

        

HOSTNAME = "192.168.0.3"
PORT = 12345
INTERVAL = 2
RETRYTIMES = 5
image_proc = imageprocessor.ImageProcessor()
raspberrypi = Raspberrypi()
raspberrypi.take_pictures()



