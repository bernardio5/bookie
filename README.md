# bookie

A set of Python scripts that operate on a the Project Gutenberg collection. I have used them to convert most of PG's books to a standard "epub" format. 

Project Gutenberg hosts a collection of ~65,000 public-domain texts, mostly books, some of them good. They're doing fine, but as the recent action against the Internet Archive shows, all publically-visible public-domain collections are one massive lawsuit from the "Writer's Guild" from obliteration. 

How I wish I had mined Google Books. Anyway, I have downloaded PG's content. This repo does not contain that.

This repo is not well-organized yet, because I am still feeling around for exactly what I want to do, and it's very much a side-project. 

In the repo you will be able to find: 
1) Code that traverses the PG bibliographics records set and parses those records into a Python object
2) Code that takes a record object and loads the corresponding TXT, HTML, or other-format object into a Python object
3) Code that outputs a Python book object as an "epub"-formatted book.

Caveat: the epub format is open, but there are many flavors. It's basically a TAR archive that contains some bibliographic XML files, and an HTML doc tree. The goal is to have a format that is "fairly pretty" and works with the maximum number of different readers. 

There are several EPub format checkers, and they're helpful, but they don't solve the problem entirely. 

My complete list of checkers and target viewling platforms is TBA, but does include Apple Books, CaLibre.

Kindles mostly will not load epubs. Most Kindles will view web pages, so don't yell at me-- Amazon is forcing you to buy public-domain data in their secret, propritary Kindle format. Yes, there are Kindle-exporting tools-- you do it.  

Apple Books is, surprise surprise, full of quirky demands, and is not great at dealing with much of the CSS formatting in the PG collection. Seriously Apple: unit tests maybe? But Apple at least is willing to try to let you use EPubs, and when they do load, provide a graceful reading experience. 

CaLibre is great because you can add a directory full of EPubs and it can populate a searchable database using embedded EPub bibliographical data. CaLibre, as of 2019, does not do a great job of handling books collections the size of PG.  
 
If you have 50 books, or 500, you can organize them informally, but 50,000 is another matter. The PG books are organized by a number that is basically the order in which they were added, which is fine for automated traversal but not a good library experience. There is a set of XML bibliographic records. 

I'd like to make an HTML library tree as a user interface, but WIP. 
