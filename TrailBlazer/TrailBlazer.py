from blaze import *
import cv2


#paths to practice photos and tesseract.exe
bob_cat = r'.\20201010_coop_bob_cat3.JPG'
doe = r'.\20201001_duck_pond_doe.JPG'
sample = r'.\sample.jpg'
                                                                                
im = Image()

print('Bob cat test:')
im.get_image(bob_cat)
im.get_camera_and_date()
print('Camera number:')
print(im.camera_number)
print('Date time group:')
print(im.datetime) 

print('Doe test:')
im.get_image(doe)
im.get_camera_and_date()
print('Camera number:')
print(im.camera_number)
print('Date time group:')
print(im.datetime)

print('Sample test:')
im.get_image(sample)
im.get_camera_and_date()
print('Camera number:')
print(im.camera_number)
print('Date time group:')
print(im.datetime) 