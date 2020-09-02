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
        
