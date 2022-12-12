import time
import datetime
import cv2
import numpy as np

class game_screen:
    def __init__(self, time, cap):
        self.time = time
        # TODO できたら動画にかえる
        self.text_images = [cv2.imread("images/1_text.png"), cv2.imread("images/2_text.png"), cv2.imread("images/3_text.png")]
        for i in range(len(self.text_images)):
            self.text_images[i] = scale_to_height(self.text_images[i], 1080)

        self.count_images = [[cv2.imread("images/1_count_3.png"), cv2.imread("images/1_count_2.png"), cv2.imread("images/1_count_1.png")], [cv2.imread("images/2_count_3.png"), cv2.imread("images/2_count_2.png"), cv2.imread("images/2_count_1.png")], [cv2.imread("images/3_count_3.png"), cv2.imread("images/3_count_2.png"), cv2.imread("images/3_count_1.png")]]

        for i in range(len(self.count_images)):
            for j in range(len(self.count_images[i])):
                self.count_images[i][j] = scale_to_height(self.count_images[i][j], 1080)

        self.nobi_images = [cv2.imread("images/1_nobi.png"), cv2.imread("images/2_nobi.png"), cv2.imread("images/3_nobi.png")]
        for i in range(len(self.nobi_images)):
            self.nobi_images[i] = scale_to_height(self.nobi_images[i], 1080)

        self.start_time = datetime.datetime.now() #プレイ開始のタイムスタンプ
        self.timestamp = self.start_time.strftime('%Y%m%d%H%M%S')

        self.cap = cap
        frame = cap.read()

    def play(self):

        self.start_time = datetime.datetime.now() #プレイ開始のタイムスタンプ
        self.timestamp = self.start_time.strftime('%Y%m%d%H%M%S')

        for stage in range(3):
            self.text(stage)
            self.count(stage)
            self.nobi(stage)

        self.result()

    def text(self, stage):
        
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
                print("--nobinobi AR-- text end")
                break

            text = side(frame, self.text_images[stage])

            cv2.imshow("nobinobi AR", text)

    def count(self, stage):

        for img in self.count_images[stage]:

            time_sta = time.time()
            while True:
                key = cv2.waitKey(1) # 1ミリ秒で次の画面へ
                t = time.time()
                hasFrame, frame = self.cap.read()
                # frameCopy = np.copy(frame)
                if not hasFrame:
                    cv2.waitKey(1)
                    break

                if t -time_sta > 1:
                    print("--nobinobi AR-- count end")
                    break

                if key == ord('s'):
                    print("--nobinobi AR-- count end")
                    break

                count = side(frame, img)

                cv2.imshow("nobinobi AR", count)
    
    def nobi(self, stage):
        time_sta = time.time()
        while True:
            key = cv2.waitKey(1) # 1ミリ秒で次の画面へ
            t = time.time()
            hasFrame, frame = self.cap.read()
            # frameCopy = np.copy(frame)
            if not hasFrame:
                cv2.waitKey(1)
                break

            if t -time_sta > 3:
                cv2.imwrite('outputs/{:14s}_{}.png'.format(self.timestamp, stage), frame)
                print("--nobinobi AR-- nobi end")
                break

            if key == ord('s'):
                cv2.imwrite('outputs/{:14s}_{}.png'.format(self.timestamp, stage), frame)
                print("--nobinobi AR-- nobi end")
                break

            if key == ord('t'):
                time_sta = time.time()

            nobi = side(frame, self.nobi_images[stage])

            cv2.imshow("nobinobi AR", nobi)

    def result(self):
        bg = cv2.imread("images/back.png")

        pics = [cv2.imread('outputs/{:14s}_0.png'.format(self.timestamp)), cv2.imread('outputs/{:14s}_1.png'.format(self.timestamp)), cv2.imread('outputs/{:14s}_2.png'.format(self.timestamp))]
        chas = [cv2.imread('images/cha1.png', cv2.IMREAD_UNCHANGED), cv2.imread('images/cha2.png', cv2.IMREAD_UNCHANGED), cv2.imread('images/cha3.png', cv2.IMREAD_UNCHANGED)]
        
        for i in range(len(pics)):
            pics[i] = scale_to_height(pics[i], 864)
            pics[i] = pics[i][0 : 864, 486 : 1051]
            #w565

        time_sta = time.time()

        while True:
            key = cv2.waitKey(1) # 1ミリ秒で次の画面へ
            t = time.time()
            hasFrame, frame = self.cap.read()

            if t -time_sta > 1:
                height, width, channels = bg.shape[:3]
                M = np.array([[1, 0, 56], [0, 1, 108]], dtype=float)
                bg = cv2.warpAffine(pics[0], M, (width, height), bg, borderMode=cv2.BORDER_TRANSPARENT)
                
                # bg = cv2.warpAffine(chas[0], M, (width, height), bg, borderMode=cv2.BORDER_TRANSPARENT)
                # putSprite_mask(bg, chas[0], (0, 0))

                # 貼り付け先座標の設定。とりあえず左上に
                x1, y1, x2, y2 = 28, 1080-chas[0].shape[0], 28+chas[0].shape[1], 1080
                # 合成!
                bg[y1:y2, x1:x2] = bg[y1:y2, x1:x2] * (1 - chas[0][:, :, 3:] / 255) + \
                                    chas[0][:, :, :3] * (chas[0][:, :, 3:] / 255)

            if t -time_sta > 2:
                height, width, channels = bg.shape[:3]
                M = np.array([[1, 0, 678], [0, 1, 108]], dtype=float)
                bg = cv2.warpAffine(pics[1], M, (width, height), bg, borderMode=cv2.BORDER_TRANSPARENT)

                # 貼り付け先座標の設定。とりあえず左上に
                x1, y1, x2, y2 = 650, 1080-chas[1].shape[0], 650+chas[1].shape[1], 1080
                # 合成!
                bg[y1:y2, x1:x2] = bg[y1:y2, x1:x2] * (1 - chas[1][:, :, 3:] / 255) + \
                                    chas[1][:, :, :3] * (chas[1][:, :, 3:] / 255)
 
            if t -time_sta > 3:
                height, width, channels = bg.shape[:3]
                M = np.array([[1, 0, 1299], [0, 1, 108]], dtype=float)
                bg = cv2.warpAffine(pics[2], M, (width, height), bg, borderMode=cv2.BORDER_TRANSPARENT)

                # 貼り付け先座標の設定。とりあえず左上に
                x1, y1, x2, y2 = 1271, 1080-chas[2].shape[0], 1271+chas[2].shape[1], 1080
                # 合成!
                bg[y1:y2, x1:x2] = bg[y1:y2, x1:x2] * (1 - chas[2][:, :, 3:] / 255) + \
                                    chas[2][:, :, :3] * (chas[2][:, :, 3:] / 255)

            if not hasFrame:
                cv2.waitKey(1)
                break

            if key == ord('s'):
                print("--nobinobi AR-- end")
                break

            cv2.imshow("nobinobi AR", bg)





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

def putSprite_mask(back, front4, pos):
    x, y = pos
    fh, fw = front4.shape[:2]
    bh, bw = back.shape[:2]
    x1, y1 = max(x, 0), max(y, 0)
    x2, y2 = min(x+fw, bw), min(y+fh, bh)
    if not ((-fw < x < bw) and (-fh < y < bh)) :
        return back
    front3 = front4[:, :, :3]
    mask1 = front4[:, :, 3]
    mask3 = 255 - cv2.merge((mask1, mask1, mask1))
    mask_roi = mask3[y1-y:y2-y, x1-x:x2-x]
    front_roi = front3[y1-y:y2-y, x1-x:x2-x]
    roi = back[y1:y2, x1:x2]
    tmp = cv2.bitwise_and(roi, mask_roi)
    tmp = cv2.bitwise_or(tmp, front_roi)
    back[y1:y2, x1:x2] = tmp
    return back