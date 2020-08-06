import os
import sys

from c_paths import paths


# mech for finding all records; iterator counter
# we don't have a dir for every integer, so 
# the index is not==GB book id; it's just a counter
# get the GB ID for the dir contents by 
# converting the dir's name to an int
class scanner:
    def __init__(self):
        self.dirIndex = 0
        self.allFiles = []
        self.counter = 1
        self.gbID = '-1'
        self.last = -1
        # find the top dir
        paths = paths()
        self.dir = paths.recordsDir
        mess = [x[1] for x in os.walk(dir)]
        self.allFiles = mess[0]
        self.last = len(self.allFiles)
        print("found ", self.last, " records")
        if (self.last>0):
            self.counter = 1

    # restart after crash; say which one to start at
    def skipTo(self, which):
        self.counter = which

    # return path to next .rdf record
    def getNextPath(self):
        res = ''
        if (self.counter!=-1 and self.counter<self.last):
            fls = self.allFiles[self.counter]
            self.gbID = fls  # fls is the dir name. fls!=counter !
            self.counter +=1
            res = self.dir + fls + "\\pg" + fls + ".rdf"
        else:
            self.counter = -1
        return res

