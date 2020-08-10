

from classes.paths import paths

# makes web pages. 
# pages are static, in a tree
# all pages mostly use image maps

# top-down org
# root page is for whole library-- floors-- hand-coded: fiction, non-fiction, music, wikipedia
# floors page has map of sections -- handcoded
#     fiction # juvie, main, ?
#     nonf # broad topics 
# section pages are generated
# -- other subdivisions? 

# bottom-up org
# single book record page for each book; link to book itself
# 18-inch page; 30 books in a grid; prev and next shifts by 15
#    need an enumeration in an order! 
# bookcase page-- front view with book spines 
#    call number range at top, shelves with call number ranges. 
#    click on page to go to 18-inch view-- 240 books-- 12 18-in, 
# section page-- top-down view of a grid of bookcases
#    cases marked with call number ranges
#    more or fewer cases depending on section book count
#    cases are buttons, up to 9? back to back, ~2000 books if full
# need 55 sections if all full;  plan on 100

# call numbers
# the floor plan is an enumeration 
# LOC classification to start, and there are 46,000 of thoses
#    so, go with the list we have, and the call numbers start out with the letters, 
#    letter classes with multiple lines get a .FFF microtopic str added
# Then alphabetize (by author?) within the topic, and scatter those to numbers 0-9999

# books can have multiple topics; they appear multiple times.
# FORMAT: LOC.MICROTOPIC.AUTHOR.BOOK_OF_AUTHOR


# tests: no two books have the same call number
# there are enough microtopic numbers.
# there are enough author numbers



# aouthor or translator, same data, same class
class author: 
    def __init__(self):
        self.gutenId = " "
        self.name = " "
        self.birth = " "
        self.death = " "
        self.workIds = []
        self.wikiLink = " "
        thePaths = paths()
        self.calPath = thePaths.outputDir

    # uniqe per-author string. 
    def authTag(self):
        nm = self.name.replace(" ","_")
        nm += "_" + self.gutenId 
        return nm

    # CalLibre uses one dir per author
    def calDir(self):
        return self.calPath + self.authTag()

