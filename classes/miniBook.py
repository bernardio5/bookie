import os
import sys


from shutil import copyfile

from classes.paths import paths
from classes.book import book


class miniBook:
    def __init__(self):
        self.authors = []
        self.title = ""
        self.topics = []
        self.gutenId = 0
        self.valid = False
        self.dir = ""
        self.htmlRelativePath = ""
        self.brutalTitle = ""
        self.brutalTitleA = ""
        self.brutalTitleAB = ""
        self.titlePath = ""
        self.bookTag = ""

    def duplicate(self):
        res = miniBook()
        for a in self.authors:
            res.authors.append(a.duplicate())
        res.title = self.title
        for t in self.topics: 
            res.topics.append(t)
        res.gutenId = self.gutenId
        res.valid = self.valid
        res.dir = self.dir 
        res.htmlRelativePath = self.htmlRelativePath
        res.brutalTitle = self.brutalTitle
        res.brutalTitleA = self.brutalTitleA
        res.brutalTitleAB = self.brutalTitleAB
        res.titlePath = self.titlePath
        res.bookTag = self.bookTag
        return res


    def makeFromBigBook(self, fullbook):
        if (fullbook.langOK() and fullbook.scanGBDir()==0):
            for a in fullbook.auths:
                self.authors.append(a.duplicate())
            self.title = fullbook.title
            self.gutenId = fullbook.gutenId
            lcc = ""
            hasLCSH = False
            for s in fullbook.subjects:
                if (s.find("LCC: ")!=-1 and lcc==""):
                    lcc = s[5:]
                if (s.find("LCSH: ")!=-1 ):
                    hasLCSH = True
            if (hasLCSH and lcc!=""):
                self.valid = True
            for s in fullbook.subjects:
                if (s.find("LCC: ")!=-1):
                    lcc = s[5:]
                if (s.find("LCSH: ")!=-1):
                    tpc = lcc + ' ' + s[6:]     # self.topics only contains LCSH strings.
                    self.topics.append(tpc)
                su = s.upper()
                if (su.find("JUVENILE")!=-1):
                    self.valid = False 
                if (su.find("CHILDREN")!=-1):
                    self.valid = False # the adult content is maudlin enough
                if (su.find("PERIODICAL")!=-1):
                    self.valid = False
            thePaths = paths()
            digits = '%05d' % int(self.gutenId)
            self.dir = thePaths.htmlDir + "\\books\\" + digits[0:1] + "\\" + digits[1:3] + "\\" + digits[3:] + "\\"
            self.htmlRelativePath = "books/" + digits[0:1] + "/" + digits[1:3] + "/" + digits[3:] + "/" + "index.html"
            brute = self.title.upper()
            if (len(brute)<1):
                brute = "A"
            alloweds = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890"
            for i in range(0,len(brute)):
                if (len(brute)>i):
                    if (alloweds.find(brute[i])==-1):
                        brute = brute.replace(brute[i], "")            
            words = brute.split(' ')
            okwords = ""
            for w in words:
                if w!="A" and w!="AN" and w!="THE":
                    if len(okwords)>0:
                        okwords = okwords + "_"
                    okwords = okwords + w
            self.brutalTitle = okwords
            self.brutalTitleA = okwords[0:1]
            self.brutalTitleAB = okwords[0:2]
            self.titlePath = thePaths.htmlDir + "\\titles\\" + self.brutalTitleA + '\\' 
            self.bookTag = fullbook.safeFn(fullbook.bookTag())
            # print(self.gutenId, okwords, self.brutalTitleA, self.brutalTitleAB)
            if (self.brutalTitle.find("PUNCHINELLO")!=-1):
                self.valid = False 
            if (self.brutalTitle.find("CHARIVARI")!=-1):
                self.valid = False # seriously: *fuck* those guys
            if (self.brutalTitle.find("MISSIONARY")!=-1):
                self.valid = False 
            if (fullbook.language.find("en")==-1):
                self.valid = False # English only for now


    def brutalLessThan(self, otherB):
        return self.brutalTitle < otherB.brutalTitle


    def arrangeBigBook(self, fullbook): 
        # print("made pub")
        targetDir = self.dir
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        src_files = os.listdir(targetDir) # clear out dir
        for fn in src_files:
            pt = targetDir + "\\" + fn
            if os.path.isfile(pt):
                os.remove(pt)
        # move book to self's HTML dir stack
        fromPt = fullbook.bookPath
        toPt = targetDir + "\\" + fullbook.safeFn(fullbook.bookTag()) + ".epub"
        # print('copying fromto', fromPt, toPt)
        if os.path.isfile(fromPt):
            copyfile(fromPt, toPt)
            os.remove(fullbook.bookPath)
        # and then add the book's html
        #  minibook.makeHTML()
        #   actually not yet; topics aren't finished
        # copy cover image over, too
        thePaths = paths()
        fromPt = thePaths.scratchDir + "OEBPS\\cover.jpg"
        toPt = targetDir + "\\cover.jpg"
        # print('copying fromto', fromPt, toPt)
        if os.path.isfile(fromPt):
            copyfile(fromPt, toPt)


    def copyText(self, fullbook): 
        # print("made pub")
        targetDir = self.dir
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        src_files = os.listdir(targetDir) # clear out dir
        for fn in src_files:
            pt = targetDir + "\\" + fn
            if os.path.isfile(pt):
                os.remove(pt)
        # move book to self's HTML dir stack
        fromPt = fullbook.txtPath
        self.bookTag = fullbook.safeFn(fullbook.bookTag())
        toPt = targetDir + "\\" + self.bookTag + ".txt"
        # print('copying fromto', fromPt, toPt)
        if os.path.isfile(fromPt):
            copyfile(fromPt, toPt)
  

    def recitation(self):
        print("      --", self.title)


    def lister(self, file):
        at = ""
        if (len(self.authors)>0):
            at = self.authors[0].name
        file.write(self.gutenId+', "'+ self.title +'", "' + at + '"\n')


    def makeHTML(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        pt = self.dir + "index.html"
        file = open(pt, "w") 
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write("<body>")
        file.write('<img src="cover.jpg"/><br/>')
        file.write('<h3>Book Page for ' + self.title + ':<a href="' + self.bookTag+ '.epub">Download</a></h3>')
        # file.write('<h4>View: <a href="' +  self.bookTag + '.txt">Link</a></h4>')
        file.write('<h4>Authors:</h4>')
        for at in self.authors:
            fs = at.name[0:1]
            tg = at.authTag()
            file.write('<a href="../../../../' + at.htmlRelativePath() + '">' + at.name + '</a><br/>')
        file.write('<h4>Topics:</h4>')
        for tp in self.topics:
            file.write(tp + '<br/>')
        file.write("</body>")
        file.write("</html>")
        file.close() 



