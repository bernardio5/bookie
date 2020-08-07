

from classes.paths import paths

# aouthor or translator, same data, same class
class author: 
    def __init__(self):
        self.gutenId = " "
        self.name = " "
        self.birth = " "
        self.death = " "
        self.workIds = []
        self.wikiLink = " "
        thePaths = paths()
        self.calPath = thePaths.outputDir

    # uniqe per-author string. 
    def authTag(self):
        nm = self.name.replace(" ","_")
        nm += "_" + self.gutenId 
        return nm

    # CalLibre uses one dir per author
    def calDir(self):
        return self.calPath + self.authTag()

