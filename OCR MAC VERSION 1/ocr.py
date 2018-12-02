from PIL import Image
import pytesseract
import argparse
import cv2
import sys
import os
again = "yes"

while again == "yes":
	#If you don't have tesseract executable in your PATH, include the following:
	pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.0.0/bin/tesseract'

	image = input("Copy file path here:" )

	#construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	#ap.add_argument("-i", "--image", required=True,
	#	help= "path to image" )
	ap.add_argument("-p", "--preprocess", type=str, default="thresh",
		help="thresh or blur")
	args = vars(ap.parse_args())

	#load the example image and convert it to grayscale
	image = cv2.imread(image)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

 
	#check to see if we should apply thresholding to preprocess the
	#image
	if args["preprocess"] == "thresh":
		gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
	#make a check to see if median blurring should be done to remove
	#noise
	elif args["preprocess"] == "blur":
		gray = cv2.medianBlur(gray, 3)
 
	#write the grayscale image to disk as a temporary file so we can
	#apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	#load the image as a PIL/Pillow image, apply OCR, and then delete
	#the temporary file
	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)
	print(text)


	#show the output images
	#cv2.imshow("Image", image)
	#cv2.imshow("Output", gray)
	
	print("\n")
	print("\n")

	again = input("Look how fast I can read! Wanna go again?").strip().lower()
if again == "no":
	quit
