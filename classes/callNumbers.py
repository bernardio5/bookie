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
from classes.scanner import scanner

# We need a topic-centric call-number system 

# call numbers
# the floor plan is an enumeration 
# LOC classification to start, and there are 46,000 of thoses
#    so, go with the list we have, and the call numbers start out with the letters, 
#    letter classes with multiple lines get a .FFF microtopic str added
# Then alphabetize (by author?) within the topic, and scatter those to numbers 0-FFF

# books can have multiple topics; they appear multiple times.
# FORMAT: LOC-MICROTOPIC-AUTHOR-BOOK_OF_AUTHOR

# needed data/stats/actions
# 0) Load the basic categories; there are ~250
     # there are the two-letter ones, and the E's, which have numbers and are history, and fancy
# 1) Sort in the subcategories, from the other file, bringing the total to 45,000, yikes.
# 2) for all the LOCsubjects with == strings, count them and distribute microtopics
#      -- equally spaced in the 000-FFF range, to allow additions later
# 3) for each microtopic, count the authors
#      -- load all the books into book records
#      -- add a list of matching books to each microtopic 
#      -- add a list of authors from each book
#      -- sort the authors & count
# 4) for each microtopic, distribute author numbers
# 5) for each author, for each book in the topic, distribute BOA numbers
# 6) save a list of all call numbers for all books. 

# For building the web pages
# 


# data structures: 

# book records: authors title topics GID call#string

#   basic cats have lists of microcategories
#     also a category name, desc, image! 
#   microcats have basic cat, cat name
#     list of authors, books
#     expect most cats to have 0-5 authors, 0-5 books, some, 100's

# list is array of callnumber records: number gid (author title?) call#string

# map into list, into the library geometry
#    generate the ordered list
#    chop into bookcases
#       bookcase is first call, last call, 
#    chop into rooms
#    chop into floors & draw a picture

# tests: no two books have the same call number
# there are enough microtopic numbers.
# there are enough author numbers



class lightAuthor:
   def __init__(self):
        self.name = ""



class lightSubject:
   def __init__(self):
        self.LOCstring = ""
        self.descr = ""



class lightBook:
    def __init__(self):
        self.authors = []
        self.title = ""
        self.subjects = []
        self.boa = 0

    # the nth distrubted number of count, distributed into 1-4095
    def scaler(nth, count):
    # init from string of form LOC-micro#-author#-boa
    def parse(): 
    # parsable string from self data
    def parsable(): 
    # load data from bib records: auth, title, subj, 
    def loadFromBibl(path):




class library:
    def __init__(self):
        self.scanner = scanner()
        thePaths = paths()
        self.covers = os.listdir(thePaths.coversDir)
        self.clips = os.listdir(thePaths.clipDir)
        self.results = [0, 0, 0,  0, 0, 0,  0, 0, 0, 0,0,0, 0,0,0, 0]


    # a dignostic! try reading the GB XML's & print tally of various results
    def scanClassifier(self):
        notDone = True
        ctr = 1
        self.scanner.skipTo(ctr)
        while notDone:
            ctr = ctr +1
            if (ctr>1000):
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

def main():
    lb = library()
    lb.scanClassifier()

if __name__ == "__main__":   
    # calling main function 
    main() 

print("ok then")