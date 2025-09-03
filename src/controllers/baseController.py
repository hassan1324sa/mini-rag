from helpers.config import getSettings,Settings
import os ,random,string
class BaseController:
    def __init__(self):
        self.appSettings=getSettings()
        self.baseDir = os.path.dirname( os.path.dirname(__file__) )
        self.filesDir= os.path.join(self.baseDir,"assets/files")
    

        
    def generateRandomString(self,length:int=12):
        return ''.join(random.choices(string.ascii_lowercase+string.digits,k=length))