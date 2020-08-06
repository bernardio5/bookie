import csv
# import requests
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 

# how to make a personal library with 40k books in it. 

# unix/cygwin command to pull the gutenberg directory tree from the "slow" server.
# note presence of 'excl.txt', which contains reg.expr for files to skip
#   mostly sound and CD/DVD data. We're here for books, mister. 
# rsync -av --exclude-from='excl.txt' --del ftp.ibiblio.org::gutenberg /cygdrive/d/gbg

# steps: scan gb records for each record:
#     read the record into a book object
# after all are scanned
# For each book
#     add author to unique author list
#     add subjects to unique subjs list
#     add LibOfCongress entries to that
#     check that you've got .txt, .htm, images, a cover
#     make a CL directory
#       populate dir with .txt, cover, xml, htm, images


# same rec for author and translator. I prefer Homer by Chapman, y'know? 
class author: 
    def __init__(self):
        self.gutenId = " "
        self.name = " "
        self.birth = " "
        self.death = " "
        self.workIds = []
        self.wikiLink = " "

    def authTag(self):
        nm = self.name.replace(" ","_")
        nm += "_" + self.gutenId 
        return nm

    def calDir(self):
        return "D:\\library\\newCal\\" + self.authTag()


# all the book data
class book:
    def __init__(self):
        # pulled from GBg XML collection
        self.gutenId = -1
        self.title = " "
        self.auths = []      # authors and translators
        self.trns = []
        self.auth = author() # scratch for parsing
        self.subjects = []   # refine: lots of kitchen-sinking
        self.formats = []    # do we care? we have to verify anyway.
        self.language = " "
        self.date = " "      # !! not present in GB XML! smh
        # set by scanning the gbg dirs; set to "-" if absent
        self.gbgDir = "-"    
        self.txtPath = "-"    
        self.htmPath = "-"
        self.imgDir = "-"
        self.coverImgPath = "-"

    def bookTag(self):
        nm = self.title.replace(" ","_") # del all chars not legal for windows paths! 
        nm = nm.replace(":","_")
        nm = nm.replace('"','') # also spaces cause they don't belong! 
        nm = nm.replace("\r","_") # '"' y u no good?
        nm = nm.replace("\n","") # ugh! newlines? scram
        nm = nm[0:30]
        return nm

    # authTag for the whichth author or translator
    def authTag(self, which):
        ath = "-"
        na = len(self.auths)
        if (which<na):
            ath = self.auths[which].authTag();
        else:
            wh = which - na
            nt = len(self.trns)
            if (wh<nt):
                ath = self.trns[which].authTag();
        return ath

    # hah, a book report
    def printSelf(self):
        print("title:", self.title)
        print("   ID:", self.gutenId)
        for ath in self.auths:
            print(" auth:", ath.authTag())
        for ath in self.trns:
            print(" trns:", ath.authTag())
        fmts = "  fmt:"
        for fm in self.formats:
            fmts += fm[-16:] + " - "
        print(fmts)            
        for fm in self.subjects:
            print(" subj:", fm)
        print(" txt:" + self.txtPath)    
        print(" htm:" + self.htmPath)
        print(" img:" + self.imgDir)
        print("  cv:" + self.coverImgPath)
        print(" lang:", self.language)
        print("--")

    # returns the path in e:\gbg that contains the book
    def makeGBGDir(self): 
        res = "E:\\gbg\\"
        lng = len(self.gutenId); 
        if (lng==1):
            res += "0\\"
        for i in range(0,lng-1):
            res += self.gutenId[i] + "\\"
        res += self.gutenId;
        return res

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
        
    # given a Gb ID and a path to an XML for it, scan the XML
    def readGbXML(self, gid, xmlfile): 
        self.gutenId = gid
        self.gbgDir = self.makeGBGDir()
        self.txtPath = self.gbgDir + "\\" + self.gutenId + ".txt"
        tree = ET.parse(xmlfile) # create element tree object 
        root = tree.getroot()  # get root element 
        # print(xmlfile)
        for rec in root:
            tg = rec.tag.split('}',1)[-1]
            if (tg == "ebook"):
                bookRecs = rec
        for child in bookRecs:
            tg = child.tag.split('}',1)[-1]
            # print(tg)
            if (tg == "title"):
                self.title = child.text
            if (tg == "bookshelf"):
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    if (gctg == "value"):
                        self.subjects.append("Bookshelf: " + gchild.text)
            if (tg == "hasFormat"):
                vals = list(child[0].attrib.values())
                self.formats.append(vals[0])
            if (tg == "subject"):
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    if (gctg == "value"):
                        self.subjects.append(gchild.text)
                    #if (gctg == "memberOf"):
                    #   self.subjects.append(gchild.text)
            if (tg == "creator"):
                vals = list(child[0].attrib.values()) #23702
                self.auth.gutenId = vals[0][12:]
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    # print("  gctg:", gctg)
                    if (gctg == "webpage"):
                        vals = list(gchild.attrib.values())
                        self.auth.wikiLink = vals[0]
                    if (gctg == "name"):
                        self.auth.name = gchild.text 
                    if (gctg == "birthdate"):
                        self.auth.birth = gchild.text 
                    if (gctg == "deathdate"):
                        self.auth.death = gchild.text
                self.auths.append(self.auth)
                self.auth = author()
            if (tg == "trl"):
                vals = list(child[0].attrib.values())
                self.auth.gutenId = vals[0][12:]
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    # print("  gctg:", gctg)
                    if (gctg == "webpage"):
                        vals = list(gchild.attrib.values())
                        self.auth.wikiLink = vals[0]
                    if (gctg == "name"):
                        self.auth.name = gchild.text
                    if (gctg == "birthdate"):
                        self.auth.birth = gchild.text 
                    if (gctg == "deathdate"):
                        self.auth.death = gchild.text
                self.trns.append(self.auth)
                self.auth = author()
            if (tg == "language"):
                self.language = child[0][0].text
        # self.printSelf()

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


# mech for finding all records; iterator counter
# we don't have a dir for every integer, so 
# the index is not==GB book id; it's just a counter
# get the GB ID for the dir contents by 
# converting the dir's name to an int
class scanner:
    def __init__(self):
        self.dirIndex = 0
        self.allFiles = []
        self.counter = 1
        self.gbID = '-1'
        self.last = -1
        # find the top dir
        dir = "D:\\library\\gutenbergRecs\\cache\\epub"
        mess = [x[1] for x in os.walk(dir)]
        self.allFiles = mess[0]
        self.last = len(self.allFiles)
        print("found ", self.last, " records")
        if (self.last>0):
            self.counter = 1

    def getNextPath(self):
        res = ''
        dir = "D:\\library\\gutenbergRecs\\cache\\epub\\"
        if (self.counter!=-1 and self.counter<self.last):
            fls = self.allFiles[self.counter]
            self.gbID = fls  # fls is the dir name. fls!=counter !
            self.counter +=1
            res = dir + fls + "\\pg" + fls + ".rdf"
        else:
            self.counter = -1
        return res


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

# formality: just do it. I guess. whatever. 
def main():
    lb = library()
    lb.readAll()

if __name__ == "__main__":   
    # calling main function 
    main() 

print("ok then")