import os
import sys

from c_paths import paths

# reads the  categories from the not-renewed.tsv file

# title   parent_title    author  parent_author   
# regnum  parent_regnum   claimants   place_of_publication   
# disposition warnings    renewal_id  renewal_date    
# renewal_registration    registration_date   renewal_title   
# renewal_author

# get it, then what?


class PDEntry:
    def __init__(self):
        title = ""
        author = ""




class PDList:
    def __init__(self, path):
        self.lines = []
        with open(“testfile.txt”) as f: 
            for line in f: 
                words = split('\t')
              
