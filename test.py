# -*- coding: utf-8 -*-
"""
Test: python test.py <pathtofile>

@author: victornavarro
"""

from waterbody import waterbody 
from skimage import io
import sys

if __name__ == "__main__":
    
    filename = sys.argv[1]
    
    test = io.imread(filename)
    
    w, e, anc = waterbody(test)
    
    io.imsave('./output_water_mask.tif',w)
    io.imsave('./output_water_edges.tif',w)
    io.imsave('./output_denoised.tif', anc["denoised"])
    io.imsave('./output_scaled.tif', anc["scaled"])
    io.imsave('./output_rawland.tif', anc["rawland"])
    
    
