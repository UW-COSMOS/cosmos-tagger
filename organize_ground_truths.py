"""
File: organize_ground_truths.py
Author: Keshav Balaji

Description: Standalone Python script to organize xml files into the subdirectories
corresponding to the pdfs they reference and convert the xmls to jsons

Usage: python3 organize_ground_truths.py <directory in which the xml files and pdfs are"
"""

import glob
from xml.dom import minidom
import os
import shutil
import sys
import subprocess
from xml_to_json import parse_xml, create_json

script_dir = os.getcwd()
dir_path = sys.argv[1]
os.chdir(dir_path)
xml_files = glob.glob('*.xml')

# organize xml files into subdirectories
# read the file, get the docid from the <folder> attribute
# If "docid" folder exists, just copy the xml in
# else, create docid folder, copy the PDF and the xml in
for xml_file in xml_files:
    xmldoc = minidom.parse(xml_file)
    doctype = xmldoc.getElementsByTagName('folder')[0].firstChild.nodeValue
    pdf_file = doctype + '.pdf'
    pdf_directory_path = './' + doctype + '/'
    if not os.path.exists(pdf_directory_path):
        os.makedirs(pdf_directory_path)
        shutil.move(pdf_file, pdf_directory_path + pdf_file)
    shutil.move(xml_file, pdf_directory_path + xml_file)

# create json files with the information from their corresponding xml files
for file in os.listdir('.'):
    if not os.path.isdir(file):
        continue
    os.chdir('./' + file + '/')
    xml_files = glob.glob('*.xml')
    for xml_file in xml_files:
        annotations, filename = parse_xml(xml_file)
        create_json(annotations, filename)
    os.chdir('..')