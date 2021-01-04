from blaze import *
import cv2


#paths to practice photos and tesseract.exe
bob_cat = r'.\20201010_coop_bob_cat3.JPG'
doe = r'.\20201001_duck_pond_doe.JPG'
sample = r'.\sample.jpg'
                                                                                
im1 = Image()

im1.get_image(bob_cat)
im1.get_camera_and_date()
im1.get_image(doe)
im1.get_camera_and_date()
im1.get_image(sample)
im1.get_camera_and_date()
#im1.display_image('test')

print('Camera number:')
print(im1.camera_number)
print('Date time group:')
print(im1.datetime) 