# bookie

<b>A set of Python scripts that operate on the Project Gutenberg collection and its metadata. </b>

This is not a mirror of Project Gutenberg (URL: www.gutenberg.org)

In the repo you will be able to find: 
1) Code that traverses the PG bibliographic records set and parses them into Python "book" objects
2) Code that takes a "book" object and loads the book's content (txt, HTML)
3) Code that outputs "book" objects as "epub"-formatted files
4) Docs discussing the data formats involved
5) Notes on organization
6) Notes on the polite way to get the data

Project Gutenberg (PG) hosts a collection of ~50,000 public-domain books, some of them good. They're doing fine, but as the recent action against the Internet Archive shows, all centralized, publically-visible, public-domain collections are one massive lawsuit from the "Writer's Guild" away from obliteration. 

How I wish I had crawled Google Books. By the way, don't crawl PG! They support full downloads in extremely-comressed formats; be a good citizen and do it the polite way. Also, talk about a worthwhile charity: www.gutenberg.org/donate 

There are non-book things in the PG archive; these scripts ignore them. 

<b>About the ePub format, and the version these scripts make: </b>

The ePub format is open, but there are many flavors. An ePub file is a zip archive that contains some bibliographic XML files, and an HTML doc tree. If you work with ePub's much at all, one of the most helpful operations is just unzipping it, and examining the parts in a text editor. My goal here is to make ePubs that load on the maximum number of platforms, support search, and are "fairly pretty".

There are several ePub format checkers, and they're helpful, but they don't solve the problem entirely. My complete list of checkers and target viewing platforms is TBA, but does include:

-- Apple Books, which is not great at dealing with much of the CSS formatting in the PG collection. Seriously Apple: unit tests maybe? But Apple at least is willing to try to let you use ePubs, and when they do load, provide a graceful reading experience, esp. on iPad minis!

-- Kindles mostly will not load epubs. Most Kindles will view web pages, so don't blame me-- Amazon is trying to force you to buy public-domain data in their propritary, ever-mutating, eyeball-tracking, arbitrarily-revokable Kindle format. Yes, there are Kindle-exporting tools: nah. 

-- Calibre is great because you can single-operation add a directory full of ePubs, whereupon it automatically generates a searchable library database from embedded data. It also can act as a web server for your collection, which has excellent support for browsing. CaLibre, as of 2019, does not do a great job of handling book collections the size of PG, but it is excellent software for a lot of reasons. Very good error messages!

-- Web browsers are nice because they have debuggers that throw errors that I can get rid of, but the reading experiences they provide are not great. I've tested in Edge, Chrome, Safari, and Firefox. 

-- There are other e-book readers, but I don't own them. 

-- I have used several online and downloadable EPub format checkers, which are comparable to the browsers-- they generate bug reports that I can respond to, but they're not readers, and don't always lead to fixes that add support. These include: EPUB-Checker and some web sites. 

So, the goals of this ePub generator are multi-platform support and widely-readable bibliographic data XML formats. The beauty of the books in the reader is a TBA. 

I do not have automated testing for this. I need it. 

<b>About the covers and formatting:</b>

It helps, when you've got a little set of books in your reader, for the books to have cover images-- basically, icons. So the scripts make covers. EPub supports having a cover HTML page, but the sketchiness of CSS support means it's better to just make a single PNG cover image. 

The scripts use OpenCV to paste together the cover images. The background is a pastel-tinted image of an old book cover. On that, I paste a big black-and-white label with title, author(s), and the PG ID number. Then I add one image, either of the book's cover (if there is one), or any image from the book. If neither is available, I use an image chosen randomly from another PG book. 

Which, of course, is super ugly-- but I love ugly old books, obviously. I'm trying for the "Library Bindings" you see in university libraries, with the brutal font labels printed on dot-matrix printers from the 80s. The repo has a testCover.jpg in root; I'm telling you: it's just what I had in mind. 

I have not taken on page-formatting in book texts. Most readers do an OK job if you just give them plain text with maybe paragraph markers. Most readers let users set the font and margins, so, usually, HTML/CSS page formatting is something to avoid. Attempts to embed images usually just make a mess. I intend to look into this more; it seems like low-hanging fruit. Some widely-implemented subset of CSS? 

<b>About Organizing your University-Scale Library: </b>

If you have 50 books, or 500, you can organize them informally, but 50k is another matter-- it's a library so big that you'll never know what's in it. For comparison, public school libraries in the US usually have around 12,000 books. A university library will have 100,000, and will employ dozens of people to maintain itself. The PG books are organized by a number that is basically the order in which they were added, which is fine for automated traversal, but not a good library experience. PG maintains a set of XML bibliographic records, but still: this is a big job. Librarians get advanced degrees about sorting this many books. 

The Calibre program has excellent search and organization, and automated scanning and integration of new documents, but loading 50k books into it takes a few days, and starting it with the loaded database is not a good experience. But, once I load the ePubs I've made and got the database running, I can do topic searches, which is kind of amazing. Apparently, I own 182 books about pirates. 

<b>About the racism</b>

Project Gutenberg is about the preservation of public-domain texts, which are mostly old books from the United States, and so, sadly, largely written and illustrated by flaming sexist bigots. Seriously, Punch Magazine: uugh. The scripts don't scan for content. The cover generator therefore does kick out a fair amount of racist awfulness. I'm sorry about that. 

Also, there are many books with serious content (for instance, slave narratives) for which the cover generator can make inappropriate covers. This is not deliberate, and not a statement, and I don't like it. Preventing it would require a topic check, which is just code I haven't written yet. 

<b>Project organization</b>
There are folders: 
1) classes: Python base classes: author, book, a directory scanner, code that parses the GB XML records, code that makes ePubs.
2) clipart: One of the scripts crawls the GB book data and copies image files out to a "clipart" directory. This is a sample, so you don't have to run that script before making books. All the images are from PG, and in the public domain. 
3) covers: Black-and-white images of old book covers, ready to be tinted and pasted on by the cover-generator
4) data: templates and other data files; the Library of Congress classifications, to be used when I start making my library interface
5) formats: text files with samples of the different XML formats, along with text about my guesses about what they mean/do/get used for
6) getData: instructions and helper files for retreiving PG data sets
7) scratch: the directory in which the epubs are assembled. As checked in, it contains the parts of the last book I made.
8) The Python files in the root directory are the scripts themselves. They have internal comments that describe what they do. 

<b> Related Work</b>
1) The Kiwix project makes data collections and a program that presents them through a web interface. With Kiwix, hosting a copy of PG or Wikipedia is pretty easy. 
2) The "Standard EBooks" project has a set of tools for producing well-formatted ePubs
3) Calibre.

<b>Future Work</b>
1) Code that removes more of the CSS formatting in PG HTML files, and generally makes better main book texts. Removing the CSS is a priority; about 30% of EPubs with CSS fail to load in one reader or other, esp. Apple Books. 
2) Code/Knowledge for mining and converting books from the Internet Archive & other sources, esp. books identified as being in the public domain.
3) OCR experimentation for converting page images to text to ePub. It seems like research on this mostly petered out 5-10y ago: fine, the utilities should work pretty well now. 
4) An HTML library interface that uses the LOC data to make a map of books, so you can wander the stacks. It looks like you could have the whole library in a 30GB directory, so with a Node server, it could go on most phones, a Raspberry Pi, a dongle on your router, etc. 
I'm imagining a "Little Free 50k Library" that is just a solar-powered Pi server, or a library kiosk that is a sign on a desk with a crappy old laptop under it. 
5) Thinking about our world, in which ordinary citizens can own 50,000 books. : ) 



