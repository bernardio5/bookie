
import os

from classes.paths import paths
from classes.miniBook import miniBook
from classes.LOCsingle import LOCsingle

# trees contain singles; singles contain doubles, doubles contain topics, topics contain minibooks. 

# use the two-letter classifications to reduce the # topics to deal with at once. 
# make a web page for each two-letter topic list. 
# make a link for each topic & index so links can be built. 

# topics are hashed; each has a unique mark that serves for HTML file names & links. 
# the hash can't be unique until all are known, so call "finish topics" after adding all books
# and before using HTML links


class LOCtree:
    def __init__(self):        
        self.thePaths = paths()
        self.singles = []
        file = open(self.thePaths.dataDir + "LOCfams.txt", "r") 
        # make all singles and all doubles not in e or f
        lines = file.readlines() 
        for ln in lines:
            if ln[1] == ' ':
                ord = LOCsingle(ln)
                self.singles.append(ord)
            else: 
                ord.addDouble(ln)

    def addBook(self, minib):
        for sn in self.singles:
            sn.maybeAddBook(minib)

    def finishTopics(self):
        for sn in self.singles:
            sn.finishTopics()

    def recitation(self):
        print("------------------")
        for s in self.singles:
            s.recitation()

    def makeHTML(self, bookCt):
        pt = self.thePaths.htmlDir + "topics\\"
        if not os.path.exists(pt):
            os.makedirs(pt)
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