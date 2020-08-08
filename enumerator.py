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

# first pass at error diagnostics: scans a book index range 
# then outputs all of the different error messages returned.

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