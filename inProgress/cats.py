import csv
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 
import zipfile
import numpy as np
import cv2
import random
import sys

# web page plan for 60k books
# read category list: categories: 517 of these
# e and f are weird, so skip them today

# for each book, 
#   make a page: cover, metadata, file link, save

# for each category, 
#   for each book, 
#       save book if in category
#
#   sort by author
#   sort by title
#   sort by LCSH
#   for each sort
#       cut into shelves/cases
#   for each case, make a page
#       for each shelf in case (4)
#            draw shelf
#           for each book on shelf
#               render book spine
#               link to book page
# case is 40 books
# book div shows cover + metadat + link to bookfile

# each category makes a room
# room can be sorted by subject or author or title
# each line of the file gives book title
# 19 letters (not e f) -> 19 metasubject rooms
# the 19 meta pages must be generated, linked to by floor diagrams, hand-coded.

# look out PN and PZ are going to be a lot
# jesis boring no. 
# one room of categories for each initial letter
# except for fucking e and f: later
# each room links to room-file-page

# for each room-file
#   divide into cases and shelves
#   page for each case: html + image + maps
#   page for each book: cover + metadata + link to book


from c_paths import paths
from c_author import author
from c_book import book
from c_scanner import scanner
from c_library import library

from c_LOCcats import LOCsubject, allLOCsubjects


# all the book data
class book:



    def writeContent(self):   
        with open("topics.txt") as f:
            content = f.readlines()
        numLns = len(content)
        for ln in content:
            first letter is main class
            second-first blank is second
            rest of line is topic name
            
        return 0



    # after you've read the XML and scanned the gbg, 
    # for each book, put in book opf, ncx, cover, htm
    # maybe mess with cover and formatting soonish.
 

class library:
    def __init__(self):
        self.scanner = scanner()
        self.results = [0, 0, 0,  0, 0, 0,  0, 0, 0, 0,0,0, 0,0,0, 0]

    def readAll(self):
        notDone = True
        ctr = 1
        self.scanner.skipTo(ctr)
        while notDone:
            ctr = ctr +1
            if (ctr>12000):
                notDone = False
            pt = self.scanner.getNextPath()
            if (len(pt)>0):
                if (".delete" in pt):
                    self.results[3]+=1  # 3:delete in fn
                else:
                    booky = book()
                    booky.readGbXML(self.scanner.gbID, pt)
                    if (not booky.langOK()): 
                        self.results[1] +=1 # ch or cn
                    else:
                        res = booky.scanGBDir()
                        if (res!=0):
                            self.results[res] +=1  # 4,5 no dir, is sound
                        else:
                            res = booky.scanHTML()
                            self.results[res]+=1 
            else: 
                notDone = False
        for i in range(0,16):
            print(i, ":", self.results[i])



print("defined")

# formality: just do it. I guess. whatever. 
def main():
    lb = library()
    lb.readAll()

if __name__ == "__main__":   
    # calling main function 
    main() 

print("ok then")