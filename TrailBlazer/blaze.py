import cv2 
import pytesseract
import numpy as np
import datetime

#Path to tesseract.exe
t_path = r'.\Tesseract-OCR\tesseract.exe'

class Image:

	def __init__(self):
		#path to 
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

	def get_image(image_path):

		try:
			self.image_data = cv2.imread(image_path)
		except:
			return -1

	def get_camera_and_date():
		camera_number = int()
		date_time = datetime.datetime() 
		try:
			camera_number, date_time = __read_image(self.image_data)
		except:
			return -1
		self.camera_number = camera_number
		self.datetime = 

	def __mask_top(image_array, slice_divisor = 1):
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

	def __read_image(image_path, tesseract_path = t_path, divisor = 1):
		""" Uses openCV and tesseract to read text in an image

		Takes an image array and the full path to the tesseract.exe file and outputs 
		a list of strings of the recognized text
		"""

		raw_text = list()

		# Mention the installed location of Tesseract-OCR in your system 
		pytesseract.pytesseract.tesseract_cmd = tesseract_path

		image_array = cv2.imread(image_path)

		gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY) 

		# Crop image to leave only bottom portion according to the divsor
		masked_image = __mask_top(gray, slice_divisor=divisor)

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

		im2 = image_array.copy() 

		# Looping through the identified contours 
		# Then rectangular part is cropped and passed on 
		# to pytesseract for extracting text from it 
		for cnt in contours: 
			x, y, w, h = cv2.boundingRect(cnt) 
	
			# Cropping the text block for giving input to OCR 
			cropped = im2[y:y + h, x:x + w] 
	
			# Apply OCR on the cropped image 
			text = pytesseract.image_to_string(cropped) 
	
			# Appending the text into a list
			raw_text.append(text)

		return raw_text

	def __parse_image_text(text_list):

		camera_number = 0
		y, m, d, h, m, s = 0, 0, 0, 0, 0, 0

		date_time = datetime.datetime(year=y, month=m, day=d, hour=h, minute=m, second=s)

		return camera_number, date_time