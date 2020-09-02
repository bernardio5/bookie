import os

from classes.paths import paths
from classes.miniBook import miniBook

# one per text-described topic in two-letter genus
class LOCtopic: 
    def __init__(self):
        self.doubleMark = "AB"
        self.mark = "AB.F00F" # mark of owner Family + self's number
        self.description = "F00F" # text description of self
        self.books = [] # all the books in the topic
        self.dirPath = "\\"     
        self.htmlRelativePath = ""
        

    def maybeAddBook(self, tp, bk): 
        res = False
        if (tp==self.description):
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
        self.htmlRelativePath = "topics/" + self.doubleMark + "/" + self.mark + ".html"

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
        self.htmlRelativePath = "topics/" + self.doubleMark + "/" + self.mark + ".html"


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
        file.write('<h3> Topic page for:' + self.mark + ':' + self.description + '</h3>')
        file.write('<h4><a href="../' + self.doubleMark + '.html">Up to classification ' + self.doubleMark + '</h3>')
        file.write('<h4>' + str(len(self.books)) + ' Book(s):</h4>')
        for bk in self.books:
            file.write('<a href="../../' + bk.htmlRelativePath + '">')
            file.write(bk.gutenId + ':' +bk.title + '</a><br/>')
        file.write("</body>")
        file.write("</html>")
        file.close() 
