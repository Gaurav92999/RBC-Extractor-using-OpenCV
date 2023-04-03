# RBC-Extractor-using-OpenCV
This code performs image processing on a set of red blood cell (RBC) images to isolate and extract the RBCs from the background. The extracted RBC images are then saved to a separate folder.

Prerequisites:
To run this code, you need to have the following packages installed:

cv2: OpenCV library for computer vision
numpy: package for scientific computing in Python
How to Use
Save your RBC images to the same directory as this code.
Run the code.
The extracted RBC images will be saved to the RBC_IMAGES folder.

Steps:
Creates a RBC_IMAGES folder if it does not already exist.
Loops through a range of image numbers from 1 to 120, and checks if the corresponding image file exists.
Reads in the image file using cv2.imread and converts it to grayscale using cv2.cvtColor.
Applies histogram equalization to the grayscale image using cv2.equalizeHist.
Applies Gaussian blur and unsharp masking to the equalized image.
Applies a circular mask to the Fourier transform of the unsharp masked image to remove any artifacts.
Applies morphological operations to the thresholded image to isolate the RBCs.
Finds contours in the binary image using cv2.findContours.
Extracts individual RBC images from the contours, resizes them to 100x100 pixels, and saves them to the RBC_IMAGES folder.

Parameters:
kernel: Structuring element used in morphological operations (default: (3, 3)).
r: Radius of circular mask (default: 50).
threshold: Threshold value used to binarize the image (default: determined automatically using Otsu's method).
area: Minimum area of a contour to be considered an RBC (default: 1000).
color_threshold: Minimum difference between the red channel and the other two channels for an RBC to be detected (default: 30).

Notes:
This code assumes that the RBCs are the only objects of interest in the images. If there are other objects in the images, they may be mistaken for RBCs and extracted as well.
The performance of this code may vary depending on the quality and resolution of the input images. It is recommended to experiment with different parameter values to achieve the best results.
