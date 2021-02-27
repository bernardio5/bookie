import csv
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 
import zipfile
import numpy as np
import cv2
import random
import sys

from classes.paths import paths
# from classes.book import book
from classes.ttyBook import ttyBook
from classes.miniBook import miniBook
from classes.titleSet import titleSet
from classes.authorSet import authorSet
from classes.scanner import scanner
from classes.LOCtree import LOCtree


class library:
    def __init__(self):
        self.scanner = scanner()
        self.thePaths = paths()
        self.bookList = titleSet()
        self.theTree = LOCtree()
        self.covers = os.listdir(self.thePaths.coversDir)
        self.clips = os.listdir(self.thePaths.clipDir)
        self.authorSet = authorSet()

    # traverse all books
    def buildCats(self):
        nco = len(self.covers)
        ncl = len(self.clips)
        notDone = True
        ctr = 1 # skip the first 2000; older scans=>low-quality? 
        self.scanner.skipTo(ctr)
        while notDone:
            ctr = ctr +1
            # if (ctr>1200): # comment out to do all books, ~61k
            #    notDone = False
            pt = self.scanner.getNextPath()
            if (len(pt)>0 and not (".delete" in pt)):
                # fullbook = book()
                fullbook = ttyBook()
                fullbook.readGbXML(self.scanner.gbID, pt)
                if (fullbook.gutenId=="9998"): 
                    notDone = False
                if fullbook.isValid():
                    minibook = miniBook()
                    minibook.makeFromBigBook(fullbook)
                    if (minibook.valid):
                        print("adding: " + fullbook.title + ' ' + fullbook.gutenId)
                        for t in fullbook.subjects:
                            print("topic: " + t)
                        coverImg = self.covers[ctr%nco]
                        clipImg = self.clips[(ctr+500)%ncl]
                        # if (fullbook.makeEpub(coverImg, clipImg)==1):
                        if (fullbook.makeTxt(coverImg, clipImg)==1):
                            # minibook.arrangeBigBook(fullbook)
                            minibook.arrangeTTYBook(fullbook)
                            self.bookList.add(minibook)
                            self.theTree.addBook(minibook)
                            for aut in fullbook.auths:
                                self.authorSet.add(aut, fullbook.gutenId)
                    else:
                        print("skipping: " + fullbook.title+ ' ' + fullbook.gutenId)
                else:
                    print("skipping: " + fullbook.title+ ' ' + fullbook.gutenId)


    def makeHTML(self):
        self.theTree.finishTopics()
        self.theTree.makeHTML(str(self.bookList.count())) 
        self.bookList.makeGIDHTML()
        self.bookList.makeTitleHTML()
        self.bookList.makeBookList()
        self.authorSet.makeHTMLs(self.bookList)  # authors
        self.authorSet.makeAuthorList()  # authors

print("defined")

# everything defines ok; run it
def main():
    lb = library()
    lb.buildCats()
    lb.makeHTML()

if __name__ == "__main__":   
    main() 

print("ok then")