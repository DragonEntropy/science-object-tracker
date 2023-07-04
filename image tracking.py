import cv2
import numpy as np
import math
import csv

#Note: All colours are in BGR format

#Converts pixel values to coordinates relative to the centre
def pixel_to_coord(pixels_coord, pixel_scale, centre):
    relative_pixels_coord = np.subtract(pixels_coord, centre)
    absolute_coord = np.multiply(relative_pixels_coord, pixel_scale)
    relative_coord = [absolute_coord[0], -absolute_coord[1]]
    return relative_coord

#Generates and applies the mask, leaving only target pixels
#The mask itself is made of black and white pixels only
def apply_mask(img, lower_bound, upper_bound):
    mask = cv2.inRange(img, lower_bound, upper_bound)
    masked = cv2.bitwise_and(img, img, mask = mask)
    return mask, masked

#Finds the centre of the image
def find_centre(frame):
    weight = [0, 0]
    pixel_list = np.transpose(np.where(frame==[255]))
    for pixel in pixel_list:
        weight = np.add(weight, pixel)
    yx_centre = np.true_divide(weight, len(pixel_list))
    xy_centre = [yx_centre[1], yx_centre[0]]
    #print("The centre of the image is at ({0}, {1})".format(*centre))
    return xy_centre

#Processes a single frame
def process_image(frame):
    mask, masked = apply_mask(frame, lower_bound, upper_bound)
    centre = find_centre(mask)

    #To save show or save the output image
    #cv2.imshow("Image Mask", mask)
    #cv2.imwrite("output.jpg", mask)
    
    return centre

#Writes the position for each image into a CSV file
def img_file_output(src_list):
    dest = input("Under what file name should the file be piped to? ")
    file = open(dest, 'a')
    for src in src_list:
        frame = cv2.imread(src)
        output = process_image(frame)
        file.write("{0}, {1}\n".format(*output))
    file.close()

#Writes the position for each frame of a video into a CSV file
def vid_file_output(src, fps, pixel_scale, centres):
    dest = src.replace("mp4", "csv")
    file = open(dest, "a", newline="")
    csv_writer = csv.writer(file, delimiter=",")
    vid = cv2.VideoCapture(src)
    
    ret, frame = vid.read()
    frame_n = 0
    while ret == True:
        pixel_value = process_image(frame)
        output = pixel_to_coord(pixel_value, pixel_scale, centres[src])
        #print("{0}, {1}\n".format(*output))

        csv_writer.writerow([frame_n/fps, *output])
        frame_n += 1
        ret, frame = vid.read()
    file.close()

#The range of target pixels
lower_bound = np.array([0, 150, 0]) 
upper_bound = np.array([140, 255, 140])
#Legacy values
#lower_bound = np.array([0, 50, 70])
#upper_bound = np.array([50, 159, 181])

#pixels to m conversion factor
pixel_scale = 60.7/(902 - 136)/100



#Each video being processed, alongside with their fulcrum position
centres = {"trial12_Trim.mp4" : [995, 155],
           "trial11_Trim.mp4" : [1022, 155],
           "trial10_Trim.mp4" : [1015, 173],
           "trial9_Trim.mp4" : [1016, 193],
           "trial8_Trim.mp4" : [1022, 156],
           "trial7_Trim.mp4" : [1022, 154],
           "trial6_Trim.mp4" : [1023, 154],
           "trial5_Trim.mp4" : [1019, 153],
           "trial4_Trim.mp4" : [1038, 151],
           "trial3_Trim.mp4" : [1000, 151],
           "trial2_Trim.mp4" : [1024, 153],
           "trial1_Trim.mp4" : [998, 152]}

fps = 30

#For videos (comment out when processing images)
for src in centres:
    print("Starting to process {}".format(src))
    vid_file_output(src, fps, pixel_scale, centres)
    print("Processing of {} complete".format(src))

#For individual images (comment out when processing videos)
#src_list = ["test.jpg"]
#img_file_output(src_list)


    
