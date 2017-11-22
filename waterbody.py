# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 11:06:50 2016

@author: victornavarro
"""

import cv2
import numpy as np
from skimage import exposure
from scipy.misc import bytescale as bytescale
from scipy.ndimage.morphology import binary_fill_holes
#from matplotlib import pyplot as plt


def waterbody(band, logarithmic = True, clipping = [5,98], 
              filter_kernel_size = 25,  opening_kernel_size = 7,
              closing_kernel_size = 7, fill_holes = True,
              sand_max_gray_level = 5):
             
    mask = ~np.isnan(band)
    band[~mask] = 0
    mask = band>0
    
    #Rescale intensity
    if logarithmic:
      #LOGARITMIC
      im_log = np.zeros(band.shape)
      im_log[mask] = np.log10(band[mask])
      p_min,p_max = np.percentile(im_log[mask], clipping)
      #print p_min, p_max
      im_rescale = np.zeros(im_log.shape)
      im_rescale[mask] = exposure.rescale_intensity(im_log[mask], in_range=(p_min,p_max))
      im_rescale[~mask] = np.min(im_rescale[mask].ravel())
    else:
      #LINEAR
      p_min,p_max = np.percentile(band[mask], clipping)
      #print p_min, p_max
      im_rescale = np.zeros(band.shape)
      im_rescale[mask] = exposure.rescale_intensity(band[mask], in_range=(p_min,p_max))
      im_rescale[~mask] = np.min(im_rescale[mask].ravel())
    
    #To byte
    img = bytescale(im_rescale)
    
    #Filter image
    ksz = filter_kernel_size
    blur = cv2.medianBlur(img,ksz)
       
    #Otsu's binarization. Ignore 0 and 255 values (truncated)
    thres,temp = cv2.threshold(blur[(blur!=0) & (blur!=255)],0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #print thres
    ret,th = cv2.threshold(blur,thres,255,cv2.THRESH_BINARY)
    
    #mark as land sand banks of low gray level or shadowing areas
    #th[blur<sand_max_gray_level & mask] = 255
    th[blur<sand_max_gray_level] = 255

    raw_land_mask = th.copy()
    #morphology operations
    #opening (remove small objects)
    ksz = opening_kernel_size
    opening_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksz,ksz))
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, opening_kernel)
    
    if fill_holes:
        #fill every gap in land, no matter how large
        th = 255*binary_fill_holes(th).astype('uint8')  
    else:
        #closing (fill only small gaps)
        ksz = closing_kernel_size
        closing_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksz,ksz))
        th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, closing_kernel)

    
    #Edge detection on open/closed image
    can = cv2.Canny(th,50,100)
  
#    #DEBUG PLOTS
#    ##simple
#    titles=['Scaled image', 'Filtered image', 'Histogram','Mask']
#    plt.subplot(1,4,1), plt.imshow(img,'gray')
#    plt.title(titles[0])
#    plt.subplot(1,4,2), plt.imshow(blur,'gray')
#    plt.title(titles[1])
#    plt.subplot(1,4,3), plt.hist(blur[(blur!=0) & (blur!=255)].ravel(),256)
#    plt.title(titles[2])
#    plt.subplot(1,4,4), plt.imshow(th,'gray') 
#    plt.title(titles[3])
#    
#    plt.savefig('/home/victornavarro/Desktop/waterbody.png')

    
    water_mask = ~np.array(th, dtype='uint8')
    water_edges = np.array(can, dtype='uint8')
    
    ancillary = {"scaled":img, "denoised":blur, "rawland":raw_land_mask}

    return water_mask, water_edges, ancillary

def waterbodydp(band1, band2, opening_kernel_size = 7,
              closing_kernel_size = 7, fill_holes = True):
             
    th = band1 & band2

    #morphology operations
    #opening (remove small objects)
    ksz = opening_kernel_size
    opening_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksz,ksz))
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, opening_kernel)
    
    if fill_holes:
        #fill every gap in land, no matter how large
        th = 255*binary_fill_holes(th).astype('uint8')  
    else:
        #closing (fill only small gaps)
        ksz = closing_kernel_size
        closing_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksz,ksz))
        th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, closing_kernel)
    
    #Edge detection on open/closed image
    can = cv2.Canny(th,50,100)
  
#    #DEBUG PLOTS
#    ##simple
#    titles=['Scaled image', 'Filtered image', 'Histogram','Mask']
#    plt.subplot(1,4,1), plt.imshow(img,'gray')
#    plt.title(titles[0])
#    plt.subplot(1,4,2), plt.imshow(blur,'gray')
#    plt.title(titles[1])
#    plt.subplot(1,4,3), plt.hist(blur[(blur!=0) & (blur!=255)].ravel(),256)
#    plt.title(titles[2])
#    plt.subplot(1,4,4), plt.imshow(th,'gray') 
#    plt.title(titles[3])
#    
#    plt.savefig('/home/victornavarro/Desktop/waterbody.png')

    water_mask = ~np.array(th, dtype='uint8')
    water_mask[np.logical_xor(band1,band2)] = 127
    water_edges = np.array(can, dtype='uint8')


    return water_mask, water_edges
    
