# bookie

<b>A set of Python scripts that operate on the Project Gutenberg collection and its data. </b>

This is not a mirror of Project Gutenberg. 

Project Gutenberg (PG) hosts a collection of ~65,000 public-domain texts, mostly books, some of them good. They're doing fine, but as the recent action against the Internet Archive shows, all centalized, publically-visible, public-domain collections are one massive lawsuit from the "Writer's Guild" away from obliteration. 

How I wish I had crawled Google Books. By the way, don't crawl PG! They support full downloads in extremely-comressed formats; be a good citizen and do it the polite way. 

In the repo you will be able to find: 
1) Code that traverses the PG bibliographic records set and parses them into Python objects
2) Code that takes a record object and loads the corresponding TXT, HTML, or other-format object into a Python object
3) Code that outputs the book objects as "epub"-formatted books
4) Docs discussing the data formats involved
5) Notes on organization
6) There are non-book things in the PG archive; they are ignored. 

<b>About the EPub format, and the version these scripts make: </b>

The EPub format is open, but there are many flavors. It's basically a TAR archive that contains some bibliographic XML files, and an HTML doc tree. The goal is to have a format that loads on the maximum number of platforms, supports search, and is "fairly pretty".

There are several EPub format checkers, and they're helpful, but they don't solve the problem entirely. My complete list of checkers and target viewing platforms is TBA, but does include:

-- Apple Books, which is not great at dealing with much of the CSS formatting in the PG collection. Seriously Apple: unit tests maybe? But Apple at least is willing to try to let you use EPubs, and when they do load, provide a graceful reading experience, esp. on iPad minis!

-- Kindles mostly will not load epubs. Most Kindles will view web pages, so don't blame me-- Amazon is trying to force you to buy public-domain data in their propritary, ever-mutating, eyeball-tracking, arbitrarily-revokable Kindle format. Yes, there are Kindle-exporting tools: nah. 

-- CaLibre is great because you can single-operation add a directory full of EPubs, whereupon it automatically generates a searchable library database from embedded data. It also can act as a web server for your collection, which has excellent support for browsing. CaLibre, as of 2019, does not do a great job of handling book collections the size of PG, but it is lovely software for a lot of reasons. 

-- Web browsers are nice because they have debuggers that throw errors that I can get rid of, but the reading experiences they provide are not great. I've tested in Edge, Chrome, Safari, and Firefox. 

-- There are other e-book readers, but I don't own them. 

-- I have used several online and downloadable EPub format checkers, which are comparable to the browsers-- they generate bug reports that I can respond to, but they're not readers, and don't always lead to fixes that add support. These include: ___. 

So, the main goal of this EPub generator is multi-platform support, and presentation of a maximum amount of bibliographic data, for the sake of search and browsing. The beauty of the books in the reader is a TBA. 

I do not have automated testing for this.

<b>About the covers and formatting:</b>

I want to have distinctive covers for all the books that include legible author/title. Apple Books, Calibre, and the Internet Archive present book cover images as part of browsing. It helps, when you've got a little set of books in your reader, to have a distinctive image for the book cover, so the EPub scripts generate cover JPGs for all the books. 

EPub supports having a cover HTML page, but the sketchiness of CSS support means your best bet is a full-page JPG of the cover. 

The covers my scripts make are fabulously ugly-- deliberately. I am emulating the "Library Binding"s I saw in university libraries: monochrome vinyl hardbacks with computer-printed stickers: functional, sturdy, cheap, and ugly. I use OpenCV to make the JPGs: it works. I use OpenCV's "Hershy" font, which is the one included, and so, so ugly. Kerning? Bah. Word wrap? Aspirational.

When the PG data has a scan of a book's cover, it almost never has a legible Author/Title. The covers can be elegant, but usually in a generic way, and they're usually really beat-up. If a cover image can be automatically identified (maybe 15% of the titles), I use it. If there are any other JPG or PNG attached to the book, I choose one at random, otherwise I use a randomly-chosen image from a different PG book. I have a collection ~20 "book front" images that I tint to some a random pastel shade, paste on a black on white Author/Title label, paste on the from-the-book image, and that's the cover.png. Image + color + title + author + image => memorable.

Page formatting is mostly TBA. Most readers do a fine job if you just give them plain text with maybe paragraph markers. Most readers let users set the font and margins, so, usually, HTML page formatting is something to avoid. Attempts to embed images usually fight with the refonting and remargining and just make a mess. I intend to look into this more; it seems like low-hanging fruit. 

<b>About Organizing your University-Scale Library: </b>

If you have 50 books, or 500, you can organize them informally, but 65,000 is another matter-- it's a library so big that you can't know what's in it. The PG books are organized by a number that is basically the order in which they were added, which is fine for automated traversal but not a good library experience. 

PG maintains a set of XML bibliographic records, and they're pretty good about Author/Title/Subject, really Author(Translator,Second Author,Editor)/Title(Subtitle,Subsubtitle)/Subject(LOC classification)/Date(of generation). Librarians get advanced degrees about sorting this many books! 

The Library Of Congress (of the United States) publishes a well-documented sorting regime, though it is rather parochial. The Dewey Decimal System is proprietary, owned by OCLC, so I'm not using that. PG often includes LOC classification, but not always. PG often includes ISBN numbers, but I don't think you can use those to organize, though I'm sure there would be a way to use them to find bibliographic data. 

Amazon has much better similarity data for books, and is probably worth a crawl for the sake of gathering that. TBD! 

I'd like to generate an HTML library tree as a user interface: WIP. 

I am aware of the Kiwix project, and respect it. I'm kind of working in parallel. 

<b>About the racism</b>

Project Gutenberg is about the preservation of public-domain texts, which are mostly old books from the United States, and so, sadly, largely written and illustrated by flaming sexist bigots. The scripts don't scan for content. The cover generator therefore does kick out a fair amount of racist awfulness that is just not seen in today's book market. 

I'm sorry about that. 

It would be worthwhile for PG to add a bigotry tag, but it would be a huge, huge job. 




