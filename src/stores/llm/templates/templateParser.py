import os

class TemplateParser:
    def __init__(self, lang=None, defaultLang="en"):
        self.currentPath = os.path.dirname(__file__)
        self.defaultLang = defaultLang
        self.lang = None
        self.setLang(lang)

    def setLang(self, lang):
        if not lang:
            self.lang = self.defaultLang
            return
        
        langPath = os.path.join(self.currentPath, "locales", lang)
        if os.path.exists(langPath):
            self.lang = lang
        else:
            self.lang = self.defaultLang
    
    def get(self, group, key, vars:dict={}):
        if not group or not key:
            return None
        
        groupPath = os.path.join(self.currentPath, "locales", self.lang, f"{group}.py")
        targetLang = self.lang
        
        if not os.path.exists(groupPath):
            groupPath = os.path.join(self.currentPath, "locales", self.defaultLang, f"{group}.py")
            targetLang = self.defaultLang
        
        if not os.path.exists(groupPath):
            return None
        
        module = __import__(f"stores.llm.templates.locales.{targetLang}.{group}", fromlist=[group])
        if not module:
            return None
        
        keyAttr = getattr(module, key)
        return keyAttr.substitute(vars)
