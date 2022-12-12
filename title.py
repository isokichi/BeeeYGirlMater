import time
import cv2
import numpy as np

class title_screen:
    def __init__(self, time, cap):
        self.time = time
        # TODO できたら動画にかえる
        self.title_image = cv2.imread("images/title.png")
        self.title_image = scale_to_height(self.title_image, 1080)

        self.cap = cap
        frame = cap.read()

    def play(self):
        print("--nobinobi AR-- title start")

        hasFrame, frame = self.cap.read()

        while True:
            key = cv2.waitKey(1) # 1ミリ秒で次の画面へ
            t = time.time()
            hasFrame, frame = self.cap.read()
            # frameCopy = np.copy(frame)
            if not hasFrame:
                cv2.waitKey(1)
                break

            # ゲーム開始
            if key == ord('s'):
                print("--nobinobi AR-- title end")
                break

            # height, width, channels = frame.shape[:3]
            # t_height, t_width, t_channels = self.title_image.shape[:3]
            

            # dx = int((width - t_width) / 2)
            # # frame = overlay(self.title_image, frame, (shift_x, 0))
            # M = np.array([[1, 0, dx], [0, 1, 0]], dtype=float)
            # title = cv2.warpAffine(self.title_image, M, (width, height), frame, borderMode=cv2.BORDER_TRANSPARENT)
            title = side(frame, self.title_image)
 

            cv2.imshow("nobinobi AR" , title)

def scale_to_height(img, height):
    """高さが指定した値になるように、アスペクト比を固定して、リサイズする。
    """
    h, w = img.shape[:2]
    width = round(w * (height / h))
    dst = cv2.resize(img, dsize=(width, height))

    return dst

def side(center, side):
    height, width, channels = center.shape[:3]
    t_height, t_width, t_channels = side.shape[:3]
    
    dx = int(width - t_width)
    M = np.array([[1, 0, dx], [0, 1, 0]], dtype=float)
    center = cv2.warpAffine(side, M, (width, height), center, borderMode=cv2.BORDER_TRANSPARENT)

    M = np.array([[1, 0, 0], [0, 1, 0]], dtype=float)
    center = cv2.warpAffine(side, M, (width, height), center, borderMode=cv2.BORDER_TRANSPARENT)

    return center