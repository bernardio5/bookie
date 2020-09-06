

from classes.paths import paths
from classes.author import author
from classes.book import book
from classes.author import author



# first pass was unresponsive: too much data. 
# let's keep data in files so we can start and resume

#authors dirs is root/authors/first/firstsecond/
#    first contains two-letter pages
#    firstsecond contains author pages

import os
from classes.paths import paths
from classes.miniBook import miniBook
from classes.titleSet import titleSet


class authorSet:
    def __init__(self):
        # maybe something more efficient, maybe just sit on yr hands.
        self.auths = []
        self.thePaths = paths()
        self.allowedTags = []
        for i in range(0,26):
            self.auths.append([])
            self.allowedTags.append([])

    def add(self, aut, gid):
        firsts = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        uppr = aut.name.upper()
        fc = firsts.find(uppr[0:1])
        if (fc==-1):
            print("AUTHOR NOT SORTABLE")
            return
        for a in self.auths[fc]:
            if a.matches(aut):
                a.workIds.append(gid)
                # print('adding to', a.name)
                return
        newAut = aut.duplicate()
        newAut.workIds = [gid]
        ntag = newAut.authTag()
        nas = len(self.auths[fc])
        for i in range(0,nas):
            ob1 = self.auths[fc][i]
            if (ob1.authTag()>ntag):
                self.auths[fc].insert(i, newAut)
                return
        self.auths[fc].append(newAut)
        # print('added new author', newAut.name)

    def makeHTMLs(self, aTitleSet):
        pt = self.thePaths.htmlDir + "authors\\"
        if not os.path.exists(pt):
            os.makedirs(pt)
        firsts = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        fl = len(firsts)
        for i in range(0, fl):
            letter = firsts[i:i+1]
            pt = self.thePaths.htmlDir + "\\authors\\" + letter + ".html"
            file = open(pt, "w") 
            file.write("<!DOCTYPE html>")
            file.write("<html>")
            file.write("<body>")
            file.write('<h3>Page for ' + letter + ' authors</h3>')
            file.write('<h4>Authors:</h4>')
            for at in self.auths[i]:
                file.write('<a href="' + letter + '/' + at.authTag() + '.html">' + at.name + '</a><br/>')
            file.write("</body>")
            file.write("</html>")
            file.close() 
            pt = self.thePaths.htmlDir + "\\authors\\" + letter + "\\"
            if not os.path.exists(pt):
                os.makedirs(pt)
            for at in self.auths[i]:
                print("make auth:", at.name)
                htpt = at.htmlPath()
                file = open(htpt, "w") 
                file.write("<!DOCTYPE html>")
                file.write("<html>")
                file.write("<body>")
                file.write('<h3>Author Page for ' + at.name + '</h3>')
                file.write('<h4>' + at.birth + "-" + at.death + '</h4>')
                file.write('<h4><a href="' + at.wikiLink + '">Wikipedia page' + '</a></h4>')
                file.write('<h4>Books:</h4>')
                for bid in at.workIds:
                    minib = aTitleSet.lookupID(bid)
                    file.write('<a href="../../' + minib.htmlRelativePath + '">' + bid + ':' + minib.title + '</a></br>')
                file.write("</body>")
                file.write("</html>")
                file.close() 


    # filtering by author; add whole name to help me out
    def makeAuthorList(self):
        file = open("authorList.txt", "w") 
        firsts = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        fl = len(firsts)
        for i in range(0, fl):
            letter = firsts[i:i+1]
            for at in self.auths[i]:
                file.write(at.authTag() + ' ' + at.name + ', ' + str(at.birth) + '-' + str(at.death))
        file.close() 

    def loadAllowedAuthors(self):
        firsts = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        file = open("authorList.txt" + "LOCfams.txt", "r") 
        lines = file.readlines() 
        file.close()
        for ln in lines:
            spp = ln.find(' ')
            tag = ln[0:spp]
            fc = ln[0:1]
            fci = firsts.find(fc)
            if (fci!=-1):
                self.alloweds[fci].append(tag)
    
    def hasAllowedAuthor(self, minib):
        firsts = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for aut in minib.authors:
            tg = aut.authorTag()
            fc = ln[0:1]
            fci = firsts.find(fc)
            if (fci==-1):
                return False
            if (tg in self.alloweds[fci]):
                return True
        return False

