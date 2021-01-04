import cv2 
import pytesseract
import numpy as np
import datetime
import re

#Path to tesseract.exe
t_path = r'.\Tesseract-OCR\tesseract.exe'

class Image:

	def __init__(self):
		
		#image data .jpg openCV array
		self.image_data = None
		#metadata
		self.camera_number = None
		self.datetime = None
		self.description = None
		self.species = None
		self.sex = None
		self.age = None
		self.tags = None
		self.location = None
		#path to tesseract.exe
		self.t_path = None

	def get_image(self, image_path):
		"""Stores image data in the image data parameter of the Image class
		
		Takes a path to the .jpg file
		"""

		try:
			self.image_data = cv2.imread(image_path)
		except RuntimeError:
			print('Image read error: image data not read, possible image path error')

	def display_image(self, window_name):
		if type(window_name) == str:
			if self.image_data.any() != None:
				try: 
					cv2.imshow(window_name, self.image_data)
					cv2.waitKey(0)
					cv2.destroyAllWindows()
				except RuntimeError:
					print('Image display error: cv2.imshow() unable to display image')
				
			else:
				print('Display image failed: no image data detected')
		else:
			raise TypeError('Window name not a string data type')

	def __mask_top(self, image_array, slice_divisor = 1):
		"""Takes a gray image and returns it with the top portion set to 255
	
		The "slice_divisor" value sets the size of the unmasked portion by taking
		the total number of pixels in the y axis and dividing it by the divisor 
		value to get the height of the unmasked portion.                               
		"""

		height, width = image_array.shape

		# Use the passed divisor to calculate the unmasked heigth
		cropped_height = int(height / slice_divisor)

		# create a mask 255 == white in grayscale
		mask = np.ones(image_array.shape,np.uint8) * 255

		y_0, y = height-cropped_height, height
		x_0, x = 0, width

		mask[y_0:y,x_0:x] = image_array[y_0:y,x_0:x]

		return mask

	def __parse_image_text(self, text_list):

		try:
			camera_raw = re.findall("CAMERA \d+", text_list)
			date = re.findall("\d\d-\d\d-\d\d\d\d", text_list)
			time = re.findall("\d\d:\d\d:\d\d", text_list)

			camera_number = re.findall("\d+", camera_raw[0])
		except:
			return None, None

		mon, d, y = re.split('-', date[0])
		h, min, s = re.split(':', time[0])

		date_time = datetime.datetime(year=int(y), month=int(mon), day=int(d), hour=int(h), minute=int(min), second=int(s))

		return int(camera_number[0]), date_time

	def __read_image(self, tesseract_path=t_path, divisor=16):
		""" Uses openCV and tesseract to read text in an image

		Takes an image array and the full path to the tesseract.exe file and outputs 
		a list of strings of the recognized text
		"""

		# Mention the installed location of Tesseract-OCR in your system 
		pytesseract.pytesseract.tesseract_cmd = tesseract_path

		try:
			gray = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2GRAY)
		except RuntimeError:
			print('Color conversion error: make sure image is loaded')

		# Crop image to leave only bottom portion according to the divsor
		masked_image = self.__mask_top(gray, slice_divisor=divisor)

		# Performing gausian thresholding 
		ret, thresh1 = cv2.threshold(masked_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) 

		# Specify structure shape and kernel size. 
		# Kernel size increases or decreases the area 
		# of the rectangle to be detected. 
		# A smaller value like (10, 10) will detect 
		# each word instead of a sentence. 
		rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 

		# Appplying dilation on the threshold image 
		dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 

		# Finding contours 
		contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

		im2 = self.image_data.copy() 

		# Looping through the identified contours 
		# Then rectangular part is cropped and passed on 
		# to pytesseract for extracting text from it

		raw_text = list()

		for cnt in contours: 
			x, y, w, h = cv2.boundingRect(cnt) 
	
			# Cropping the text block for giving input to OCR 
			cropped = im2[y:y + h, x:x + w] 
	
			# Apply OCR on the cropped image 
			text = pytesseract.image_to_string(cropped) 
	
			# Appending the text into a list
			raw_text.append(text)

		try:
			camera_number, date_time = self.__parse_image_text(text)
		except RuntimeError:
			print('Text parsing error: unable to read camera number and date/ time from text within image')

		return camera_number, date_time

	def get_camera_and_date(self):
		try:
			camera_number, date_time = self.__read_image()
		except RuntimeError:
			print('Text recognition of image failed: make sure image is loaded and has camera # and date in it')
		self.camera_number = camera_number
		self.datetime = date_time



	

