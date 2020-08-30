import os
import sys
from shutil import copyfile
import xml.etree.ElementTree as ET 
import math
from classes.paths import paths
from classes.book import book
from classes.scanner import scanner


# as LOCcats, but with state stored in files in the directory tree





class LOCtitleSet:
    def __init__(self):
        self.books = []

    def add(self, minib):
        self.books.append(minib.duplicate())

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
        for bk in self.books:
            bk.makeHTML()

    def makeTitleHTML(self):
        # sort books by brutalTitleAB
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
            for j in range(0,fl):
                letter2 = firsts[j:j+1]
                file.write('<td><a href="' + letter + '/' + letter + letter2 + '.html">' + letter+letter2 + '</a></td>')
                if ctr%6==5:
                    file.write('</tr><tr>')
                ctr = ctr+1
            file.write("</tr></table></body></html>")
            file.close() 
        self.books.sort(key = lambda x: x.brutalTitleAB)
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




# will have one of these per book, stored in a gid-indexed array,
# and, multiply, in the order/fam/gen tree
class LOCminiBook:
    def __init__(self):
        self.authors = []
        self.title = ""
        self.topics = []
        self.lcc = "-"
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
        res = LOCminiBook()
        for a in self.authors:
            res.authors.append(a.duplicate())
        res.title = self.title
        for t in self.topics: 
            res.topics.append(t)
        res.lcc = self.lcc
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
            for s in fullbook.subjects:
                if (s.find("LCC: ")!=-1):
                    if (self.lcc!="-"):
                        print("multiple LCCs!")
                    self.lcc = s[5:]
                    self.valid = True
                if (s.find("LCSH: ")!=-1):
                    tpc = s[6:]     # self.topics only contains LCSH strings.
                    self.topics.append(tpc)
                    self.valid = True
            thePaths = paths()
            digits = '%05d' % int(self.gutenId)
            self.dir = thePaths.htmlDir + "\\books\\" + digits[0:1] + "\\" + digits[1:3] + "\\" + digits[3:] + "\\"
            self.htmlRelativePath = "books/" + digits[0:1] + "/" + digits[1:3] + "/" + digits[3:] + "/" + "index.html"
            brute = self.title.upper()
            if (len(brute)<1):
                return "A"
            alloweds = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890"
            for i in range(0,len(brute)):
                if (len(brute)<=i):
                    return brute
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
            print("brutal", okwords, self.brutalTitleA, self.brutalTitleAB)
            
        if (self.title.find("Punchinello")!=-1):
            self.valid = False # seriously: *fuck* those guys

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
        fromPt = thePaths.scratchDir + "OEBPS\\cover.png"
        toPt = targetDir + "\\cover.png"
        # print('copying fromto', fromPt, toPt)
        if os.path.isfile(fromPt):
            copyfile(fromPt, toPt)

    def recitation(self):
        print("      --", self.title)

    def listRecitation(self):
        print(self.title, " gid:", self.gutenId, "LCC:", self.lcc )
        for s in self.topics:
            print("  ", s)

    def makeHTML(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        pt = self.dir + "index.html"
        file = open(pt, "w") 
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write("<body>")
        file.write('<img src="cover.png"/><br/>')
        file.write('<h3>Book Page for ' + self.title + ': <a href="' + self.bookTag+ '.epub">Download</a></h3>')
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




# one per text-described topic in two-letter genus
class LOCtopic: 
    def __init__(self):
        self.doubleMark = "AB"
        self.mark = "AB.F00F" # mark of owner Family + self's number
        self.description = "F00F" # text description of self
        self.books = [] # all the books in the topic
        self.dirPath = "\\"     
        self.htmlRelativePath = ""
        
    def matches(self, bk):
        res = False
        for sb in bk.topics:
            if (sb==self.description):
                res = True
        return res

    def maybeAddBook(self, bk): 
        res = False
        if (self.matches(bk)):
            self.books.append(bk.duplicate())
            res = True
        return res

    def bookCount(self):
        return len(self.books)

    def setFromBook(self, dblMark, subj, bk): 
        self.doubleMark = dblMark
        self.description = subj
        self.books.append(bk.duplicate())
        self.setStdMark()

    def brutalDescription(self):
        brute = self.description.upper()
        if (len(brute)<1):
            return "A"
        alloweds = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        for i in range(0,len(brute)):
            if (len(brute)<=i):
                return brute
            # print("brutal:", i, brute, brute[i])
            if (alloweds.find(brute[i])==-1):
                brute = brute.replace(brute[i], "")
            
        return brute

    def setStdMark(self):
        desc = self.brutalDescription()
        thePaths = paths()
        self.dirPath = thePaths.htmlDir + "topics\\" + self.doubleMark + "\\"     
        self.mark = self.doubleMark + "." + desc[0:5]
        self.link = self.mark + ".html"

    def markLessThan(self, otherTopic):
        return self.mark < otherTopic.mark

    def marksEqual(self, otherTopic):
        return self.mark == otherTopic.mark

    def setAltMark(self, dupe):
        # find first char where self.desc and dupe differ
        notDone = True
        brute = self.brutalDescription()
        othBrute = dupe.brutalDescription()
        pl = 5
        while notDone and pl<len(brute)-3:
            c1 = brute[pl:pl+1]
            c2 = othBrute[pl:pl+1]
            if (c1==c2):
                pl = pl +1
            else:
                notDone = False
        p2 = pl + 3
        if p2>len(brute):
            p2 = len(brute)
        thePaths = paths()
        self.dirPath = thePaths.htmlDir + "topics\\" + self.doubleMark + "\\"     
        self.mark = self.doubleMark + "_" + brute[0:5] + brute[pl:p2]
        self.link = self.mark + ".html"

    def htmlRelativePath(self):
        return "topics/" + self.doubleMark + "/" + self.mark + ".html"

    def recitation(self):
        print("   ", self.doubleMark, " ", self.description, " count:", len(self.books))
        for b in self.books:
            b.recitation()
        return len(self.books)

        # want books in topic, related topics, link up, link down
    def makeHTML(self):
        if not os.path.exists(self.dirPath):
            os.makedirs(self.dirPath)
        htpt = self.dirPath + self.link
        file = open(htpt, "w") 
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write("<body>")
        file.write('<h3>' + self.mark + ':' + self.description + '</h3>')
        file.write('<h4><a href="../' + self.doubleMark + '.html">Up to classification ' + self.doubleMark + '</h3>')
        file.write('<h4>' + str(len(self.books)) + ' Book(s):</h4>')
        for bk in self.books:
            file.write('<a href="../../' + bk.htmlRelativePath + '">')
            file.write(bk.gutenId + ':' +bk.title + '</a><br/>')
        file.write("</body>")
        file.write("</html>")
        file.close() 


# one per two-letter LOC classification (or 1+number, for E & F)
class LOCdouble: 
    def __init__(self, line):
        # oh, nope. marks can be more than 2 chars. 
        spot = line.find(' ')  # the letters of
        self.mark = line[0:spot]
        self.description =line[(spot+1):]
        thePaths = paths()
        self.link = self.mark + ".html"
        self.path = thePaths.htmlDir + "\\topics\\" + self.mark + ".html"
        self.subDir = thePaths.htmlDir + "\\topics\\" + self.mark + "\\"
        self.topics = []

    # given a subject description string, return -1 for can't find, or an index? what. 
    def matches(self, bk):
        booksMark = bk.lcc[0:2]
        if (self.mark==booksMark):
            return True
        return False

    def maybeAddBook(self, bk):
        toAppend = []
        if (self.matches(bk)):
            hasMatch = False
            # if self.topics is empty, just add all the book's topics
            if (len(self.topics)==0):
                for btp in bk.topics:
                    newt = LOCtopic()
                    newt.setFromBook(self.mark, btp, bk)
                    self.topics.append(newt)
            else:
                # otherwise, for each book topic, maybe add to existing
                toAppend = []
                notAdded = True
                for tpc in self.topics:
                    if tpc.maybeAddBook(bk):
                        notAdded = False
                # add new LOC topics for all book topics for all books that didn't find a match
                if notAdded:
                    for tp in bk.topics:
                        newt = LOCtopic()
                        newt.setFromBook(self.mark, tp, bk)
                        self.topics.append(newt)

    def bookCount(self):
        tot = 0
        for tp in self.topics:
            tot += tp.bookCount()
        return tot

    def finishTopics(self):
        self.topics.sort(key = lambda x: x.mark)
        lg = len(self.topics)
        someChanged = False
        for i in range(0,lg-1):
            t1 = self.topics[i]
            k=-1
            for j in range(i+1, lg):
                t2 = self.topics[j]
                if t1.marksEqual(t2):
                    k=j
            if k!=-1:
                someChanged = True
                self.topics[i].setAltMark(self.topics[i+1])
                for n in range(i+1, k):
                    self.topics[n].setAltMark(self.topics[i])
        if someChanged:
            self.topics.sort(key = lambda x: x.mark)

    def recitation(self):
        print(self.mark, " -- ", self.description, " topics " + str(len(self.topics)))
        for t in self.topics:
            t.recitation()
        
    def makeHTML(self):
        file = open(self.path, "w") 
        if not os.path.exists(self.subDir):
            os.makedirs(self.subDir)
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write('<link rel="stylesheet" href="styles.css">')
        file.write("<body>")

        file.write('<h3>' + self.mark + ':' + self.description + '</h3>')
        file.write('<h4><a href="' + self.mark[0:1] + '.html">Up to classification ' + self.mark[0:1] + '</a></h4>')
        file.write('<h4>' + str(self.bookCount()) + ' Book(s) in ' + str(len(self.topics)) + ' Subtopic(s):</h4>')
        file.write('<table>')
        file.write('<tr><td>Topic ID</td><td>Description</td><td># Books</td></tr>')
        
        for sn in self.topics:
            sn.makeHTML()
            file.write('<tr><td>'+ sn.mark +'</td><td><a href="'+self.mark + "/" + sn.link + '">')
            file.write(sn.description + '</td><td>' + str(sn.bookCount()) + '</td></tr>')
        file.write("</body>")
        file.write("</html>")
        file.close() 
        

# one per single-letter LOC classification
class LOCsingle:
    def __init__(self, line):
        self.mark = line[0:1]
        self.description = line[2:] # text description of this order
        self.doubles = [] # list of LOCdoubles in 
        thePaths = paths()
        self.path = thePaths.htmlDir + "topics\\" + self.mark + ".html"
        self.link = self.mark + ".html"

    def addDouble(self, line):
        d = LOCdouble(line)
        self.doubles.append(d)

    def matches(self, bk):
        booksMark = bk.lcc[0:1]
        if (self.mark==booksMark):
            return True
        return False

    def maybeAddBook(self, bk):
        if (self.matches(bk)):
            for db in self.doubles:
                db.maybeAddBook(bk)

    def finishTopics(self):
        for db in self.doubles:
            db.finishTopics()

    def recitation(self):
        print(self.mark + " -- " + self.description)
        print(" doubles contained: " + str(len(self.doubles)))
        for d in self.doubles:
            d.recitation()
        
    def makeHTML(self):
        file = open(self.path, "w") 
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write("<body>")
        file.write('<h3>' + self.mark + ':' + self.description + '</h3>')
        file.write('<table>')
        file.write('<tr><td>Topic ID</td><td>Description</td><td># Books</td></tr>')
        for sn in self.doubles:
            sn.makeHTML()
            file.write('<tr><td>'+sn.mark+'</td><td><a href="' + sn.link + '">')
            file.write(sn.description + '</a></td><td>' + str(sn.bookCount()) +'</td></tr>')
        file.write("</table></body></html>")
        file.close() 
        


# all of the orders/families/topics; all of the books. 
class LOCtree:
    def __init__(self):        
        self.thePaths = paths()
        self.singles = []
        file = open(self.thePaths.dataDir + "LOCfams.txt", "r") 
        lines = file.readlines() 
        for ln in lines:
            if ln[1] == ' ':
                ord = LOCsingle(ln)
                self.singles.append(ord)
            else: 
                ord.addDouble(ln)

    def addBook(self, book):
        for sn in self.singles:
            sn.maybeAddBook(book)

    def finishTopics(self):
        for sn in self.singles:
            sn.finishTopics()

    def recitation(self):
        print("------------------")
        for s in self.singles:
            s.recitation()

    def makeHTML(self, bookCt):
        targ = self.thePaths.htmlDir + "index.html"
        file = open(targ, "w") 
        file.write("<!DOCTYPE html>")
        file.write("<html>")
        file.write("<body>")
        file.write("<h2>A library of " + bookCt + " volumes:</h2>")
        file.write("<h3>Subjects</h3><table><tr>")
        ctr = 0
        for sn in self.singles:
            sn.makeHTML()
            file.write('<td><a href="topics/' + sn.link + '">')
            file.write(sn.mark + ':' +sn.description + '</a></td>')
            if (ctr%3==2):
                file.write('</tr><tr>')
            ctr =ctr+1
        file.write("</tr></table><h3>Authors</h3><table><tr>")
        ctr = 0
        abc  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        abln = len(abc)
        for i in range(0, abln):
            lt = abc[i:i+1]
            file.write('<td><a href="authors/' + lt + '.html">' + lt + '</a></td>')
            if (ctr%6==5):
                file.write('</tr><tr>')
            ctr =ctr+1
        file.write("</tr></table><h3>Titles</h3><table><tr>")
        ctr = 0
        for i in range(0, abln):
            lt = abc[i:i+1]
            file.write('<td><a href="titles/' + lt + '.html">' + lt + '</a></td>')
            if (ctr%6==5):
                file.write('</tr><tr>')
            ctr =ctr+1
        file.write("</tr></table></body></html>")
        file.close() 



class library:
    def __init__(self):
        self.scanner = scanner()
        self.thePaths = paths()
        self.theTree = LOCtree()
        self.bookList = LOCtitleService()
        self.covers = os.listdir(self.thePaths.coversDir)
        self.clips = os.listdir(self.thePaths.clipDir)
        self.authorSet = LOCauthorSet()

    # traverse all books
    def buildCats(self):
        nco = len(self.covers)
        ncl = len(self.clips)
        notDone = True
        ctr = 1
        self.scanner.skipTo(ctr)
        while notDone:
            ctr = ctr +1
            #if (ctr>150): # comment out to do all books
            #   notDone = False
            pt = self.scanner.getNextPath()
            if (len(pt)>0 and not (".delete" in pt)):
                # read in the book if you can
                fullbook = book()
                fullbook.readGbXML(self.scanner.gbID, pt)
                print(fullbook.title)
                if fullbook.isValid():
                    minibook = LOCminiBook()
                    minibook.makeFromBigBook(fullbook)
                    if (minibook.valid):
                        self.bookList.add(minibook)
                        self.theTree.addBook(minibook)
                        coverImg = self.covers[ctr%nco]
                        clipImg = self.clips[(ctr+500)%ncl]
                        if (fullbook.makeEpub(coverImg, clipImg)==1):
                            minibook.arrangeBigBook(fullbook)
                            # for each author, add to auth list.
                            for aut in fullbook.auths:
                                self.authorSet.add(aut, fullbook.gutenId)


    def recitation(self):
        print("book list by gid:   -------------------------------------")
        for b in self.gidList:
            b.listRecitation()
        print("tree:               -------------------------------------")
        self.theTree.recitation()


    def makeHTML(self):
        pt = self.thePaths.htmlDir + "topics\\"
        if not os.path.exists(pt):
            os.makedirs(pt)
        self.theTree.finishTopics()
        self.theTree.makeHTML(str(self.bookList.count()))     # make html for topics
        pt = self.thePaths.htmlDir + "books\\"
        if not os.path.exists(pt):
            os.makedirs(pt)
        self.bookList.makeGIDHTML()
        pt = self.thePaths.htmlDir + "titles\\"
        if not os.path.exists(pt):
            os.makedirs(pt)
        self.bookList.makeTitleHTML()
        pt = self.thePaths.htmlDir + "authors\\"
        if not os.path.exists(pt):
            os.makedirs(pt)
        self.authorSet.makeHTMLs(self.bookList)  # authors

print("defined")

# everything defines ok; run it
def main():
    lb = library()
    lb.buildCats()
    lb.makeHTML()

if __name__ == "__main__":   
    main() 

print("ok then")