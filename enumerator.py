import csv
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 
import zipfile
import numpy as np
import cv2
import random
import sys
# how to make a personal library with 40k books in it. 

# unix/cygwin command to pull the gutenberg directory tree from the "slow" server.
# note presence of 'excl.txt', which contains reg.expr for files to skip
#   mostly sound and CD/DVD data. We're here for books, mister. 
# rsync -av --exclude-from='excl.txt' --del ftp.ibiblio.org::gutenberg /cygdrive/d/gbg

# steps: scan gb records for each record:
#     read the record into a book object
# after all are scanned
# For each book
#   if neither .txt nor .htm, skip
#   scan the gbg data to see what you've got for it: .txt. htm, images, cover
#   make an epub!
#       in scratch/OEBPS/
#       use the .htm if there is one
#       ow make a content.html with all the text in a <PRE>       
#       if there's a cover, make the title.html with it
#       make content.opf
#       make toc.ncx
#       populate dir with .txt, cover, xml, htm, images

# these are not the most beautiful books ever. 
# eh, you can read them. 

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

    # hah, a book report
    def printSelf(self, ctr):
        try:
            print("count:", ctr)
            print("title:", self.title)
            print("   ID:", self.gutenId)
            print(" type:", self.type)
            for ath in self.auths:
                print(" auth:", ath.authTag())
            #for ath in self.trns:
            #    print(" trns:", ath.authTag())
            #fmts = "  fmt:"
            #for fm in self.formats:
            #    fmts += fm[-16:] + " - "
            #print(fmts)            
            #for fm in self.imgs:
            #    fmts += fm + " - "
            #print(fmts)            
            for fm in self.subjects:
                print(" subj:", fm)
            print(" txt:" + self.txtPath)    
            print(" htm:" + self.htmPath)
            print(" lang:", self.language)
        except:
            cnt=1; # don't care just keep your shit together bitch

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
        


    def writeContent(self):   
        res = 0;
        if (self.htmPath!="-"):
            targPath = "D:\\library\\pythonic\\scratch\\OEBPS\\content.xhtml"
            content = []
            try: 
                res = 6 # html w read err
                with open(self.htmPath) as f:
                    content = f.readlines()
                res = 7 # read ok, is html, no fix
                numLns = len(content)
                if (numLns>40):
                    numLns = 40
                for lnCt in range(0,numLns):
                    if ("/*" in content[lnCt]):
                        if ("*/" in content[lnCt]):
                            s1 = content[lnCt].find("/*")
                            s2 = content[lnCt].find("*/")
                            stra = content[lnCt][0:s1] + content[lnCt][s2+2:]
                            print(self.gutenId, ":fix:", content[lnCt], stra)
                            content[lnCt] = stra
                            res = 8 # html fixed
                with open(targPath, 'w') as outf:
                    for ln in content:
                        outf.write(ln)
                return res
            except:
                if os.path.isfile(self.htmPath):
                    res = 10 # html with unicode write issues
                    copyfile(self.htmPath, targPath)    
                return res
        if (self.txtPath=="-"):
            return 11 # no data, I guess. fuck off!
        html = ET.Element("html")
        html.set("xmlns", "http://www.w3.org/1999/xhtml")
        head = ET.SubElement(html, "head")
        title = ET.SubElement(head, "title")
        title.text = self.title
        link = ET.SubElement(head, "link")
        link.set('type', "text/css")
        link.set('rel', "stylesheet")
        link.set('href', "stylesheet.css")
        body = ET.SubElement(html, "body")
        # body.set("id", "startyStart") # so fucking do it you cunt. 
        pre = ET.SubElement(body, "pre")
        pre.set("id", "startyStart") # so fucking do it you cunt. 
        txf = open(self.txtPath, 'r+')
        try:
            wholeText = txf.read()
            pre.text = wholeText
            tree = ET.ElementTree(html)
            tree.write("D:\\library\\pythonic\\scratch\\OEBPS\\content.xhtml")
        except:
            return 15
        return 0



    # after you've read the XML and scanned the gbg, 
    # for each book, put in book opf, ncx, cover, htm
    # maybe mess with cover and formatting soonish.
    def scanHTML(self):
        # self.printSelf()
        if (self.type!="Text"):
            # print("not a Text", self.gutenId)
            return 12
        if (self.txtPath=="-" and self.htmPath=="-"):
            # print("no text", self.gutenId)
            return 13 # no book! skip
        if (len(self.title)<1):
            return 14 # no title? fuck you
        # write content
        return self.writeContent()


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
        self.counter = 1
        self.gbID = '-1'
        self.last = -1
        self.results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
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
        self.results = [0, 0, 0,  0, 0, 0,  0, 0, 0, 0,0,0, 0,0,0, 0]

    def readAll(self):
        notDone = True
        ctr = 1
        self.scanner.skipTo(ctr)
        while notDone:
            ctr = ctr +1
            if (ctr>12000):
                notDone = False
            pt = self.scanner.getNextPath()
            if (len(pt)>0):
                if (".delete" in pt):
                    self.results[3]+=1  # 3:delete in fn
                else:
                    booky = book()
                    booky.readGbXML(self.scanner.gbID, pt)
                    if (not booky.langOK()): 
                        self.results[1] +=1 # ch or cn
                    else:
                        res = booky.scanGBDir()
                        if (res!=0):
                            self.results[res] +=1  # 4,5 no dir, is sound
                        else:
                            res = booky.scanHTML()
                            self.results[res]+=1 
            else: 
                notDone = False
        for i in range(0,16):
            print(i, ":", self.results[i])

print("defined")

# formality: just do it. I guess. whatever. 
def main():
    lb = library()
    lb.readAll()

if __name__ == "__main__":   
    # calling main function 
    main() 

print("ok then")