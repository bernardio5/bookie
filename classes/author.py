
# same rec for author and translator. I prefer Homer by Chapman, y'know? 

class author: 
    def __init__(self):
        self.gutenId = " "
        self.name = " "
        self.birth = " "
        self.death = " "
        self.workIds = []
        self.wikiLink = " "

    # uniqe per-author string. 
    def authTag(self):
        nm = self.name.replace(" ","_")
        nm += "_" + self.gutenId 
        return nm

# CalLibre uses one dir per author
    def calDir(self):
        return "D:\\library\\newCal\\" + self.authTag()

