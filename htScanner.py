import csv
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 
import zipfile
import numpy as np
import cv2
import random
import sys

class author: 
    def __init__(self):
        self.gutenId = " "
        self.name = " "
        self.birth = " "
        self.death = " "
        self.workIds = []
        self.wikiLink = " "

    def authTag(self):
        nm = self.name.replace(" ","_")
        nm += "_" + self.gutenId 
        return nm

    def calDir(self):
        return "D:\\library\\newCal\\" + self.authTag()


# all the book data
class book:
    def __init__(self):
        # pulled from GBg XML collection
        self.gutenId = -1
        self.title = " "
        self.auths = []      # authors and translators
        self.trns = []
        self.imgs = []
        self.auth = author() # scratch for parsing
        self.subjects = []   # refine: lots of kitchen-sinking
        self.formats = []    # do we care? we have to verify anyway.
        self.language = "-"
        self.type = "-"
        self.description = "-"
        self.date = " "      # !! not present in GB XML! smh
        # set by scanning the gbg dirs; set to "-" if absent
        self.gbgDir = "-"    
        self.txtPath = "-"    
        self.htmPath = "-"
        self.imgPath = "-"
        self.coverImgPath = -1

    def bookTag(self):
        nm = self.title.replace(" ","_") # del all chars not legal for windows paths! 
        nm = nm.replace(":","_")
        nm = nm.replace('"','') # also spaces cause they don't belong! 
        nm = nm.replace("\r","_") # '"' y u no good?
        nm = nm.replace("\n","") # ugh! newlines? scram
        nm = nm[0:50] + "_" + str(self.gutenId)
        return nm

    # authTag for the whichth author or translator
    def authTag(self, which):
        ath = "-"
        na = len(self.auths)
        if (which<na):
            ath = self.auths[which].authTag();
        else:
            wh = which - na
            nt = len(self.trns)
            if (wh<nt):
                ath = self.trns[which].authTag();
        return self.safeString(ath)


    def langOK(self):
        if (self.language == "ch"):
            return False
        if (self.language == "zh"):
            return False
        return True

    # returns the path in e:\gbg that contains the book
    def makeGBGDir(self): 
        res = "E:\\gbg\\"
        lng = len(self.gutenId); 
        if (lng==1):
            res += "0\\"
        for i in range(0,lng-1):
            res += self.gutenId[i] + "\\"
        res += self.gutenId;
        return res

    def safeString(self, inStr):
        safe = inStr
        alloweds = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_~+=:;?><-, 1234567890"
        for i in range(0,len(inStr)):
            if (alloweds.find(inStr[i])==-1):
                safe = safe.replace(inStr[i], "")
        return safe

    # given a Gb ID and a path to an XML for it, scan the XML
    def readGbXML(self, gid, xmlfile): 
        self.gutenId = gid
        self.subjects.append("GB# " + str(gid))
        self.gbgDir = self.makeGBGDir()
        self.txtPath = self.gbgDir + "\\" + self.gutenId + ".txt"
        tree = ET.parse(xmlfile) # create element tree object 
        root = tree.getroot()  # get root element 
        for rec in root:
            tg = rec.tag.split('}',1)[-1]
            if (tg == "ebook"):
                bookRecs = rec
        for child in bookRecs:
            tg = child.tag.split('}',1)[-1]
            if (tg == "title"):
                self.title = self.safeString(child.text)
            if (tg == "bookshelf"):
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    if (gctg == "value"):
                        self.subjects.append("Bookshelf: " + gchild.text)
            if (tg == "hasFormat"):
                try:
                    vals = list(child[0].attrib.values())
                    self.formats.append(vals[0])  # pgterms:file rdf:about="http....images"
                    for gchild in child[0]:
                        gctg = gchild.tag.split('}',1)[-1]
                        if (gctg == "format"):
                            for ggch in gchild:
                                ggctg = ggch.tag.split('}',1)[-1]
                                if (ggctg == "Description"):
                                    vals = list(ggch.attrib.values())
                                    self.uuid = vals[0] # uuid = attr[0].value[0]  uuugh
                except:
                    tg = "eh just get the next one"
            if (tg == "subject"):
                subjText = ": "
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    if (gctg == "value"):
                        subjText = subjText + gchild.text
                    if (gctg == "memberOf"):
                        vals = list(gchild.attrib.values())
                        if (len(vals[0])>26):
                            subjText = vals[0][25:] + subjText 
                if (subjText!=": "):
                    self.subjects.append(subjText)
            if (tg == "creator"):
                try:
                    self.auth = author()
                    vals = list(child[0].attrib.values()) #23702
                    self.auth.gutenId = vals[0][12:]
                    for gchild in child[0]:
                        gctg = gchild.tag.split('}',1)[-1]
                        if (gctg == "webpage"):
                            vals = list(gchild.attrib.values())
                            self.auth.wikiLink = vals[0]
                        if (gctg == "name"):
                            self.auth.name = gchild.text 
                        if (gctg == "birthdate"):
                            self.auth.birth = gchild.text 
                        if (gctg == "deathdate"):
                            self.auth.death = gchild.text
                    self.auths.append(self.auth)
                except:
                    tg = "eh just get the next one"
            if (tg == "trl"):
                try:
                    vals = list(child[0].attrib.values())
                    self.auth.gutenId = vals[0][12:]
                    for gchild in child[0]:
                        gctg = gchild.tag.split('}',1)[-1]
                        if (gctg == "webpage"):
                            vals = list(gchild.attrib.values())
                            self.auth.wikiLink = vals[0]
                        if (gctg == "name"):
                            self.auth.name = gchild.text
                        if (gctg == "birthdate"):
                            self.auth.birth = gchild.text 
                        if (gctg == "deathdate"):
                            self.auth.death = gchild.text
                    self.trns.append(self.auth)
                    self.auth = author()
                except:
                    tg = "eh just get the next one"
            if (tg == "language"):
                try: 
                    self.language = child[0][0].text
                except: 
                    self.language = "en"
            if (tg == "description"):
                self.description = child.text
            if (tg == "type"):
                try: 
                    self.type = child[0][0].text
                except: 
                    self.type = "Text"

    # looks in the gbg for the book's .txt, .htm, and images dir
    # if there are images, chooses one to use as the cover image
    # empty records are set to "-"
    def scanGBDir(self):
        self.gbgDir = self.makeGBGDir()
        if (not os.path.isdir(self.gbgDir)):
            return 4 # no dir
        if (self.type=="Sound"):
            return 5 # is sound
        self.txtPath = self.gbgDir + "\\" + self.gutenId + ".txt"
        htPth = self.gbgDir + "\\" + self.gutenId + "-h\\"
        htmPath1 = htPth + self.gutenId + "-h.htm"
        htmPath2 = htPth + self.gutenId + "-h.html"
        htmPath3 = htPth + self.gutenId + "-h.xhtml"# fucking pick one, kk?
        self.imgPath = htPth + "images"
        scan = os.listdir(self.gbgDir)
        if (not os.path.isfile(self.txtPath)):
            self.txtPath = "-"
            for fn in scan:
                suf = fn[-4:]
                if (suf==".txt"):
                    self.txtPath = self.gbgDir + "\\" + fn
                    self.type = "Text"
        else:
            self.type = "Text"
        self.htmPath = "-"
        if (os.path.isfile(htmPath1)):
            self.htmPath = htmPath1
        if (os.path.isfile(htmPath2)):
            self.htmPath = htmPath2
        if (os.path.isfile(htmPath3)): 
            self.htmPath = htmPath3
        if (self.htmPath!="-"):
            self.type = "Text"
        if (not os.path.isdir(self.imgPath)):
            self.imgPath = "-"
        else:
            mess = os.listdir(self.imgPath)
            # no images? clear that path + set cover img to "none"
            ctr = 0
            spare = -1
            for fn in mess:
                self.imgs.append(fn)
                # cover, title, frontispiece?
                if (("over" in fn) or ("ontis" in fn) or ("itle" in fn)):
                    if ((".png" in fn) or (".jpg" in fn)):
                        self.coverImgPath = ctr
                if ((".png" in fn) or (".jpg" in fn)):
                    spare = ctr
                ctr = ctr +1
            if (self.coverImgPath==-1 and spare!=-1):
                self.coverImgPath = spare
        return 0
        





#  zip -Xr9Dq D:/library/pythonic/pubs/The_Declaration_of_Independenc.epub . -i D:/library/pythonic/scratch/*

# mech for finding all records; iterator counter
# we don't have a dir for every integer, so 
# the index is not==GB book id; it's just a counter
# get the GB ID for the dir contents by 
# converting the dir's name to an int
class scanner:
    def __init__(self):
        self.dirIndex = 0
        self.allFiles = []
        self.counter = -1
        self.gbID = '-1'
        self.last = -1
        # find the top dir
        dir = "D:\\library\\gutenbergRecs\\cache\\epub"
        mess = [x[1] for x in os.walk(dir)]
        self.allFiles = mess[0]
        self.last = len(self.allFiles)
        print("found ", self.last, " records")
        if (self.last>0):
            self.counter = 1

    def skipTo(self, which):
        self.counter = which

    def getNextPath(self):
        res = ''
        dir = "D:\\library\\gutenbergRecs\\cache\\epub\\"
        if (self.counter!=-1 and self.counter<self.last):
            fls = self.allFiles[self.counter]
            self.gbID = fls  # fls is the dir name. fls!=counter !
            self.counter +=1
            res = dir + fls + "\\pg" + fls + ".rdf"
        else:
            self.counter = -1
        return res


class library:
    def __init__(self):
        self.scanner = scanner()
        self.results = []
        self.langs = []

    def readAll(self):
        notDone = True
        ctr = 1
        self.scanner.skipTo(ctr)
        while notDone:
            ctr = ctr +1
            #if (ctr>10000):
            #    notDone = False
            pt = self.scanner.getNextPath()
            if (len(pt)>0):
                if (not (".delete" in pt)):
                    booky = book()
                    booky.readGbXML(self.scanner.gbID, pt)
                    found = -1
                    for ct2 in range(0,len(self.langs)):
                        if (booky.language == self.langs[ct2]):
                            found = ct2
                    if (found!=-1):
                        self.results[found] += 1
                    else:
                        self.results.append(1)
                        self.langs.append(booky.language)
            if (ctr%5000==0):    
                for i in range(0,len(self.results)):
                    print(ctr, i, ":", self.langs[i], ":", self.results[i])
            
print("defined")

# formality: just do it. I guess. whatever. 
def main():
    lb = library()
    lb.readAll()

if __name__ == "__main__":   
    # calling main function 
    main() 

print("ok then")