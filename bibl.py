import csv
# import requests
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 

from classes.paths import paths
from classes.book import book
from classes.scanner import scanner

# this program scans some or all of the GB data and enumerates authors 
# and translators. A CaLibre library is a directory tree, root/author/book,
# This makes that tree.

# 

# all the book data
class book:
  
    # looks in the gbg for the book's .txt, .htm, and images dir
    # if there are images, chooses one to use as the cover image
    # empty records are set to "-"
    def scanGBDir(self):
        print("gb scan-------")
        self.gbgDir = self.makeGBGDir()
        self.txtPath = self.gbgDir + "\\" + self.gutenId + ".txt"
        htPth = self.gbgDir + "\\" + self.gutenId + "-h\\"
        self.htmPath = htPth + self.gutenId + "-h.htm"
        self.imgPath = htPth + "images"
        scan = os.listdir(self.gbgDir)
             
        print("    self.gbgDir", self.gbgDir)
        if (not os.path.isfile(self.txtPath)):
            self.txtPath = "-"
            for fn in scan:
                suf = fn[-4:]
                if (suf==".txt"):
                    self.txtPath = self.gbgDir + "\\" + fn
        print("    self.txtPath", self.txtPath)
        if (not os.path.isfile(self.htmPath)):
            self.htmPath = "-"
        print("    self.htmPath", self.htmPath)
        if (not os.path.isdir(self.imgPath)):
            self.imgPath = "-"
            print("    self.imgPath", self.imgPath)
        else:
            print("    self.imgPath", self.imgPath)
            # if there is no .htm, clear htmPAth
            mess = os.listdir(self.imgPath)
            # no images? clear that path + set cover img to "none"
            for fn in mess:
                # cover, title, frontispiece?
                if (("over" in fn) or ("ontis" in fn) or ("itle" in fn)):
                    self.coverImgPath = self.imgPath + "\\" + fn
        print("    self.coverImgPath", self.coverImgPath)
        

    # ouput an XML suitable for Calibre for this book -- an ".opf"
    # --into the specified directory, since we're duplicating books. 
    # this is only part of the output process; doesn't copy the files!
    def writeCalXML(self, pth):   
        doc = ET.Element("doc")
        root = ET.SubElement(doc, "?xml")
        root.set('version', '1.0')
        root.set('encoding', 'utf-8')
        package = ET.SubElement(doc, "package")
        package.set('xmlns', "http://www.idpf.org/2007/opf")
        package.set('unique-identifier', "uuid_id")
        package.set('version', "2.0")
        metadata = ET.SubElement(package, "metadata")
        metadata.set('xmlns:dc', "http://purl.org/dc/elements/1.1/")
        metadata.set('xlmns:opf', "http://www.idpf.org/2007/opf")
        dcidentifier = ET.SubElement(metadata, "dc:identifier")
        dcidentifier.set('opf:scheme', "calibre")
        dcidentifier.set('id', "calibre_id")
        dcidentifier.text = "2"
        dcidentifier = ET.SubElement(metadata, "dc:identifier")
        dcidentifier.set('opf:scheme', "uuid")
        dcidentifier.set('id', "uuid_id")
        dcidentifier.text = "a479fce7-8cf2-46e9-980f-89e02b0a4963"
        dctitle = ET.SubElement(metadata, "dc:title")
        dctitle.text = self.title
        for aut in self.auths:
            dccontr = ET.SubElement(metadata, "dc:creator")
            dccontr.set('opf:file-as', aut.authTag())
            dccontr.set('opf:role', "aut")
            dccontr.text = aut.authTag()
            suj = ET.SubElement(metadata, "dc:subject")
            suj.text = aut.wikiLink
        for aut in self.trns:
            dccontr = ET.SubElement(metadata, "dc:translator")
            dccontr.set('opf:file-as', aut.authTag())
            dccontr.set('opf:role', "trn")
            dccontr.text = aut.authTag()
            suj = ET.SubElement(metadata, "dc:subject")
            suj.text = aut.wikiLink
        description = ET.SubElement(metadata, "dc:description")
        des = "&lt;div&gt;" + self.title
        des += "&lt;div&gt;" + "Via Progect Gutenberg"
        des += "&lt;div&gt;" + "http://www.gutenberg.org/ebooks/" + self.gutenId
        description.text = des
        date = ET.SubElement(metadata, "dc:date")
        date.text = "2015-08-12T04:00:00+00:00"
        publisher = ET.SubElement(metadata, "dc:publisher")
        publisher.text = "http://www.gutenberg.org"
        ert = ET.SubElement(metadata, "dc:identifier")
        ert.set('opf:scheme', "PROJECTGUTENBERG")
        ert.text = self.gutenId
        lnggt = ET.SubElement(metadata, "dc:language")
        lnggt.text = "eng"   # need enum for language translations
        for sub in self.subjects:
            suj = ET.SubElement(metadata, "dc:subject")
            suj.text = sub        
        for aut in self.auths:
            suj = ET.SubElement(metadata, "dc:subject")
            suj.text = aut.wikiLink
        for aut in self.trns:
            suj = ET.SubElement(metadata, "dc:subject")
            suj.text = aut.wikiLink
        guide = ET.SubElement(package, "guide")
        img = ET.SubElement(guide, "reference")
        img.set('href', "cover.jpg")
        img.set('title', "Cover")
        img.set('type', "cover")
        tree = ET.ElementTree(package)
        tree.write(pth) # no, use pth!


    # after you've read the XML and scanned the gbg, 
    # this gets called for each auth. ensure that there is a dir 
    # for each, ensure book dir, and put in book opf, cover, and data
    def calSingleOutput(self, which):
        print("single", self.txtPath)
        if (self.txtPath=="-" and self.htmPath=="-"):
            return # no book!
        base = "D:\\library\\latest"
        authdir = base + "\\" + self.authTag(which)
        bookdir = authdir + "\\" + self.bookTag()
        bookpath = bookdir + "\\" + self.authTag(which) + "_" + self.bookTag() + ".txt"
        coverpath = bookdir + "\\cover.txt"
        htmpath = bookdir + "\\" + self.authTag(which) + "_" + self.bookTag() + ".htm"
        opfpath = bookdir + "\\metadata.opf" 
        imgdir = bookdir + "\\images"
        if (not os.path.isdir(base)):
            os.makedirs(base)
        if (not os.path.isdir(authdir)): 
            os.makedirs(authdir)
        if (not os.path.isdir(bookdir)):
            os.makedirs(bookdir)
        if (self.txtPath!="-"):
            copyfile(self.txtPath, bookpath)
        if (self.htmPath!="-"):
            copyfile(self.htmPath, htmpath)
        if (self.imgDir!="-"):
            if (not os.path.isdir(imgdir)):
                so.makedirs(imgdir)
            src_files = os.listdir(self.imgDir)
            for fn in src_files:
                ffn = os.path.join(imagePath, file_name)
                if os.path.isfile(ffn):
                    shutil.copy(ffn, imgdir)
        if (self.coverImgPath!="-"):
            copyfile(self.coverImgPath, coverpath)
        self.writeCalXML(opfpath)

    # make a book data for all auths and trans
    def calOutputAll(self):
        nath = len(self.auths)
        for n in range(0,nath):
            self.calSingleOutput(n)
        ntrs = len(self.trns)
        for n in range(0,ntrs):
            self.calSingleOutput(n+nath)



# iterator class. reads all PGb catalog records, 
# converts to book, collects author/translators, 
# scans "gbg", the rsync dir tree w/ all the books in it, 
# sets up dirs for use by Calibre, puts in files, 
# outputs .opf (metadata files)
class library:
    def __init__(self):
        self.books = []
        self.authors = []
        self.subjects = []
        self.languages = []
        self.locClasses = []
        self.scanner = scanner()

    def readAll(self):
        notDone = True
        ctr = 0
        while notDone:
            ctr = ctr +1
            pt = self.scanner.getNextPath();
            if (len(pt)>0):
                booky = book()
                booky.readGbXML(self.scanner.gbID, pt)
                self.books.append(booky)
            else: 
                notDone = False
            if (ctr%300==0):
                print(ctr, ":", self.scanner.gbID)
            if (ctr>4):
                notDone = False
        print("read ", len(self.books), " books")
        #for ath in self.authors:
        #    os.mkdir(ath.calDir())
        for bk in self.books:
            bk.scanGBDir()
            bk.printSelf()
            bk.calOutputAll()


print("defined")

def main():
    lb = library()
    lb.readAll()

if __name__ == "__main__":   
    main() 

print("ok then")