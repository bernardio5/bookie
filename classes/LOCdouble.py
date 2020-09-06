import os

from classes.paths import paths
from classes.LOCtopic import LOCtopic
from classes.miniBook import miniBook

# one per two-letter LOC classification (or 1+number, for E & F)
class LOCdouble: 
    def __init__(self, line):
        # oh, nope. marks can be more than 2 chars. 
        spot = line.find(' ')  # the letters of
        self.mark = line[0:spot]
        self.description = line[(spot+1):]
        thePaths = paths()
        self.link = self.mark + ".html"
        self.path = thePaths.htmlDir + "\\topics\\" + self.mark + ".html"
        self.subDir = thePaths.htmlDir + "\\topics\\" + self.mark + "\\"
        self.topics = []


    def addBook(self, bookTopic, book):
        newt = LOCtopic()
        newt.setFromBook(self.mark, bookTopic, book)
        self.topics = [newt]



    def matches(self, bk):
        for tp in bk.topics:
            spot = tp.find(' ')  
            tmark = tp[0:spot]
            if (self.mark==tmark):
                return True
        return False


    def topicIn(self, tp):
        spot = tp.find(' ')  
        tmark = tp[0:spot]
        return self.mark==tmark

    # at least one topic in this double. for each one in, 
    # either add to existing or make new
    def maybeAddBook(self, bk):
        for tp in bk.topics:
            if (self.topicIn(tp)):
                notAdded = True
                for tpc in self.topics:
                    if tpc.maybeAddBook(tp, bk):
                        notAdded = False
                if notAdded:
                    newt = LOCtopic()
                    newt.setFromBook(self.mark, tp, bk)
                    self.topics.append(newt)


    # add book topics in self to existing or new.
    def maybeAddEFBook(self, tp, bk):    
        res = False     
        if (self.topicIn(tp)):    
            notAdded = True
            for tpc in self.topics:
                if tpc.maybeAddBook(tp, bk):
                    notAdded = False
                    res = True
            if notAdded:
                newt = LOCtopic()
                newt.setFromBook(self.mark, tp, bk)
                self.topics.append(newt)
                res = True
        return res


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
        file.write('<tr><td>Topic Description</td><td># Books</td></tr>')
        
        for sn in self.topics:
            sn.makeHTML()
            file.write('<tr><td><a href="'+self.mark + "/" + sn.link + '">')
            file.write(sn.description + '</td><td>' + str(sn.bookCount()) + '</td></tr>')
        file.write("</body>")
        file.write("</html>")
        file.close() 
        
