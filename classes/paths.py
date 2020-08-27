

# the conversion project uses data stored in directory trees
# set them here



class paths: 
    def __init__(self):
        # where you put this archive
        self.baseDir = "D:\\nomad\\mine\\bookie\\"

        # root dir of the cover images
        self.coversDir =  self.baseDir + "covers\\"

        # dir of clip art to use when no cover image is found
        self.clipDir =  "D:\\library\\clipart\\"

        # dir holding misc data and template files
        self.dataDir =  self.baseDir + "data\\"

        # dir in which the epub 
        self.scratchDir = self.baseDir + 'scratch\\'
        

        # root dir for the collection of gutenberg bibliographic records (.rdf)
        self.recordsDir = "D:\\library\\gutenbergRecs\\cache\\epub\\"

        # root dir of all of the Gutenberg content. It's big! Had to buy a new drive. 
        self.contentDir = "E:\\gbg\\"

        # "new CaLibre" dir, where we store all the newly-made epubs
        # one subdirectory for each unique author or translator
        self.outputDir = "F:\\newCal\\"

        # where the HTML tree goes
        self.htmlDir = "F:\\libHtml\\"
