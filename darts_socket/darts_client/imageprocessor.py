# -*- coding: utf-8 -*-
import numpy as np
import cv2


class ImageProcessor:
    '''
    opencvを使って画像処理を施し、ダーツの矢を認識する。
    '''

    def __init__(self):
        self.photonumber = 0
        self.a = 0
        self.b = 0
        self.threshold = 0
        self.round_total = 0
        self.first_throw = 0
        self.second_throw = 0
        self.third_throw = 0
        self.photoorder = 0

    def image_scan(self,imgz):
        self.photoorder = self.photonumber % 3+1
        flag = 0
        self.round_total = 0

        # frameに画像を入れて切り抜き
        img2 = imgz[363:475, 265:350]

        # 画像の平滑化
        img_bi = cv2.bilateralFilter(img2, 20, 120, 120)

        # 色検出
        hsv = cv2.cvtColor(img_bi, cv2.COLOR_BGR2HSV)
        lower = np.array([40, 84, 40])
        upper = np.array([110, 230, 110])
        frame_mask = cv2.inRange(hsv, lower, upper)
        dst = cv2.bitwise_and(img_bi, img_bi, mask=frame_mask)

        # グレースケール
        img_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

        # 二値化
        ret1, img_th = cv2.threshold(img_gray, self.threshold, 255, cv2.THRESH_BINARY)


        # ラベリング処理
        color_src01 = cv2.cvtColor(img_th, cv2.COLOR_GRAY2BGR)
        label = cv2.connectedComponentsWithStats(img_th)
        n = label[0] - 1
        print("n="+str(n))
        data = np.delete(label[2], 0, 0)
        center = np.delete(label[3], 0, 0)
        for i in range(n):
            x0 = data[i][0]
            y0 = data[i][1]
            x1 = data[i][0] + data[i][2]
            y1 = data[i][1] + data[i][3]
            cv2.rectangle(color_src01, (x0, y0), (x1, y1), (0, 0, 255))
            cv2.putText(color_src01, "X: " + str(int(center[i][0])), (x1 - 30, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 255, 255))
            cv2.putText(color_src01, "Y: " + str(int(center[i][1])), (x1 - 30, y1 + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 255, 255))


        # ブルに入ってたらBULL!!!と表示
        if self.photoorder == 1 and n == 1:
            # cv2.putText(color_src01, "BULL!!!", (x1 - 85, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255))
            print("bull")
            self.a += 1
            flag = 1
            self.first_throw = 50
        elif self.photoorder == 2 and (n + self.a) % 2 == 1:
            print("bull")
            self.b += 1
            flag = 1
            self.second_throw = 50
        elif self.photoorder == 3 and (n + self.a + self.b) % 2 == 1:
            print("bull")
            self.a = 0
            self.b = 0
            flag = 1
            self.third_throw = 50


        if self.photoorder==3:
            self.round_total = self.first_throw+self.second_throw+self.third_throw
            self.first_throw = 0
            self.second_throw = 0
            self.third_throw = 0


        self.photonumber += 1

        return flag

