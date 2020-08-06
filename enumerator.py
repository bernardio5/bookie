import csv
import os
from shutil import copyfile
import xml.etree.ElementTree as ET 
import zipfile
import numpy as np
import cv2
import random
import sys

from c_paths import paths
from c_author import author
from c_book import book
from c_scanner import scanner
from c_library import library



print("defined")

def main():
    lb = library()
    lb.scanClassifier()

if __name__ == "__main__":   
    # calling main function 
    main() 

print("ok then")