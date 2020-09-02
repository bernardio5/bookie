
import os
import numpy as np
import cv2

from classes.paths import paths
from classes.author import author



# cover experiments

# everything defines ok; run it
def main():
	titl1 = "SOME TITLES AND OTH"
	titl2 = "ER TEXT THAT IS HERE"
	titl3 = "OKAY"
	titInd = 123
	aut1 = "AUTHOR NAME GOES HE"
	aut2 = "RE AND SECOND AUTHO"
	aut3 = "R OKAY"
	autInd = 45
	resultImg = cv2.imread("D:\\nomad\\mine\\bookie\\covers\\1328_cover.jpg", cv2.IMREAD_COLOR)
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
	cv2.putText(txti,"www.gutenberg.org/ebooks/23134",(x, y), font,fsc, fco, fln)
	cropTxt = txti[0:y+10, 0:500]
	newWd = covWd -40
	ysz = int((newWd / 500.0) * (y+10.0))
	reszTxt = cv2.resize(cropTxt, (newWd, ysz))
	# a clipart image is available
	clipPath = "D:\\library\\clipart\\1310_p8b.jpg"
	clipImg = cv2.imread(clipPath, cv2.IMREAD_COLOR)
	if not clipImg is None:
	    clHt, clWd, clCh = clipImg.shape
	    bchan, gchan, rchan = cv2.split(clipImg);
	    clipImg = cv2.merge((rchan,rchan,rchan))
	    clpx = int(covWd/2.0)
	    clpy = int( clpx *(clHt/clWd))
	    clpSx = int(clpx*1.5)
	    clpSy = int(clpy*1.5)
	    reszClp = cv2.resize(clipImg, (clpSx, clpSy))
	    centerx = clpx 
	    centery = (((covHt - 20) - ysz) / 2.0) + (ysz +20)
	    maxClipHt = covHt - ysz -50; 
	    if (clpSy>maxClipHt):
	        clpSy = maxClipHt
	    stx = int(centerx - (clpSx/2.0))
	    sty = int(centery - (clpSy/2.0))
	    resultImg[sty:sty+clpSy, stx:stx+clpSx] = reszClp[0:clpSy, 0:clpSx] # paste clip first
	resultImg[20:20+ysz, 20:20+newWd] = reszTxt # then text block
	cv2.imwrite("testCover.jpg", resultImg, [int(cv2.IMWRITE_JPEG_QUALITY), 20]) # quality goes from 1-100 


if __name__ == "__main__":   
    main() 