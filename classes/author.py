

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


    def authTag(self):
        nm = self.name.replace(" ","_")
        nm += "_" + self.gutenId 
        return nm

    # for my cat, root/authors/index.html
    #             root/authors/firstLetter/index.html
    #             root/authors/firstLetter/lastname.html
    def htmlDir(self):
        nm = self.authTag()
        fs = nm[0:1]
        thePaths = paths()
        return thePaths.htmlDir + "\\authors\\" + fs + "\\"

    def htmlPath(self):
        pt = self.htmlDir()
        tg = self.authTag()
        return pt + tg + ".html"


    # CalLibre uses one dir per author
    def calDir(self):
        return self.calPath + self.authTag()


    def matches(self, other):
        t1 = self.authTag()
        t2 = other.authTag()
        if (t1==t2):
            return True
        return False

    def duplicate(self):
        res = author()
        res.gutenId = self.gutenId
        res.name = self.name
        res.birth = self.birth
        res.death = self.death
        for id in self.workIds:
            res.workIds.append(id)
        res.wikiLink = self.wikiLink
        return res
