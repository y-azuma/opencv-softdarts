# -*- coding: utf-8 -*-
from mutagen.mp3 import MP3 as mp3
import pygame
import time


class Sounds:
    '''
    得点に応じて効果音をならす'
    '''

    def sound1(self):
        filename = 'darts_bull_sound.mp3'  # 再生したいmp3ファイル
        pygame.mixer.init()
        pygame.mixer.music.load(filename)  # 音源を読み込み
        mp3_length = mp3(filename).info.length  # 音源の長さ取得
        pygame.mixer.music.play(1)  # 再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
        time.sleep(mp3_length + 0.25)  # 再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
        pygame.mixer.music.stop()  # 音源の長さ待ったら再生停止


    def sound2(self):
        filename = "darts_award_sound.mp3"  # 再生したいmp3ファイル
        pygame.mixer.init()
        pygame.mixer.music.load(filename)  # 音源を読み込み
        mp3_length = mp3(filename).info.length  # 音源の長さ取得
        pygame.mixer.music.play(1)  # 再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
        time.sleep(mp3_length + 0.25)  # 再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
        pygame.mixer.music.stop()  # 音源の長さ待ったら再生停止
