import cv2
import numpy as np
import mss
import pyglet
import threading
from time import sleep

def play_sound(sound_file):
    sound = pyglet.media.load(sound_file)
    sound.play()

def wait_and_play(sound_file):
    sleep(2)
    play_sound(sound_file)

def match_and_notify(img_path, threshold=0.8):
    target_image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    w, h = target_image.shape[::-1]

    sound_file = r"C:\Users\matia\OneDrive\Escritorio\ML LOL\orbwalker\Autopicker\imgs\bump.mp3"

    with mss.mss() as sct:
        monitor = {"top": 940, "left": 2050, "width": 500, "height": 500}

        sound_thread = None

        while True:
            screenshot = np.array(sct.grab(monitor))
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(screenshot_gray, target_image, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):
                cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                print("Imagen encontrada en la región de la pantalla")

                if sound_thread is None or not sound_thread.is_alive():
                    sound_thread = threading.Thread(target=wait_and_play, args=(sound_file,))
                    sound_thread.start()

            cv2.imshow('Región de búsqueda', screenshot)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()

    return len(loc[0]) > 0

image_path = r'C:\Users\matia\OneDrive\Escritorio\ML LOL\orbwalker\Autopicker\imgs\champs\ww.png'

threshold_value = 0.6
found = match_and_notify(image_path, threshold_value)
