import csv
import os
from shutil import copyfile

# This class takes a text file and turns it into a set of interlinked
# HTML files, each w/ ~1000 lines of text. 

# To use: create an instance, giving the name of the file and the directory it's in. 
# Then call "output()". Bang, new files. 
# Expects a stylesheet at the root-level books dir. 

class textWrapper:
    def __init__(self, source, titleIn, targetDir):
        self.volumeCounter = 0  # one HTML per volume; about 500 lines? 
        self.minLinesPerVolume = 2000

        self.title = titleIn
        self.targetDir = targetDir

        self.lines = []     # the book's lines of text
        txf = open(source, 'r+', errors="ignore")
        self.lines = txf.read().split('\n')
        self.lineCount = len(self.lines)
        # print("lines in file:" + str(self.lineCount))
        

    def volString(self, vol):
        res = "0"
        if (vol<10):
            res = "0" + str(vol)
        else:
            res = str(vol)
        return res;

    def safeFn(self, inStr):
        safe = inStr
        alloweds = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_1234567890"
        for i in range(0,len(inStr)):
            if (alloweds.find(inStr[i])==-1):
                safe = safe.replace(inStr[i], "")
        return safe


    # epub supports an HTML cover page; this make that out of the cover image
    def writeVolume(self, volNum, firstLine, lastLine, isLast): 
        print(str(firstLine) + '-' + str(lastLine))
        vst = self.volString(volNum)
        vstm = self.volString(volNum-1)
        vstp = self.volString(volNum+1)
        txtPath = self.targetDir + self.title + "_" + vst + ".htm"
        txf = open(txtPath, 'w+')
        txf.write('<!DOCTYPE html><html><head><link rel="stylesheet" href="../../../bookstyle.css"></head>')
        txf.write('<body><h2>'  + self.title + ", v." + vst + "</h2>")
        if volNum>1:
            txf.write('<a href="' + self.title + "_" + vstm + '.htm">previous</a> -------- ')
        if not isLast:
            txf.write('<a href="' + self.title + "_" + vstp + '.htm">next</a>')
        txf.write('<br><br>')
        for i in range(firstLine, lastLine):
            ln = self.lines[i]
            if (len(ln)<1): # does that work? gee, I'd like it to. 
                txf.write('<br><br>')
            else:
                ln = ln.replace('&', "&#38;");  # do first, so you can keep the other ones
                ln = ln.replace('"', "&#34;");
                ln = ln.replace('%', "&#37;");
                ln = ln.replace('<', "&#60;");
                ln = ln.replace(">", "&#62;");
                ln = ln.replace("`", "&#96;");
                ln = ln.replace("“", "&#8216;");
                ln = ln.replace("”", "&#8216;");
                ln = ln.replace("‵", "&#8216;");
                txf.write(ln + ' ')
        txf.write('<br><br>')
        if (volNum>1):
            txf.write('<a href="' + self.title + "_" + vstm + '.htm">previous</a> -------- ')
        if not isLast:
            txf.write('<a href="' + self.title + "_" + vstp + '.htm">next</a> <br><br>')
        txf.write('<br><br></body></html>')
        txf.close()


    def output(self):
        startVolLine = 0 
        endVolLine = 1
        volCounter = 1
        isLast = False
        while not isLast:
            endVolLine += 1000
            if not endVolLine < self.lineCount:
                isLast = True
                endVolLine = self.lineCount - 1
            while len(self.lines[endVolLine])>2 and not endVolLine<self.lineCount:
                print(self.lines[endVolLine] + " len=" + str(len(self.lines[endVolLine])))
                endVolLine = endVolLine+1                    
            self.writeVolume(volCounter, startVolLine, endVolLine+1, isLast)
            volCounter = volCounter +1
            startVolLine = endVolLine
            endVolLine = startVolLine+1
        return volCounter
