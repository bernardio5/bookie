import os

from classes.paths import paths
from classes.miniBook import miniBook
from classes.LOCdouble import LOCdouble


# one per single-letter LOC classification
class LOCsingle:
    def __init__(self, line):
        self.mark = line[0:1]
        self.description = line[2:] # text description of this order
        self.doubles = [] # list of LOCdoubles in 
        thePaths = paths()
        self.path = thePaths.htmlDir + "topics\\" + self.mark + ".html"
        self.link = self.mark + ".html"
        self.isNumbered = False
        if (self.mark=='E' or self.mark=='F'):
            self.isNumbered = True
        # nothing but this class needs to know about special treatment for E&F?


    def addDouble(self, line):
        d = LOCdouble(line)
        self.doubles.append(d)

    def matches(self, bk):
        for tp in bk.topics:
            if tp[0:1]==self.mark:
                return True
        return False                

    # letters other than E and F have a standard set of 2-letter codes. 
    # E and F are numbered, maybe standard, but not in a helpful way, so deal
    def maybeAddBook(self, bk):
        if (self.matches(bk)):
            if self.isNumbered: 
                newTopics = []
                for tp in bk.topics: # might need to add double for each topic
                    if tp[0:1]==self.mark:
                        isAdded = False
                        print("------------------- numbered topic: "+ tp)
                        for db in self.doubles:
                            if db.maybeAddEFBook(tp, bk): # could be an existing double
                                isAdded = True
                        if not isAdded: # didn't find one; add it
                            d = LOCdouble(tp)
                            d.addBook(tp, bk)
                            newTopics.append(d)
                for tp in newTopics:
                    self.doubles.append(tp)
            else:
                for db in self.doubles: # all available doubles premade
                    db.maybeAddBook(bk)

    def finishTopics(self):
        if self.isNumbered:
            self.doubles.sort(key = lambda x: x.mark)
            for db in self.doubles:
                print("numbered topic: "+ db.mark)
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
        file.write('<html><head><link rel="stylesheet" href="../styles.css"></head>')
        file.write("<body>")
        file.write('<h3>Topic Set ' + self.mark + ':' + self.description + '</h3>')
        file.write('<table>')
        file.write('<tr><td>Topic ID</td><td>Description</td><td># Books</td></tr>')
        for sn in self.doubles:
            sn.makeHTML()
            file.write('<tr><td>'+sn.mark+'</td><td><a href="' + sn.link + '">')
            file.write(sn.description + '</a></td><td>' + str(sn.bookCount()) +'</td></tr>')
        file.write("</table></body></html>")
        file.close() 
        
