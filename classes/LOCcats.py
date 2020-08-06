import os
import sys

from c_paths import paths

# reads LOC categories from the LCC.txt file

# Each line in the file is two strings: a classification string, 
# a space, then a human-readable topic name

class LOCsubject:
    def __init__(self):
        name = "-" # name string for humans
        thisid = "-" # string used for matching
        nextid = "-" # for E and F
        isSimple = True
        indentation = 0
        section = -1
        subsection = -1
        floater = -1.0  # single 

    def init(self, str):
        # section is first letter
        section = ln[0]
        floater = float(int(section) - int("A") + 1)
        
        # subject is second letter-first space
        firstSpace = ln.firstIndOf(" ")

        # indentation is # dashes after space
        firstDash = ln.firstInfOf("-")
        lastDash = ln.lstIndOf("_")
        indentation = lastDash-firstDash
                

    def owns(self, ):




class allLOCsubjects:
    def __init__(self):
        self.lineCounter = 0
        self.subjs = []
        thePaths = paths()
        with open(thePaths.LOCpath) as f:
            content = f.readlines()
            self.lineCounter = len(content)
            for ln in content:
                sb = subject()
                sb.init(ln)
                self.subjects.append(sb)

# matching? searching? etc? 

