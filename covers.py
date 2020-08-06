
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 
import zipfile

from c_paths import paths
from c_author import author
from c_book import book
from c_scanner import scanner
from c_library import library

print("defined")

def main():
    lb = library()
    lb.makeCovers()

if __name__ == "__main__":   
    main() 

print("ok then")