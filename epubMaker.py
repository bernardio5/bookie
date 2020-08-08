import csv
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 
import zipfile
import numpy as np
import cv2
import random
import sys

# this script scans the records and makes epubs


# steps: scan gb records for each record:
#     read the record into a book object
# after all are scanned
# For each book
#   if neither .txt nor .htm, skip
#   scan the gbg data to see what you've got for it: .txt. htm, images, cover
#   make an epub!
#       in scratch/OEBPS/
#       use the .htm if there is one
#       ow make a content.html with all the text in a <PRE>       
#       if there's a cover, make the title.html with it
#       make content.opf
#       make toc.ncx
#       populate dir with .txt, cover, xml, htm, images

from classes.paths import paths
from classes.book import book
from classes.scanner import scanner

class library:
    def __init__(self):
        self.scanner = scanner()
        thePaths = paths()
        self.covers = os.listdir(thePaths.coversDir)
        self.clips = os.listdir(thePaths.clipDir)


    def readAll(self):
        notDone = True
        ctr = 1000  # set to not 1 to start in the middle of the list
        nco = len(self.covers)
        ncl = len(self.clips)
        self.scanner.skipTo(ctr)
        while notDone:
            ctr = ctr +1
            # when debugging, this line stops after book 120
            if (ctr>1100): # comment out to do all books
                notDone = False
            pt = self.scanner.getNextPath()
            if (len(pt)>0 and not (".delete" in pt)):
                booky = book()
                booky.readGbXML(self.scanner.gbID, pt)
                if (booky.langOK() and booky.scanGBDir()==0):
                    #if (ctr%30==0):
                    #    print(ctr, ":", booky.gutenId)
                    coverImg = self.covers[ctr%nco]
                    clipImg = self.clips[(ctr+500)%ncl]
                    if (booky.makeEpub(coverImg, clipImg)==0):
                        print("skipped id ", booky.gutenId)
            else: 
                notDone = False


print("defined")

# everything defines ok; run it
def main():
    lb = library()
    lb.readAll()

if __name__ == "__main__":   
    main() 

print("ok then")