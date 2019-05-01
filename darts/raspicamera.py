# -*- coding: utf-8 -*-
import numpy as np
import picamera
import pyaudio
import time
import cv2


class Raspberrypi:
    '''
    ダーツ音を感知し、闢値を超えていたならカメラを撮り、画像情報を送る。
    '''

    def __init__(self):
        self.chunk = 512
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.threshold = 0.07

    def take_pictures(self):
        self. p = pyaudio.PyAudio()
        self.stream = self.p.open(
                 format=self.FORMAT,
                 channels=self.CHANNELS,
                 rate=self.RATE,
                 input=True,
                 frames_per_buffer=self.chunk
        )
        self.n = 0


        while True:
            self.data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.x = np.frombuffer(self.data, dtype="int16")/32768.0

            if self.x.max() > self.threshold:
                print("take a picture")
                with picamera.PiCamera() as camera:
                 camera.resolution = (1024,768)
                 camera.start_preview()
                 time.sleep(2)
                 camera.capture('darts_picture.jpg')

                 img1 = cv2.imread('darts_picture.jpg')
                 yield img1

        self.stream.close()
        self.p.terminate()
