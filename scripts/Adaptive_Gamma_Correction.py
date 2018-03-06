#! /usr/bin/python3
import numpy as np

def heaviside(x):
	"""Implementation of the Heaviside step function (https://en.wikipedia.org/wiki/Heaviside_step_function)
    Args:
    x: Numpy-Array or single Scalar
    Returns:
    x with step values 	
    """
        if x <= 0:
                return 0
        else:
                return 1

def adaptiveGammaCorrection(v_Channel):
	"""https://jivp-eurasipjournals.springeropen.com/articles/10.1186/s13640-016-0138-1#CR14 
	Applies adaptive Gamma-Correction to V-Channels of an HSV-image.

    Args:
    v_Channel: Numpy-Array (uint8) representing the "Value"-Channel of the image
    Returns:
      Corrected channel 
    """

	#calculate general variables
	I_in = v_Channel/255.0
	I_out = I_in
	
	sigma = np.std(I_in)
	mean = np.mean(I_in)
	D = 4*sigma


	#low contrast image
	if D <= 1/3:

		gamma = - np.log2(sigma)

		I_in_f = I_in**gamma
		mean_f = (mean**gamma)

		k =  I_in_f + (1 - I_in_f) * mean_f

		c = 1 / (1 + heaviside(0.5 - mean) * (k-1))

		#dark
		if mean < 0.5:
			I_out = I_in_f / ((I_in_f + ((1-I_in_f) * mean_f)))

		#bright			
		else:
			I_out = c * I_in_f



	#high contrast image
	elif D > 1/3:

		gamma = np.exp((1- (mean+sigma))/2)

		I_in_f = I_in**gamma
		mean_f = (mean**gamma)

		k =  I_in_f + (1 - I_in_f) * mean_f

		c = 1/ (1 + heaviside(0.5 - mean) * (k-1))

		I_out = c * I_in_f


	else:
		print('Error calculating D')


	I_out = I_out*255
	
	return I_out.astype(np.uint8)


