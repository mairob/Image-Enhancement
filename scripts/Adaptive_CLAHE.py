def CLAHE(channel, limit, tiles):
	"""Applies CLAHE via OpenCV implementation (can be used for Saturation or Value Channel of HSV-Space)
    Args:
    channel: 2-D-Numpy-Array (uint8) representing the "Value"/"Saturation"-Channel of the image
    limit: Float, Clip-Limit for CLAHE
    tiles: Tupel, sets the grid size to divide the image into
    Returns:
      Corrected channel 
    """

	clahe = cv2.createCLAHE(clipLimit= limit, tileGridSize=(tiles,tiles)) 
	return clahe.apply(channel)


def calcEntropy(channel):
	"""Calculates the entropy for the current CLAHE-channel
    Args:
    channel: 2-D-Numpy-Array (uint8) representing the "Value"/"Saturation"-Channel of the image
    Returns:
      Entropy 
    """
	hist = cv2.calcHist([channel],[0],None,[256],[0,256]) / channel.size
	entropy = np.sum(hist* np.log2(hist + 1e-7))
	return (-1.0 * entropy)			

def calcCurvature(xs, ys):
	"""Calculates the curvature of the Clip-Limit vs. Entropy function
    Args:
    xs: List, represents different Clip-Limits
    ys: List, represents corresponding, calculated entropies
    Returns:
      Optimal position (in array) (highest curvature) 
    """
	dx_dt = np.gradient(xs)
	dy_dt = np.gradient(ys)
	d2x_dt2 = np.gradient(dx_dt)
	d2y_dt2 = np.gradient(dy_dt)
	curvature = (d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / (dx_dt * dx_dt + dy_dt * dy_dt)**1.5

	#return optimal position
	return np.argmax(curvature)


def adaptiveCLAHE(channel):
	"""Wrapper to apply adaptive CLAHE to a channel (H / S-channel of HSV)
  http://onlinepresent.org/proceedings/vol21_2013/52.pdf
    Args:
    channel: 2-D-Numpy-Array (uint8) representing the "Value"/"Saturation"-Channel of the image
    Returns:
      Contrast limited histogram equalized channel ("contrast" only of V-Channel is used ;))
    """
  
	channel_orig = channel
  
	#resizing for drastic speedup with minor quality loss
	channel = cv2.resize(channel, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA) 

basic_limit = 0.5
	expanding = 0.01

	res_entropys = []
	cur_entropy = calcEntropy(channel)
	res_entropys.append(cur_entropy)


	for cnt in range(50):
		tmp_v_CLAHE = CLAHE(channel, basic_limit + expanding*cnt, 8)
		cur_entropy = calcEntropy(tmp_v_CLAHE)
		res_entropys.append(cur_entropy)

	
	#find and apply optimal cliplimit
	res_entropys = list(map(float, res_entropys))
	opt_Limit = basic_limit  + expanding* calcCurvature(range(51), res_entropys)

	if opt_Limit < basic_limit:
		opt_Limit=basic_limit


	#adjust window size
	tiles = 6
	res_entropys = []
	tmp_v_CLAHE = CLAHE(channel, opt_Limit, 8)
	cur_entropy = calcEntropy(tmp_v_CLAHE)
	res_entropys.append(cur_entropy)

	for cnt in range(7):
		tmp_v_CLAHE = CLAHE(channel, opt_Limit, tiles + cnt)
		cur_entropy = calcEntropy(tmp_v_CLAHE)
		res_entropys.append(cur_entropy)


	res_entropys = list(map(float, res_entropys))
	opt_tiles = tiles  + calcCurvature(range(8), res_entropys)


	#return optimized channel
	return CLAHE(channel_orig, opt_Limit, opt_tiles)
