import csv
# import requests
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 
import zipfile
import numpy as np
import cv2

from classes.paths import paths
from classes.author import author


# all the book data
class book:
    def __init__(self):
        # pulled from GBg XML collection
        self.gutenId = -1
        self.title = " "
        self.auths = []      # authors and translators
        self.trns = []
        self.imgs = []
        self.auth = author() # scratch for parsing
        self.subjects = []   # refine: lots of kitchen-sinking
        self.formats = []    # do we care? we have to verify anyway.
        self.language = "-"
        self.type = "-"
        self.description = "-"
        self.date = " "      # !! not present in GB XML! smh
        # set by scanning the gbg dirs; set to "-" if absent
        self.gbgDir = "-"    
        self.txtPath = "-"    
        self.htmPath = "-"
        self.imgPath = "-"
        self.coverImgPath = -1

    # unique book title string: safestring of title + guten id
    def bookTag(self):
        nm = self.title.replace(" ","_") # del all chars not legal for windows paths! 
        nm = nm.replace(":","_")
        nm = nm.replace('"','') # also spaces cause they don't belong! 
        nm = nm.replace("\r","_") # '"' y u no good?
        nm = nm.replace("\n","") # ugh! newlines? scram
        nm = nm[0:50] + "_" + str(self.gutenId)
        return nm

    # unique string for each author
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
        return self.safeString(ath)

    # return false if the unicode for the declared language can make trouble
    def langOK(self):
        if (self.language == "ch"):
            return False
        if (self.language == "zh"):
            return False
        return True

    def isValid(self):
        if not self.langOK():
            return False
        if (len(self.title)<1):
            print("no titla", self.title)
            return False # no title? skip
        if (self.scanGBDir()==0):  # SIDE EFFECT BAD
            return True
        print("GB scan failed")
        return False

    # make a book report for runtime monitoring
    def printSelf(self, ctr):
        try:
            print("count:", ctr)
            print("title:", self.title)
            print("   ID:", self.gutenId)
            print(" type:", self.type)
            for ath in self.auths:
                print(" auth:", ath.authTag())
            #for ath in self.trns:
            #    print(" trns:", ath.authTag())
            #fmts = "  fmt:"
            #for fm in self.formats:
            #    fmts += fm[-16:] + " - "
            #print(fmts)            
            #for fm in self.imgs:
            #    fmts += fm + " - "
            #print(fmts)            
            for fm in self.subjects:
                print(" subj:", fm)
            print(" txt:" + self.txtPath)    
            print(" htm:" + self.htmPath)
            print(" lang:", self.language)
        except:
            cnt=1; # don't care just don't crash ok? 

    # paths.contentDir points to the root of your local GB all-books 
    # collection. Returns the path in that, that contains self's book
    def makeGBGDir(self): 
        thePaths = paths()
        res = thePaths.contentDir
        idStr = str(self.gutenId)
        lng = len(idStr)
        if (lng==1):
            res += "0\\"
        for i in range(0,lng-1):
            res += idStr[i] + "\\"
        res += idStr;
        return res

    # safe for using as a file name or directory name or HTML URL component
    def safeString(self, inStr):
        safe = inStr
        alloweds = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_~+=:;?><-, 1234567890"
        for i in range(0,len(inStr)):
            if (alloweds.find(inStr[i])==-1):
                safe = safe.replace(inStr[i], "")
        return safe

    # given a Gb ID and a path to an XML for it, scan that XML
    def readGbXML(self, gid, xmlfile): 
        self.gutenId = gid
        self.subjects.append("GB# " + str(gid))
        self.gbgDir = self.makeGBGDir()
        self.txtPath = self.gbgDir + "\\" + str(self.gutenId) + ".txt"
        tree = ET.parse(xmlfile) # create element tree object 
        root = tree.getroot()  # get root element 
        for rec in root:
            tg = rec.tag.split('}',1)[-1]
            if (tg == "ebook"):
                bookRecs = rec
        for child in bookRecs:
            tg = child.tag.split('}',1)[-1]
            if (tg == "title"):
                self.title = self.safeString(child.text)
            if (tg == "bookshelf"):
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    if (gctg == "value"):
                        self.subjects.append("Bookshelf: " + gchild.text)
            if (tg == "hasFormat"):
                try:
                    vals = list(child[0].attrib.values())
                    self.formats.append(vals[0])  # pgterms:file rdf:about="http....images"
                    for gchild in child[0]:
                        gctg = gchild.tag.split('}',1)[-1]
                        if (gctg == "format"):
                            for ggch in gchild:
                                ggctg = ggch.tag.split('}',1)[-1]
                                if (ggctg == "Description"):
                                    vals = list(ggch.attrib.values())
                                    self.uuid = vals[0] # uuid = attr[0].value[0]  uuugh
                except:
                    tg = "eh just get the next one"
            if (tg == "subject"):
                subjText = ": "
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    if (gctg == "value"):
                        subjText = subjText + gchild.text
                    if (gctg == "memberOf"):
                        vals = list(gchild.attrib.values())
                        if (len(vals[0])>26):
                            subjText = vals[0][25:] + subjText 
                if (subjText!=": "):
                    self.subjects.append(subjText)
            if (tg == "creator"):
                try:
                    self.auth = author()
                    vals = list(child[0].attrib.values()) #23702
                    self.auth.gutenId = vals[0][12:]
                    for gchild in child[0]:
                        gctg = gchild.tag.split('}',1)[-1]
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
                except:
                    tg = "eh just get the next one"
            if (tg == "trl"):
                try:
                    vals = list(child[0].attrib.values())
                    self.auth.gutenId = vals[0][12:]
                    for gchild in child[0]:
                        gctg = gchild.tag.split('}',1)[-1]
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
                except:
                    tg = "eh just get the next one"
            if (tg == "language"):
                try: 
                    self.language = child[0][0].text
                except: 
                    self.language = "en"
            if (tg == "description"):
                self.description = child.text
            if (tg == "type"):
                try: 
                    self.type = child[0][0].text
                except: 
                    self.type = "Text"


    # after you've read the XML and scanned the gbg, 
    # for each book, put in book opf, ncx, cover, htm
    # maybe mess with cover and formatting soonish.
    def scanHTML(self):
        # self.printSelf()
        if (self.type!="Text"):
            # print("not a Text", self.gutenId)
            return 12
        if (self.txtPath=="-" and self.htmPath=="-"):
            # print("no text", self.gutenId)
            return 13 # no book! skip
        if (len(self.title)<1):
            return 14 # no title? skip
        # write content
        return self.writeContent()


    # looks in the gbg for the book's .txt, .htm, and images dir
    # if there are images, chooses one to use as the cover image
    # empty records are set to "-"
    def scanGBDir(self):
        self.gbgDir = self.makeGBGDir()
        if (not os.path.isdir(self.gbgDir)):
            return 4 # no dir
        if (self.type=="Sound"):
            return 5 # is sound
        self.txtPath = self.gbgDir + "\\" + str(self.gutenId) + ".txt"
        htPth = self.gbgDir + "\\" + str(self.gutenId) + "-h\\"
        htmPath1 = htPth + str(self.gutenId) + "-h.htm"
        htmPath2 = htPth + str(self.gutenId) + "-h.html"
        htmPath3 = htPth + str(self.gutenId) + "-h.xhtml"# jeez pick one, kk?
        self.imgPath = htPth + "images"
        scan = os.listdir(self.gbgDir)
        if (not os.path.isfile(self.txtPath)):
            self.txtPath = "-"
            for fn in scan:
                suf = fn[-4:]
                if (suf==".txt"):
                    self.txtPath = self.gbgDir + "\\" + fn
                    self.type = "Text" 
        else:
            self.type = "Text"
        self.htmPath = "-"
        if (os.path.isfile(htmPath1)):
            self.htmPath = htmPath1
        if (os.path.isfile(htmPath2)):
            self.htmPath = htmPath2
        if (os.path.isfile(htmPath3)): 
            self.htmPath = htmPath3
        if (self.htmPath!="-"):
            self.type = "Text"
        if (not os.path.isdir(self.imgPath)):
            self.imgPath = "-"
        else:
            mess = os.listdir(self.imgPath)
            # no images? clear that path + set cover img to "none"
            ctr = 0
            spare = -1
            for fn in mess:
                self.imgs.append(fn)
                # cover, title, frontispiece?
                if (("over" in fn) or ("ontis" in fn) or ("itle" in fn)):
                    if ((".png" in fn) or (".jpg" in fn)):
                        self.coverImgPath = ctr
                if ((".png" in fn) or (".jpg" in fn)):
                    spare = ctr
                ctr = ctr +1
            if (self.coverImgPath==-1 and spare!=-1):
                self.coverImgPath = spare
        return 0
        


    # copies all the images from a book's /images to the clipart dir
    def addImagesToClips(self, clipDir):
        # write images
        if (self.imgPath!="-"):
            for fn in self.imgs:
                if (".png" in fn) or ("jpg" in fn) or ("jpeg" in fn):
                    fromPt = self.imgPath + "\\" + fn
                    toPt = clipDir + str(self.gutenId) + "_" + fn
                    if os.path.isfile(fromPt):
                        copyfile(fromPt, toPt)
    # only needs to run once a year or so, right?


    # yep
    def writeOPF(self):   
        doc = ET.Element("doc")
        package = ET.SubElement(doc, "package")
        package.set('version', "3.0")
        package.set('xmlns', "http://www.idpf.org/2007/opf")
        package.set('xml:lang', self.language)
        package.set('unique-identifier', "bookid")
        metadata = ET.SubElement(package, "metadata")
        metadata.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
        dcidentifier = ET.SubElement(metadata, "dc:identifier")
        dcidentifier.set('id', "bookid")
        dcidentifier.text =  "urn:uuid:" +self.uuid
        modified = ET.SubElement(metadata, "meta")
        modified.set('property', "dcterms:modified")
        modified.text = "2019-10-11T01:34:19Z"    
        dctitle = ET.SubElement(metadata, "dc:title")
        dctitle.text = self.title
        for aut in self.auths:
            dccontr = ET.SubElement(metadata, "dc:creator")
            dccontr.set('id', "creator")
            dccontr.text = aut.name
            suj = ET.SubElement(metadata, "dc:subject")
            suj.text = aut.wikiLink
        for aut in self.trns:
            dccontr = ET.SubElement(metadata, "dc:translator")
            dccontr.text = aut.name
            suj = ET.SubElement(metadata, "dc:subject")
            suj.text = aut.wikiLink
        description = ET.SubElement(metadata, "dc:description")
        description.text = self.description + " www.gutenberg.org/ebooks/" + str(self.gutenId)
        date = ET.SubElement(metadata, "dc:date")
        date.text = "2015-08-12T04:00:00+00:00"
        publisher = ET.SubElement(metadata, "dc:publisher")
        publisher.text = "http://www.gutenberg.org"
        cover = ET.SubElement(metadata, "meta")
        cover.set("name", "cover")
        cover.set("content", "cover")
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
        manifest = ET.SubElement(package, "manifest")
        anItem = ET.SubElement(manifest, "item")
        anItem.set('id', "ncx")
        anItem.set('href', "toc.ncx")
        anItem.set("media-type", "application/x-dtbncx+xml")
        anItem = ET.SubElement(manifest, "item")
        anItem.set('id', "content")
        anItem.set('href', "content.xhtml")
        anItem.set("media-type", "application/xhtml+xml")
        anItem = ET.SubElement(manifest, "item")
        anItem.set('id', "cover")
        anItem.set('href', "title.xhtml")
        anItem.set("media-type", "application/xhtml+xml")
        anItem = ET.SubElement(manifest, "item")
        anItem.set('id', "coverImg")
        anItem.set('href', "cover.png")
        anItem.set("media-type", "image/png")
        anItem = ET.SubElement(manifest, "item")
        anItem.set('id', "css")
        anItem.set('href', "stylesheet.css")
        anItem.set("media-type", "text/css")
        anItem = ET.SubElement(manifest, "item")
        anItem.set('id', "nav")
        anItem.set('href', "nav.xhtml")
        anItem.set('properties', "nav")
        anItem.set("media-type", "application/xhtml+xml")
#        itemctr = 5
 #       for img in self.imgs:
  #          anItem = ET.SubElement(manifest, "item")
   #         anItem.set('href', "images/"+img)
    #        anItem.set('media-type', "image/jpeg")
     #       anItem.set("id", "item"+str(itemctr))
      #      itemctr += 1
        spine = ET.SubElement(package, "spine")
        spine.set('page-progression-direction', "default")
        spine.set('toc', "ncx")
        anItem = ET.SubElement(spine, "itemref")
        anItem.set('idref', "cover")
        anItem = ET.SubElement(spine, "itemref")
        anItem.set('idref', "content")
        guide = ET.SubElement(package, "guide")
        img = ET.SubElement(guide, "reference")
        img.set('href', "title.xhtml")
        img.set('title', "Cover")
        img.set('type', "cover")
        thePaths = paths()
        tree = ET.ElementTree(package)          
        tree.write(thePaths.dataDir + "scratch.opf")    
        finalVers = open(thePaths.scratchDir + 'OEBPS\\content.opf', 'w+')
        # write in 
        finalVers.write("<?xml version='1.0' encoding='utf-8'?>")
        xmlvers = open(thePaths.dataDir + 'scratch.opf', 'r+')
        irm = xmlvers.read()
        finalVers.write(irm)
        finalVers.close()

    # yep
    def writeNCX(self):   
        ncx = ET.Element("ncx")
       # ncx.set('xmlns', "http://www.daisy.org/z3986/2005/ncx/")
        #ncx.set('version', "2005-1")
        head = ET.SubElement(ncx, "head")
        meta = ET.SubElement(head, "meta")
        meta.set('name', 'dtb:uid')
        meta.set('content', "urn:uuid:" + self.uuid)
        meta = ET.SubElement(head, "meta")
        meta.set('name', 'dtb:depth')
        meta.set('content', "1")
        meta = ET.SubElement(head, "meta")
        meta.set('name', 'dtb:totalPageCount')
        meta.set('content', "0")
        meta = ET.SubElement(head, "meta")
        meta.set('name', 'dtb:maxPageNumber')
        meta.set('content', "0")
        docTitle = ET.SubElement(ncx, "docTitle")
        txt = ET.SubElement(docTitle, "text")
        txt.text = self.title
        navMap = ET.SubElement(ncx, "navMap")
        navPoint = ET.SubElement(navMap, "navPoint")
        navPoint.set('id', 'navPoint-1')
        navPoint.set('playOrder', "1")
        navLabel = ET.SubElement(navPoint, "navLabel")
        text = ET.SubElement(navLabel, "text")
        text.text = "Start"
        content = ET.SubElement(navPoint, "content")
        content.set('src', 'content.xhtml#startyStart')
        thePaths = paths()
        tree = ET.ElementTree(ncx)
        tree.write(thePaths.dataDir + "scratch.ncx")
        # open file at
        finalVers = open(thePaths.scratchDir +'OEBPS\\toc.ncx', 'w+')
        # write in 
        finalVers.write("<?xml version='1.0' encoding='utf-8'?>")
        finalVers.write('<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"')
        finalVers.write(' "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">')
        xmlvers = open(thePaths.dataDir + "scratch.ncx", 'r+')
        irm = xmlvers.read()
        finalVers.write(irm)
        finalVers.close()


    def svgTextSet(self, t, x, y, txt, fntsz):
        t.set("font-size", fntsz)
        t.set("x", x)
        t.set("y", y)
        t.set("text-anchor", "middle")
        t.set("fill", "white")
        t.text = txt


    def brutalString(self, inStr):
        subj = inStr.upper()
        brute = subj
        alloweds = "ABCDEFGHIJKLMNOPQRSTUVWXYZ-, 1234567890"
        for i in range(0,len(subj)):
            if (alloweds.find(subj[i])==-1):
                brute = brute.replace(subj[i], "")
        blen = len(brute)
        res1 = ""
        res2 = ""
        res3 = ""
        if (blen<31):
            res1 = brute
        else:
            res1 = brute[0:30]
            if (blen<61):
                res2 = brute[30:]
            else:
                res2 = brute[30:60]
                if (blen<91):
                    res3 = brute[60:]
                else:
                    res3 = brute[60:90]
        tintInt = alloweds.find(res1[0])
        return res1, res2, res3, tintInt


    def makeCoverImage(self, coverFn, clipFn):  
        # make title strings and authors strings
        titl1, titl2, titl3, titInd = self.brutalString(self.title)
        # make 'em real ugly
        authNames = ""
        notFirst = 1
        for aut in self.auths:
            if (notFirst==1):
                notFirst =0
            else:
                authNames += "--"
            authNames += aut.name
        if (len(self.trns)>0):
            authNames += "--"
        for aut in self.trns:
            if (notFirst==1):
                notFirst =0
            else:
                authNames += "--"
            authNames += aut.name
        if (len(authNames)<1):
            authNames = "Unknown"
        aut1, aut2, aut3, autInd = self.brutalString(authNames)
        # make bg image by loading the cover
        thePaths = paths()
        coverDir = thePaths.coversDir
        coverPath = coverDir + coverFn
        resultImg = cv2.imread(coverPath, cv2.IMREAD_COLOR)
        covHt, covWd, covCh = resultImg.shape
        # change tint
        tintRatio = 0.7 + (autInd / 80.0)
        rFac = 1.0
        gFac = 1.0
        bFac = 1.0
        titInd = titInd % 6
        if (titInd==0):
            rFac = tintRatio 
        if (titInd==1):
            gFac = tintRatio 
        if (titInd==2):
            bFac = tintRatio 
        if (titInd==3):
            rFac = tintRatio 
            gFac = tintRatio 
        if (titInd==4):
            rFac = tintRatio 
            bFac = tintRatio 
        if (titInd==5):
            gFac = tintRatio 
            bFac = tintRatio 
        bchan, gchan, rchan = cv2.split(resultImg);
        rchanf = rchan * rFac; 
        gchanf = gchan * gFac; 
        bchanf = bchan * bFac; 
        rchani = rchanf.astype(np.uint8)
        gchani = gchanf.astype(np.uint8)
        bchani = bchanf.astype(np.uint8)
        resultImg = cv2.merge((rchani,gchani,bchani))
        # make text image
        txti = np.ones((500,500, 3), np.uint8)
        txti *= 255
        # white bg
        font = cv2.FONT_HERSHEY_DUPLEX
        # convert title to all caps, A-Z and space only
        # convert to up to 3 strings 30 char
        x = 6
        y = 26
        fsc = 0.8
        fsp = 27
        fln = 2
        fco = (0,0,0)
        cv2.putText(txti, titl1, (x, y), font, fsc, fco, fln)
        if (len(titl2)>0):
            y += fsp
            cv2.putText(txti,titl2,(x, y), font, fsc, fco, fln)
        if (len(titl3)>0):
            y += fsp
            cv2.putText(txti,titl3,(x, y), font,fsc, fco, fln)
        y += fsp
        cv2.putText(txti,aut1,(x, y), font,fsc, fco, fln)
        if (len(aut2)>0):
            y += fsp
            cv2.putText(txti,aut2,(x, y), font,fsc, fco, fln)
        if (len(aut3)>0):
            y += fsp
            cv2.putText(txti,aut3,(x, y), font,fsc, fco, fln)
        y += fsp
        cv2.putText(txti,"www.gutenberg.org/ebooks/"+str(self.gutenId),(x, y), font,fsc, fco, fln)
        cropTxt = txti[0:y+10, 0:500]
        newWd = covWd -40
        ysz = int((newWd / 500.0) * (y+10.0))
        reszTxt = cv2.resize(cropTxt, (newWd, ysz))
        # a clipart image is available
        clipDir = thePaths.clipDir
        clipPath = clipDir + clipFn
        if (self.imgPath!="-"):
            if (self.coverImgPath!=-1):
                # but if there's an image from the book, use that.
                imgdir = thePaths.scratchDir + "OEBPS\\images\\"
                clipPath = imgdir +self.imgs[self.coverImgPath]
        clipImg = cv2.imread(clipPath, cv2.IMREAD_COLOR)
        if not clipImg is None:
            clHt, clWd, clCh = clipImg.shape
            bchan, gchan, rchan = cv2.split(clipImg);
            clipImg = cv2.merge((rchan,rchan,rchan))
            clpx = int(covWd/2)
            clpy = int( clpx *(clHt/clWd))
            reszClp = cv2.resize(clipImg, (clpx, clpy)) 
            centerx = clpx 
            centery = (((covHt - 20) - ysz) / 2.0) + (ysz +20)
            maxClipHt = covHt - ysz -50; 
            if (clpy>maxClipHt):
                clpy = maxClipHt
            stx = int(centerx - (clpx/2.0))
            sty = int(centery - (clpy/2.0))
            resultImg[sty:sty+clpy, stx:stx+clpx] = reszClp[0:clpy, 0:clpx] # paste clip first
        resultImg[20:20+ysz, 20:20+newWd] = reszTxt # then text block
        resPath = thePaths.scratchDir + "OEBPS\\cover.png"
        cv2.imwrite(resPath, resultImg)
        

    # epub supports an HTML cover page; this make that out of the cover image
    def writeCover(self):   
        html = ET.Element("html")
        html.set('xmlns', "http://www.w3.org/1999/xhtml")
        html.set('xml:lang', "en")
        head = ET.SubElement(html, "head")
        title = ET.SubElement(head, "title")
        title.text = "Cover"
        meta = ET.SubElement(head, "meta")
        meta.set('name', "calibre:cover")
        meta.set('content', "true")
        body = ET.SubElement(html, "body")
        img =ET.SubElement(body, "img")
        img.set("src", "cover.png")
        tree = ET.ElementTree(html)
        thePaths = paths()
        tree.write(thePaths.scratchDir + "OEBPS\\title.xhtml")



    def writeContent(self):   
        thePaths = paths()
        if (self.htmPath!="-"):
            targPath = thePaths.scratchDir + "OEBPS\\content.xhtml"
            content = []
            try: 
                with open(self.htmPath) as f:
                    content = f.readlines()
                numLns = len(content)
                if (numLns>100):
                    numLns = 100
                for lnCt in range(0,numLns):
                    if ("/*" in content[lnCt]):
                        if ("*/" in content[lnCt]):
                            s1 = content[lnCt].find("/*")
                            s2 = content[lnCt].find("*/")
                            stra = content[lnCt][0:s1] + content[lnCt][s2+2:]
                            print(self.gutenId, ":fix:", content[lnCt], stra)
                            content[lnCt] = stra
                    if ("<body" in content[lnCt]):
                        content[lnCt].replace("<body",'<body id=<body id="startyStart "')
                with open(targPath, 'w') as outf:
                    for ln in content:
                        outf.write(ln)
                return 1
            except:
                if os.path.isfile(self.htmPath):
                    copyfile(self.htmPath, targPath)    
                    return 1
        if (self.txtPath=="-"):
            return 0 # no data, I guess. 
        html = ET.Element("html")
        html.set("xmlns", "http://www.w3.org/1999/xhtml")
        head = ET.SubElement(html, "head")
        title = ET.SubElement(head, "title")
        title.text = self.title
        link = ET.SubElement(head, "link")
        link.set('type', "text/css")
        link.set('rel', "stylesheet")
        link.set('href', "stylesheet.css")
        body = ET.SubElement(html, "body")
        # body.set("id", "startyStart")  
        pre = ET.SubElement(body, "pre")
        pre.set("id", "startyStart") 
        txf = open(self.txtPath, 'r+')
        try:
            wholeText = txf.read()
            pre.text = wholeText
            tree = ET.ElementTree(html)
            tree.write(thePaths.scratchDir + "OEBPS\\content.xhtml")
        except:
            return 0
        return 1

   # yep
    def writenavx(self):  
        thePaths = paths()
        html = ET.Element("html")
        html.set('xmlns', "http://www.w3.org/1999/xhtml")
        html.set('xmlns:epub', "http://www.idpf.org/2007/ops")
        head = ET.SubElement(html, "head")
        title = ET.SubElement(head, "title")
        title.text = "Navigation"
        body = ET.SubElement(html, "body")
        nav = ET.SubElement(body, "nav")
        nav.set('epub:type', 'toc')
        ol = ET.SubElement(nav, "ol")
        li = ET.SubElement(ol, "li")
        aref = ET.SubElement(li, "a")
        aref.set('href', "content.xhtml")
        aref.text = "Start"
        tree = ET.ElementTree(html)
        tree.write(thePaths.scratchDir + "OEBPS\\nav.xhtml")


    def safeFn(self, inStr):
        safe = inStr
        alloweds = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_1234567890"
        for i in range(0,len(inStr)):
            if (alloweds.find(inStr[i])==-1):
                safe = safe.replace(inStr[i], "")
        return safe


    # after you've read the XML and scanned the gbg, 

#   make an epub!
#       in scratch/OEBPS/
#       use the .htm if there is one
#       ow make a content.html with all the text in a <PRE>       
#       if there's a cover, make the title.html with it
#       make content.opf
#       make toc.ncx
#       populate dir with .txt, cover, xml, htm, images


    def makeEpub(self, coverPt, clipPt):
        # self.printSelf()
        if (self.type!="Text"):
            print("not a Text", self.gutenId)
            return 0
        if (self.txtPath=="-" and self.htmPath=="-"):
            print("no text", self.gutenId)
            return 0 # no book! skip
        if (len(self.title)<1):
            return 0 # no title? fuck you
        #clean out all the last book's files  
        thePaths = paths()
        base = thePaths.scratchDir + "OEBPS\\"
        src_files = os.listdir(base)
        for fn in src_files:
            if (fn != "stylesheet.css"): # del everything but the stylesheet
                pt = base  + fn
                if os.path.isfile(pt):
                    os.remove(pt)
        # gbg has all the images in *-h/images, darn it. 
        imgdir = base + "images"
        src_files = os.listdir(imgdir)
        for fn in src_files:
            pt = imgdir + "\\" + fn
            if os.path.isfile(pt):
                os.remove(pt)
        htmpath = base + "content.xhtml"
        # write content
        if (self.writeContent()==0):
            return 0 # could not convert
        # write images
        if (self.imgPath!="-"):
            for fn in self.imgs:
                fromPt =self.imgPath + "\\" + fn
                toPt = imgdir + "\\" + fn
                if os.path.isfile(fromPt):
                    copyfile(fromPt, toPt)
        self.writeOPF()
        self.makeCoverImage(coverPt, clipPt)
        self.writeCover()
        self.writeNCX()
        self.writenavx()
        # write index! 
        self.bookPath = thePaths.outputDir + self.safeFn(self.bookTag()) + ".epub"
        if (os.path.isfile(self.bookPath)):
            os.remove(self.bookPath)
        zipf = zipfile.ZipFile(self.bookPath, 'a', zipfile.ZIP_DEFLATED)
        zipf.write("scratch/mimetype", "mimetype", zipfile.ZIP_STORED)
        zipf.write("scratch/META-INF/container.xml", "META-INF/container.xml", zipfile.ZIP_DEFLATED)
        src_files = os.listdir("scratch/OEBPS")
        for file in src_files:
            zipf.write("scratch/OEBPS/" + file, "OEBPS/"+file, zipfile.ZIP_DEFLATED)
        src_files = os.listdir("scratch/OEBPS/images")
        for file in src_files:
            zipf.write("scratch/OEBPS/images/" + file, "OEBPS/images/"+file, zipfile.ZIP_DEFLATED)
        zipf.close()
        return 1
#  zip -Xr9Dq D:/library/pythonic/pubs/The_Declaration_of_Independenc.epub . -i D:/library/pythonic/scratch/*
