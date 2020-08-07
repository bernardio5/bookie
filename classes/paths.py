

# the conversion project uses data stored in directory trees
# set them here



class paths: 
    def __init__(self):
        # "new CaLibre" dir, where we store all the newly-made epubs
        # one subdirectory for each unique author or translator
        self.outputDir = "D:\\library\\newCal\\"

        # dir in which the epub is assembled; will contain XML, HTML, & image files 
        # final step is zipping it up
        self.scratchDir = 'D:\\library\\pythonic\\scratch\\'
        
        # root dir for the collection of gutenberg bibliographic records (.rdf)
        self.recordsDir = "D:\\library\\gutenbergRecs\\cache\\epub\\"

        # root dir of all of the Gutenberg content 
        self.contentDir = "E:\\gbg\\"

        # root dir of the cover images
        self.coversDir = "D:\\library\\pythonic\\covers\\"

        # dir of clip art to use when no cover image is found
        self.clipDir = "D:\\library\\pythonic\\clipArt\\"

        self.LOCpath = "topics.txt"