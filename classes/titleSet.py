import os
import sys

from shutil import copyfile
from classes.paths import paths
from classes.miniBook import miniBook


class titleSet:
    def __init__(self):
        self.books = []
        self.thePaths = paths()

    def add(self, minib):
        nbks = len(self.books)
        for i in range(0,nbks):
            ob1 = self.books[i]
            if (minib.brutalLessThan(ob1)):
                self.books.insert(i, minib.duplicate())
                return
        self.books.append(minib)


    def count(self):
        return len(self.books)

    # sort, binary search: premature optimization
    def lookupTitle(self, title):
        for ts in self.books:
            if ts.full==title:
                return ts

    def lookupID(self, gid):
        for ts in self.books:
            if ts.gutenId==gid:
                return ts

    def makeGIDHTML(self):
        pt = self.thePaths.htmlDir + "books\\"
        if not os.path.exists(pt):
            os.makedirs(pt)
        for bk in self.books:
            bk.makeHTML()

    def makeTitleHTML(self):
        pt = self.thePaths.htmlDir + "titles\\"
        if not os.path.exists(pt):
            os.makedirs(pt)
        firsts = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        fl = len(firsts)
        thePaths = paths()
        for i in range(0, fl):
            letter = firsts[i:i+1]
            pt = thePaths.htmlDir + "\\titles\\" + letter + ".html"
            file = open(pt, "w") 
            file.write("<!DOCTYPE html>")
            file.write("<html>")
            file.write("<body>")
            file.write('<h3>Page for ' + letter + ' titles:</h3><table><tr>')
            ctr = 0;
            for j in range(0,fl-10):
                letter2 = firsts[j:j+1]
                file.write('<td><a href="' + letter + '/' + letter + letter2 + '.html">' + letter+letter2 + '</a></td>')
                if ctr%6==5:
                    file.write('</tr><tr>')
                ctr = ctr+1
            file.write("</tr></table></body></html>")
            file.close() 
        oldMark = "INIT"
        file = 0
        for bk in self.books:
            if len(bk.titlePath)>0:
                if (bk.brutalTitleAB != oldMark):
                    if oldMark!="INIT":
                        file.write("</body>")
                        file.write("</html>")
                        file.close() 
                    oldMark = bk.brutalTitleAB
                    if not os.path.exists(bk.titlePath):
                        os.makedirs(bk.titlePath)
                    pt = bk.titlePath  + bk.brutalTitleAB + ".html"
                    file = open(pt, "w") 
                    file.write("<!DOCTYPE html>")
                    file.write("<html>")
                    file.write("<body>")
                    file.write('<h3>Titles Page for ' + bk.brutalTitleAB + ':</h3>')
                file.write('<a href="../../' + bk.htmlRelativePath + '">' + bk.title + '</a><br/>' )

    def makeBookList(self):
        file = open("bookList.txt", "w") 
        for bk in self.books:
            bk.lister(file)
        file.close() 



