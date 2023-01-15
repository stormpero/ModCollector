import os
import shutil
import sys
import subprocess

import tkinter as tk
from tkinter import filedialog

import PIL.Image
from pystray import Menu, MenuItem, Icon

from Paths import Paths

root = tk.Tk()
root.withdraw()

paths = Paths()
paths_config = paths.get()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def clearFolderMods():
    shutil.rmtree(paths_config["PATH_OUTPUT"])
    os.makedirs(paths_config["PATH_OUTPUT"])


# def startMinecraft():
#     os.system(f"start {paths_config['PATH_MINECRAFT']}")
#     x = 970
#     y = 745
#     color = "(0, 140, 69)"
#     while True:
#         px = pyautogui.pixel(x, y)
#         print(str(px))
#         if str(px) == color:
#             pyautogui.click(x, y)
#             break
#         time.sleep(0.5)


def updateModes():
    clearFolderMods()
    for root, subFolder, files in os.walk(paths_config["PATH_INPUT"]):
        for item in files:
            if item.endswith(".jar"):
                print(root + "\\" + item)
                shutil.copy(root + "\\" + item, paths_config["PATH_OUTPUT"] + "\\" + item)


def updateModesAndStart():
    updateModes()
    # startMinecraft()


image_main = PIL.Image.open(resource_path("icons/buildmods.ico"))
image_loading = PIL.Image.open(resource_path("icons/loading.ico"))
image_error = PIL.Image.open(resource_path("icons/error.ico"))


def is_loading(icon, state):
    icon.icon = image_loading if state else image_main


def on_ready(icon):
    icon.notify('Ready')


def is_filepaths_exists(icon):
    if not paths_config["PATH_INPUT"]:
        icon.notify('PATH_INPUT is None. Enter it in settings!')
    if not paths_config["PATH_OUTPUT"]:
        icon.notify('PATH_OUTPUT is None. Enter it in settings!')
    else:
        return True


def on_clicked_build(icon, item):
    print("Build")
    if not is_filepaths_exists(icon):
        return
    is_loading(icon, True)
    print("Build: Start")
    updateModes()
    is_loading(icon, False)
    on_ready(icon)


def on_clicked_build_and_start(icon, item):
    print("Build And Start")
    if not is_filepaths_exists(icon):
        return
    is_loading(icon, True)
    print("Build And Start: Start")
    updateModesAndStart()
    is_loading(icon, False)


def on_clicked_exit(icon, item):
    print("Exit")
    icon.stop()


def on_clicked_path_input(icon, item):
    paths_config["PATH_INPUT"] = filedialog.askdirectory().replace("/", "\\")
    paths.save()


def on_clicked_path_output(icon, item):
    paths_config["PATH_OUTPUT"] = filedialog.askdirectory().replace("/", "\\")
    paths.save()


def on_clicked_path_minecraft(icon, item):
    paths_config["PATH_MINECRAFT"] = filedialog.askopenfilename().replace("/", "\\")
    paths.save()


def on_clicked_open_explorer(icon, item):
    subprocess.Popen(rf'explorer "{paths_config["PATH_INPUT"]}"')
    subprocess.Popen(rf'explorer "{paths_config["PATH_OUTPUT"]}"')


def ui_menu():
    return Menu(
        MenuItem('Modpacks Build', action=None, enabled=False),
        Menu.SEPARATOR,
        MenuItem('Build', on_clicked_build, default=False),
        # MenuItem('Build and Start', on_clicked_build_and_start),
        Menu.SEPARATOR,
        MenuItem('Settings', Menu(
            MenuItem("Path input", on_clicked_path_input),
            MenuItem('Path output', on_clicked_path_output),
            MenuItem('Path minecraft.exe', on_clicked_path_minecraft),
            MenuItem('Open explorers', on_clicked_open_explorer),
        )),
        Menu.SEPARATOR,
        MenuItem('Exit', on_clicked_exit),
    )


def on_error(icon, error):
    icon.icon = image_error
    icon.notify('ERROR:' + str(error))
    print('ERROR:' + str(error))


def main():
    icon = Icon("Mods", image_main,
                menu=ui_menu(),
                title="Modpacks Build")
    try:
        icon.run()
    except Exception as e:
        on_error(icon, e)


if __name__ == '__main__':
    main()
