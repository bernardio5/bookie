# bookie

<b>A set of Python scripts that operate on the Project Gutenberg collection and its metadata. </b>

This is not a mirror of Project Gutenberg (URL: www.gutenberg.org)

In the repo you will be able to find: 
1) Code that traverses the PG bibliographic records set and parses them into Python "book" objects
2) Code that takes a "book" object and loads the book's content (txt, HTML)
3) Code that outputs "book" objects as "epub"-formatted files
4) Docs discussing the data formats involved
5) Code that makes an HTML document tree that links books, subjects, and authors. 
6) Notes on the polite way to get the data

Project Gutenberg (PG) hosts a collection of ~50,000 public-domain books, some of them good. They're doing fine, but as the recent action against the Internet Archive shows, all centralized, publically-visible, public-domain collections are one massive lawsuit from the "Writer's Guild" away from obliteration. 

How I wish I had crawled Google Books. By the way, don't crawl PG! They support full downloads in extremely-comressed formats; be a good citizen and do it the polite way. Also, talk about a worthwhile charity: www.gutenberg.org/donate 

There are non-book things in the PG archive; these scripts ignore them. 

<b>About the ePub format, and the version these scripts make: </b>

The ePub format is open, but there are many flavors. An ePub file is a zip archive that contains some bibliographic XML files, and an HTML doc tree. If you work with ePub's much at all, you can learn a lot right away by just taking a book, renaming it to end with .zip, unzipping it, and examining the parts in a text editor. My goal here is to make ePubs that load on the maximum number of platforms, support search, and are "fairly pretty".

ePub's are compressed, so an ePub containing text and some images is generally 30%-50% smaller than a simple ASCII text file containing only the text. 

There are several ePub format checkers, and they're helpful, but they don't solve the problem entirely. My complete list of checkers and target viewing platforms is TBA, but does include:

-- Apple Books, which is not great at dealing with much of the CSS formatting in the PG collection. Seriously Apple: unit tests maybe? But Apple at least is willing to try to let you use ePubs, and when they do load, provide a graceful reading experience, esp. on iPad minis!

-- Kindles mostly will not load epubs. Most Kindles will view web pages, so don't blame me-- Amazon is trying to force you to buy public-domain data in their propritary, ever-mutating, eyeball-tracking, arbitrarily-revokable Kindle format. Yes, there are Kindle-exporting tools: nah. 

-- Calibre is great because you can single-operation add a directory full of ePubs, whereupon it automatically generates a searchable library database from embedded data. It also can act as a web server for your collection, which has excellent support for browsing. CaLibre, as of 2019, does not do a great job of handling book collections the size of PG, but it is excellent software for a lot of reasons. Very good error messages!

-- Web browsers USED TO BE helpful. In Spring of 2020, all web browsers simultaneously stopped loading epubs. Again, this is very much a decision by the men who control the internet to make data less free. 

-- There are other e-book readers, but I don't own them. 

-- I have used several online and downloadable EPub format checkers, which are comparable to the browsers-- they generate bug reports that I can respond to, but they're not readers, and don't always lead to fixes that add support. These include: EPUB-Checker and some web sites. 

So, the goals of this ePub generator are multi-platform support and widely-readable bibliographic data XML formats. The beauty of the books in the reader is a TBA. 

I do not have automated testing for this. I need it. 

<b>About the covers and formatting:</b>

It helps, when you've got a little set of books in your reader, for the books to have cover images-- basically, icons. So the scripts make covers. EPub supports having a cover HTML page, but the sketchiness of CSS support means it's better to just make a single PNG cover image. 

The scripts use OpenCV to paste together the cover images. The background is a pastel-tinted image of an old book cover. On that, I paste a big black-and-white label with title, author(s), and the PG ID number. Then I add one image, either of the book's cover (if there is one), or any image from the book. If neither is available, I use an image chosen randomly from another PG book. 

Which, of course, is super ugly-- but I love ugly old books, obviously. I'm trying for the "Library Bindings" you see in university libraries, with the brutal font labels printed on dot-matrix printers from the 80s. The repo has a testCover.jpg in root; I'm telling you: it's just what I had in mind. I save low-quality JPEG images; the PNG's were 500k, which was most of the data in most of the books; the JPGs are ~20k. It halved the size of the book set. 

I have not taken on page-formatting in book texts. Most readers do an OK job if you just give them plain text with maybe paragraph markers. Most readers let users set the font and margins, so, usually, HTML/CSS page formatting is something to avoid. Attempts to embed images usually just make a mess. I intend to look into this more; it seems like low-hanging fruit. Some widely-implemented subset of CSS? 

I'm experimenting with just embedding the text files, and avaiding HTML tags as much as possible. Line endings are interfering with page flow, but at least the text is visible and has minimal formatting garbage (that your TTS reader will read aloud).

<b>About Organizing your University-Scale Library: </b>

If you have 50 books, or 500, you can organize them informally, but 50k is another matter-- it's a library so big that you'll never know what's in it. For comparison, public school libraries in the US usually have around 12,000 books. A university library will have 100,000, and will employ dozens of people to maintain itself. The PG books are organized by a number that is basically the order in which they were added, which is fine for automated traversal, but not a good library experience. PG maintains a set of XML bibliographic records, but still: this is a big job. Librarians get advanced degrees about sorting this many books. 

Kiwix and Calibre are two desktop programs that handle this very dataset well enough. I'm not breaking new ground with work here on organizing books. Project Gutenberg has a web site, after all. 

But: I want the data to be easier to share. The "libraryMaker.py" file in this repo makes plain-HTML pages for each book, topic, and author in the library, giving you an index.html at the head of an HTML document tree that lets you search by author, title, or subject just by following links. No database, no PHP, just drop the directory set wherever you like and you own the books and can search them. 

libraryMaker skips everything that's not text, documents marked "juvenile" or "periodical", and books larger than 3MB; these are just my personal preferences. The resulting directory tree is 14.5GB. I now have the entire tree on a Raspberry Pi, which serves a 34,000-book searchable library through NGINX. Not perfect, but not bad. 

Better topic searching is for sure possible: word clouds, full-text searches, NLP.

<b>About the racism</b>

Project Gutenberg is about the preservation of public-domain texts, which are mostly old books from the United States, and so, sadly, largely written and illustrated by flaming sexist bigots. Seriously, Punch Magazine: uugh. The scripts don't scan for content. The cover generator therefore does kick out a fair amount of racist awfulness. I'm sorry about that. 

Also, there are many books with serious content (for instance, slave narratives) for which the cover generator can make inappropriate covers. This is not deliberate, and not a statement, and I don't like it. Preventing it would require a topic check, which is just code I haven't written yet. 

<b>Project organization</b>
There are folders: 
1) classes: Python base classes: author, book, a directory scanner, code that parses the GB XML records, code that makes ePubs, classes that support LOC classifications. 
2) clipart: One of the scripts crawls the GB book data and copies image files out to a "clipart" directory. This is a sample, so you don't have to run that script before making books. All the images are from PG, and in the public domain. 
3) covers: Black-and-white images of old book covers, ready to be tinted and pasted on by the cover-generator, again from PG itself
4) data: templates and other data files; the Library of Congress classifications
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
4) Thinking about our world, in which ordinary citizens can own 50,000 books. : ) 



