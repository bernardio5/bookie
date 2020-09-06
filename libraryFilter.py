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
from classes.book import book
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
        self.authorSet = authorSet()

    # traverse all books
    def buildCats(self):
        notDone = True
        ctr = 1
        self.scanner.skipTo(ctr)
        while notDone:
            ctr = ctr +1
            if (ctr>800): # comment out to do all books
                notDone = False
            pt = self.scanner.getNextPath()
            if (len(pt)>0 and not (".delete" in pt)):
                fullbook = book()
                fullbook.readGbXML(self.scanner.gbID, pt)
                if (fullbook.gutenId=="9998"): 
                    notDone = False
                if (fullbook.checkForText()==1):
                    print(fullbook.title)
                    minibook = miniBook()
                    minibook.makeFromBigBook(fullbook)
                    if (minibook.valid):
                        minibook.copyText(fullbook)
                        self.bookList.add(minibook)
                        self.theTree.addBook(minibook)
                        for aut in fullbook.auths:
                            self.authorSet.add(aut, fullbook.gutenId)

    def makeHTML(self):
        self.theTree.finishTopics()
        self.theTree.makeHTML(str(self.bookList.count())) 
        self.bookList.makeGIDHTML()
        self.bookList.makeTitleHTML()
        self.bookList.makeBookList()
        self.authorSet.makeHTMLs(self.bookList)  # authors
        self.authorSet.makeAuthorList()

print("defined")

# everything defines ok; run it
def main():
    lb = library()
    lb.buildCats()
    lb.makeHTML()

if __name__ == "__main__":   
    main() 

print("ok then")