from helpers.config import getSettings,Settings

class BaseController:
    def __init__(self):
        self.appSettings=getSettings()