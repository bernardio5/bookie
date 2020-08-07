
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 
import zipfile

from classes.paths import paths
from classes.book import book
from classes.scanner import scanner

# This program scans GB data directories and copies images to the 
# clip art direcotry, to be used as clip art for making book covers


class library:
    def __init__(self):
        self.scanner = scanner()
        thePaths = paths()
        self.covers = os.listdir(thePaths.coversDir)
        self.clipDir = thePaths.clipDir

    # instead of making an epub, you just move images to the clip art dir
    def pullImages(self):
        notDone = True
        ctr = 3000		# first GB record that is scanned/mined
        self.scanner.skipTo(ctr)
        while notDone:
            ctr = ctr +1
            if (ctr>3030):
                notDone = False
            pt = self.scanner.getNextPath();
            if (len(pt)>0):
                booky = book()
                booky.readGbXML(self.scanner.gbID, pt)
                if (booky.scanGBDir()==1):
                    booky.addImagesToClips(self.clipDir)
                    print("Output rec#:", ctr, " -- ID:", self.scanner.gbID, " :", booky.title)
                    print("-----------------")
            else: 
                notDone = False


print("defined")

def main():
    lb = library()
    lb.pullImages()

if __name__ == "__main__":   
    main() 

print("ok then")