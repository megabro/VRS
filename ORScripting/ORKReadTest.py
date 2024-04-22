import matplotlib.pyplot as plt
import numpy as np

# Libraries used for reading .ork files
import zipfile
import xml.etree.ElementTree as ET

from matplotlib.widgets import Button, Slider

ork_file_name = 'void_rocket.ork'

with zipfile.ZipFile(ork_file_name, 'r') as ork_zip:
    ork_xml = ork_zip.read('rocket.ork') # The actual rocket XML data is called "rocket.ork".

    root = ET.fromstring(ork_xml)

    for neighbor in root.iter():
        print(neighbor.tag)

    
