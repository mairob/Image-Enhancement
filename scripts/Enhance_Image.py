#! /usr/bin/python3
import numpy as np
import math 
from PIL import Image
from PIL import ImageOps
from PIL import ImageFilter, ImageEnhance
import cv2
import os


srcDirectory = r'../Originals'
saveDirectory = r'../Enhanced/'


def wrapper(path):
	""" Extensive Image-Enhancement featuring Adaptive-CLAHE and Adaptive Gamma-Correction. 
  Colors are additonally improved via a simple gradient guided saturation adjustment.
  Can be used as general script for large amount of images e.g. from vacation, parties, shootings...
  
  Due to the implementation, some parts are unperformant python code. Therefore enhancing a huge amount of high-res images
  will take some time. Better grab a coffee ;)

    Args:
    path: Path to image
    Returns:
      Returns extensively enhanced Image.
    """

	filename = os.path.basename(path)
	#uncomment for duplicating the orignal images 
	#img = Image.open(path).convert('RGB')
	#img.save(saveDirectory + filename + '.png')
	
	img_orig = cv2.imread(path, 1)
	img = img_orig

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)

	gradient =  cv2.Laplacian(s,cv2.CV_32F, ksize = 1)  #cv2.Laplacian(s, cv2.CV_32F, ksize = 1) 
	clipped_gradient = gradient * np.exp(-1 * np.abs(gradient) * np.abs(s - 0.5))

	#normalize to [-1...1]
	clipped_gradient =  2*(clipped_gradient - np.max(clipped_gradient))/-np.ptp(clipped_gradient)-1
	#clipped_gradient = (clipped_gradient - np.amin(clipped_gradient)) / (np.amax(clipped_gradient) - np.amin(clipped_gradient)) 
	clipped_gradient =  0.5 * clipped_gradient #--> 0.5 limits maximum saturation change to 50 %

	factor = np.add(1.0, clipped_gradient)

	s = np.multiply(s, factor)
	s = cv2.convertScaleAbs(s)

	v = adaptiveGammaCorrection(v)
	#v = adaptiveCLAHE(v)
	s = adaptiveCLAHE(s)
	

	final_CLAHE = cv2.merge((h,s,v))

	#additional sharpening
	tmpimg = cv2.cvtColor(final_CLAHE, cv2.COLOR_HSV2BGR)
	shimg = Image.fromarray(cv2.cvtColor(tmpimg,cv2.COLOR_BGR2RGB))
	sharpener = ImageEnhance.Sharpness(shimg)
	sharpened = sharpener.enhance(2.0)

	return sharpened
  
  
  
  
#Do the magic
for filename in os.listdir(srcDirectory):
	if filename.endswith(".JPG") or filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".PNG"): 

		enhImg = wrapper(os.path.join(srcDirectory, filename))
		enhImg.save(saveDirectory + filename + '_enh.jpg', quality=94 ,optimize=True)
 		print(os.path.join(srcDirectory, filename))
