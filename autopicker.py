import cv2
import numpy as np
import pyautogui
import time
from time import sleep
import pygetwindow as gw
import ttkbootstrap as tb
import threading
import urllib.parse
import webbrowser
import requests
import json


def AutoPick(type, ban_champion, champion_selected):
    buscar_ban_champion = r"C:\Users\matia\OneDrive\Escritorio\ML LOL\orbwalker\Autopicker\imgs\buscador_ban.png"
    banear = r"C:\Users\matia\OneDrive\Escritorio\ML LOL\orbwalker\Autopicker\imgs\banear.png"
    buscar_champion = r"C:\Users\matia\OneDrive\Escritorio\ML LOL\orbwalker\Autopicker\imgs\buscador_champion.png"
    fijar = (
        r"C:\Users\matia\OneDrive\Escritorio\ML LOL\orbwalker\Autopicker\imgs\fijar.png"
    )
    aceptar = "imgs\aceptar.png"

    def match_and_click(img, tr):
        path_to_image = img
        target_image = cv2.imread(path_to_image, cv2.IMREAD_UNCHANGED)
        target_image_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
        w, h = target_image_gray.shape[::-1]

        while not root.protocol_close:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(
                screenshot_gray, target_image_gray, cv2.TM_CCOEFF_NORMED
            )
            threshold = tr
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(screenshot_np, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                print("Imagen encontrada")
                center_x = pt[0] + w // 2
                center_y = pt[1] + h // 2
                pyautogui.click(center_x, center_y)
                return True

    def write_champ(text):
        pyautogui.write(text)
        time.sleep(0.5)

    def click_on_window(title, x, y):
        window = gw.getWindowsWithTitle(title)[0]
        absolute_x = window.left + x
        absolute_y = window.top + y
        pyautogui.click(absolute_x, absolute_y)

    if type == "normal":
        print("Has iniciado el modo normal")
        while not root.protocol_close:
            if match_and_click(aceptar, 0.8):
                sleep(4)
                match_and_click(buscar_champion, 0.8)
                sleep(2)
                write_champ(champion_selected)
                sleep(2)
                click_on_window("League of Legends", 380, 150)
                sleep(2)
                match_and_click(fijar, 0.8)
            else:
                print("Esperando a que todos los jugadores acepten la partida...")
                sleep(3)  # Esperar un tiempo antes de verificar nuevamente
    elif type == "ranked":
        print("Has iniciado el modo ranked")
        while not root.protocol_close:
            if match_and_click(aceptar, 0.8):
                sleep(30)
                match_and_click(buscar_ban_champion, 0.8)
                sleep(2)
                write_champ(ban_champion)
                sleep(2)
                click_on_window("League of Legends", 380, 150)
                sleep(2)
                match_and_click(banear, 0.8)
                sleep(2)
                match_and_click(buscar_champion, 0.8)
                sleep(2)
                write_champ(champion_selected)
                sleep(2)
                click_on_window("League of Legends", 380, 150)
                sleep(2)
                match_and_click(fijar, 0.8)
            else:
                print("Esperando a que todos los jugadores acepten la partida...")
                sleep(3)

    if not root.protocol_close:
        root.after(1000, lambda: AutoPick(type, ban_champion, champion_selected))

def send_whatsapp_message(phone_number):
    phone_number = phone_number.replace("+", "")
    encoded_message = urllib.parse.quote("Entra a la partida pedazo de hdp")
    url = f"https://web.whatsapp.com/send?phone=+54{phone_number}&text={encoded_message}"
    webbrowser.open(url)
    sleep(5)
    pyautogui.press('enter')

def check_ingame():
    request = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False).text
    data = json.loads(request)
    if data != None:
        send_whatsapp_message("2954390837")

def start_AutoPick():
    type = "ranked" if ranked_var.get() else "normal"
    ban_champion = champ_ban_entry.get()
    champion_selected = champ_select_entry.get()
    thread = threading.Thread(target=AutoPick, args=(type, ban_champion, champion_selected))
    thread.start()

def on_closing():
    root.protocol_close = True
    root.destroy()

root = tb.Window(themename="superhero", title="Duckies autopicker by Mati V1.0")
root.geometry("500x500")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

frame = tb.Frame(bootstyle="dark", height=200, width=450, padding=20)
frame.grid(row=0, column=1, sticky="n", pady=25)

title = tb.Label(
    frame, text="AUTOPICKER", font=("Monserrat", 20, "bold"), background="#20374c"
)
title.grid(row=0, column=0, columnspan=2, pady=10)

normal_var = tb.BooleanVar()
normal_var.set(False)
check_normal = tb.Checkbutton(
    frame, text="Normal", bootstyle="success", variable=normal_var
)
check_normal.grid(row=1, column=0, sticky="w")

ranked_var = tb.BooleanVar()
ranked_var.set(False)
check_ranked = tb.Checkbutton(
    frame, text="Ranked", bootstyle="success", variable=ranked_var
)
check_ranked.grid(row=1, column=1, sticky="w", pady=10)

champ_ban_label = tb.Label(
    frame, text="Campeon a banear", bootstyle="success", background="#20374c"
)
champ_ban_label.grid(row=2, column=0, sticky="w")
champ_ban_entry = tb.Entry(frame, bootstyle="success")
champ_ban_entry.grid(row=3, column=0)

champ_select_label = tb.Label(
    frame, text="Campeon a elegir", bootstyle="success", background="#20374c"
)
champ_select_label.grid(row=4, column=0, sticky="w")
champ_select_entry = tb.Entry(frame, bootstyle="success")
champ_select_entry.grid(row=5, column=0)

principal_button = tb.Button(
    frame,
    text="Iniciar",
    bootstyle="success",
    command=start_AutoPick,
)
principal_button.grid(row=6, column=0, columnspan=2, pady=15)
principal_button.config(width=30)

root.protocol_close = False
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
