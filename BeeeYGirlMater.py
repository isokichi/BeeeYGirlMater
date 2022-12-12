import cv2
import time
import numpy as np

import title
import game

def main():
    print("--nobinobi AR-- system boot up")

    # カメラの読み込み
    # TODO カメラ自動認識
    cap = cv2.VideoCapture(1)

    # windowサイズ設定 TODO 本番環境ではフルスクリーン
    cv2.namedWindow("nobinobi AR", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("nobinobi AR", 1080, 1920) 

    # オブジェクト
    title_screen = title.title_screen(time.time(), cap)
    game_screen = game.game_screen(time.time(), cap)

    while True:
        # タイトル画面
        title_screen.play()
        # 待機画面
        # 遊び方の説明
        # ゲームスタート
        game_screen.play()

        # 骨格検知点数化
        # 結果表示

        # スマホに落とせるように？
        # ゲーム終了

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()