# PythonAI
# Kevin McAleer
# April 2021

class Skill():
    __name = ""
    __actions = []
    __version = 0.1

    def __init__(self, name=None):
        if name is not None:
            self.name = name
        else: self.name = "new skill"
        print(self.name, "skill loaded")

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        self.__version = value

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value