

from classes.paths import paths
from classes.author import author
from classes.book import book
from classes.author import author



# first pass was unresponsive: too much data. 
# let's keep data in files so we can start and resume

#authors dirs is root/authors/first/firstsecond/
#    first contains two-letter pages
#    firstsecond contains author pages



class authorSet:
    def __init__(self):
        # maybe something more efficient, maybe just sit on yr hands.
        self.auths = []
        for i in range(0,36):
            self.auths.append([])

    def add(self, aut, gid):
        firsts = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        uppr = aut.name.upper()
        fc = firsts.find(uppr[0:1])
        if (fc==-1):
            print("AUTHOR NOT SORTABLE")
            return
        for a in self.auths[fc]:
            if a.matches(aut):
                a.workIds.append(gid)
                print('adding to', a.name)
                return
        newAut = aut.duplicate()
        newAut.workIds = [gid]
        self.auths[fc].append(newAut)
        print('added new author', newAut.name)

    def makeHTMLs(self, titleService):
        firsts = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        fl = len(firsts)
        thePaths = paths()
        for i in range(0, fl):
            letter = firsts[i:i+1]
            pt = thePaths.htmlDir + "\\authors\\" + letter + ".html"
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
            pt = thePaths.htmlDir + "\\authors\\" + letter + "\\"
            if not os.path.exists(pt):
                os.makedirs(pt)
            for at in self.auths[i]:
                htpt = at.htmlPath()
                file = open(htpt, "w") 
                file.write("<!DOCTYPE html>")
                file.write("<html>")
                file.write("<body>")
                file.write('<h3>Author Page for ' + at.name + '</h3>')
                file.write('<h4>' + at.birth + "-" + at.death + '</h4>')
                file.write('<h4><a href="' + at.wikiLink + '">Wikipedia page' + '</a></h4>')
                file.write('<h4>Books:</h4>')
                thePaths = paths()
                for bid in at.workIds:
                    minib = titleService.lookupID(bid)
                    file.write('<a href="../../' + minib.htmlRelativePath + '">' + bid + ':' + minib.title + '</a></br>')
                file.write("</body>")
                file.write("</html>")
                file.close() 

