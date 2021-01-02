from blaze import Blaze
import cv2

#paths to practice photos and tesseract.exe
bob_cat = r'.\20201010_coop_bob_cat3.JPG'
doe = r'.\20201001_duck_pond_doe.JPG'
sample = r'.\sample.jpg'
                                                                                
#This slices the image into a 16th of the original in the y direction
SLICE_DIVISOR = 16

b1 = Image()
b2 = Image()
b3 = Image()

print(b1.read_image(bob_cat, divisor=SLICE_DIVISOR))
print(b2.read_image(image_path=doe, divisor=SLICE_DIVISOR))
print(b3.read_image(image_path=sample))
