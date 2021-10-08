#!/usr/bin/env python3
#Author : olivier.chambon@gmail.com
#tested on Ubuntu 20.04.2 LTS
#if pip3 install py3exiv2 doesn't work try the following before
#sudo apt-get install build-essential python-all-dev libexiv2-dev libboost-python-dev
#to use example : python3 image_rename.py tata where tata is the folder containing your pictures

import pyexiv2
import os
import sys
import shutil


def main():
    print('Hello, ' + os.getlogin() +'!')
    src_files = []
    # Loop on arguments and find *jpg and *JPG
    for arg in sys.argv[1:]:
        for dirpath,dirnames,filenames in os.walk(arg):
            for file in filenames:
                src = ''
                if file.endswith(".jpg") or file.endswith(".JPG"):
                    src_files.append(os.path.join(dirpath,file))

    for file in src_files:
        #print file
        metadata = pyexiv2.ImageMetadata(file)
        metadata.read()
        
        try:
            tag = metadata['Exif.Photo.DateTimeOriginal']
            print(tag)
        except KeyError:
            tag = metadata['Exif.Image.DateTime']
        try:
            destination = tag.value.strftime('dest/%Y/%m/%d/')
        except AttributeError:
            print ('--> %s lacks creation time data. Deal with it manually' % file)
            pass
        create_dir(destination)
        print ("cp: %s -> %s" % (file,destination))
        shutil.copy2(file,destination)

def create_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

if __name__ == "__main__":
    main()