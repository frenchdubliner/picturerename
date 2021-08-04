#!/usr/bin/env python3
#Author : olivier.chambon@gmail.com
#Version 1.0
#tested on Ubuntu 20.04.2 LTS
#if pip3 install py3exiv2 doesn't work try the following before
#sudo apt-get install build-essential python-all-dev libexiv2-dev libboost-python-dev
#to use example : python3 image_rename.py tata where tata is the folder containing your pictures
#
#Summary : script adds the date to the filename using the EXIF data
#Problem : Nikon cameras use the following format DSC_XXXXX.JPG where X are numbers
#          Those numbers start from 00001 and increase but start again with 00001
#          when a new memory is used leading to conflicting filenames
#Solution : Add Year Month and day in the filename


import pyexiv2
import os
import sys
import shutil


def main():
    src_files = []
    # Loop on arguments and find *jpg and *JPG
    for arg in sys.argv[1:]:
        for dirpath,dirnames,filenames in os.walk(arg):
            for file in filenames:
                src = ''
                if (file.endswith(".jpg") or file.endswith(".JPG")) and file.startswith("DSC"):
                    src_files.append(os.path.join(dirpath,file))

    for file in src_files:
        #read metadata
        metadata = pyexiv2.ImageMetadata(file)
        metadata.read()
        
        try:
            tag = metadata['Exif.Photo.DateTimeOriginal']
        except KeyError:
            tag = metadata['Exif.Image.DateTime']
        try:
            string_of_time = tag.value.strftime('%Y%m%d%H%M%S')
        except AttributeError:
            print ('--> %s lacks creation time data. Deal with it manually' % file)
            pass
        #rename file
        os.rename(file,add_date_to_filename(file,string_of_time))

def add_date_to_filename(file_name,date_of_shot):
    filename_without_extension = file_name[:-4]
    extension = file_name[-4:]
    return filename_without_extension+'_'+date_of_shot+extension


if __name__ == "__main__":
    main()