import csv
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 
import zipfile
import numpy as np
import cv2
import random
import sys




# how to make a personal library with 40k books in it. 

# unix/cygwin command to pull the gutenberg directory tree from the "slow" server.
# note presence of 'excl.txt', which contains reg.expr for files to skip
#   mostly sound and CD/DVD data. We're here for books, mister. 
# rsync -av --exclude-from='excl.txt' --del ftp.ibiblio.org::gutenberg /cygdrive/d/gbg

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

# these are not the most beautiful books ever. 
# eh, you can read them. 

class library:
    def __init__(self):
        self.scanner = scanner()
        pathThing = paths()
        self.covers = os.listdir(paths.coversDir)
        self.clips = os.listdir(paths.clipDir)
        self.results = [0, 0, 0,  0, 0, 0,  0, 0, 0, 0,0,0, 0,0,0, 0]


    # a dignostic! try reading the GB XML's & print tally of various results
    def scanClassifier(self):
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