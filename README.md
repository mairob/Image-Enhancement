# Image-Enhancement
Different implementations of effective enhancement algorithms.
Some examples of the full enhancement script (2500x3382 Pixel):

### ./images/Results.png


Implementation is "pure" or rather "poor" python and is meant to give a simple, easy and free to use example of some effective methods.

Where possible, speedy functions are used (e.g OpenCV).

If speed should be a problem, down scaling the image by factor 4 should give a huge speed boost while still maintaining most of the image quality.

Papers used are


##  ADAPTIVE GAMMA CORRECTION: 
https://jivp-eurasipjournals.springeropen.com/articles/10.1186/s13640-016-0138-1#CR14


@Article{Rahman2016,
author="Rahman, Shanto
and Rahman, Md Mostafijur
and Abdullah-Al-Wadud, M.
and Al-Quaderi, Golam Dastegir
and Shoyaib, Mohammad",
title="An adaptive gamma correction for image enhancement",
journal="EURASIP Journal on Image and Video Processing",
year="2016",
month="Oct",
day="18",
volume="2016",
number="1",
pages="35",
abstract="Due to the limitations of image-capturing devices or the presence of a non-ideal environment, the quality of digital images may get degraded. In spite of much advancement in imaging science, captured images do not always fulfill users' expectations of clear and soothing views. Most of the existing methods mainly focus on either global or local enhancement that might not be suitable for all types of images. These methods do not consider the nature of the image, whereas different types of degraded images may demand different types of treatments. Hence, we classify images into several classes based on the statistical information of the respective images. Afterwards, an adaptive gamma correction (AGC) is proposed to appropriately enhance the contrast of the image where the parameters of AGC are set dynamically based on the image information. Extensive experiments along with qualitative and quantitative evaluations show that the performance of AGC is better than other state-of-the-art techniques.",
issn="1687-5281",
doi="10.1186/s13640-016-0138-1",
url="https://doi.org/10.1186/s13640-016-0138-1"
}




## ADAPTIVE CLAHE:
http://onlinepresent.org/proceedings/vol21_2013/52.pdf


@inproceedings{kim2013determining,
  title={Determining parameters in contrast limited adaptive histogram equalization},
  author={Kim, Seung Jong and Min, Byong Seok and Lim, Dong Kyun and Lee, Joo Heung},
  booktitle={The 7th International Conference on Information Security and Assurance},
  volume={21},
  pages={204--207},
  year={2013}
}

