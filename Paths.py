import configparser
import os

CONFIG_FILENAME = "paths.ini"


# self.PATH_INPUT = r"F:\Stormpero\Сборка Маинкравт\bundles"
# self.PATH_OUTPUT = r"C:\Users\staro\AppData\Roaming\.minecraft\Another Versions\Automation Technology\mods"
# self.PATH_MINECRAFT = r"C:\Users\staro\AppData\Roaming\.minecraft\Minecraft.lnk"

class Paths:

    def __init__(self):
        self.config = configparser.ConfigParser()
        if not os.path.exists(CONFIG_FILENAME):
            self.config["PATH"] = {
                "PATH_INPUT": "",
                "PATH_OUTPUT": "",
                "PATH_MINECRAFT": ""
            }
            self.save()
        else:
            self.config.read(CONFIG_FILENAME)

    def get(self):
        return self.config["PATH"]

    def save(self):
        with open(CONFIG_FILENAME, 'w') as configfile:
            self.config.write(configfile)

