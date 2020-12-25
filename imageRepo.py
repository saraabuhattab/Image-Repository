from PIL import Image , ImageChops
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import webcolors # use version 1.3 of this,'pip install webcolors==1.3'
import os

# FUNCITONS 
def spottingDifferences(firstImage, secondImage):
    '''
    The fuction displays the differences between the two images of the same type and dimensions 
    arguments:
            firstImage(str) : the name of the first image in your working directory that you want to compare
            secondImage(str) : the name of the second image in your working directory that you want to compare with
    output: 
        Displays the differences between the two passed images 
    '''
    img1 = Image.open(firstImage)
    img2 = Image.open(secondImage)
    result = ImageChops.difference(img1, img2)
    print(result.getbbox())
    if result.getbbox():
        result.show()


def closest_color(arr):
    '''
        The fuction finds the closest name of the color for given rgb value 
        arguments:
                arr(numpyarray) : its the numpy array containing the rgb pixel value
        returns: 
            returns the closest name of the color for the given rgb value
    '''
    min_colours = {}
    # Euclidean distance formula to calculate the distance from one color to another 
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - arr[0]) ** 2
        gd = (g_c - arr[1]) ** 2
        bd = (b_c - arr[2]) ** 2
        min_colours[rd + gd + bd] = name
    return min_colours[min(min_colours.keys())]


def get_color_name(requested_color, arr):
    '''
        The fuction finds the name or the closest name of the color for given rgb value 
        arguments:
               requested_color(tuple)  : its a tuple containing the rgb pixel value
                arr(numpyarray) : its the numpy array containing the rgb pixel value which is passed to the closest_color() function if the exact name is not found for the given value
        returns: 
            returns name(str): actual or the closest name of the color for the given rgb value
    '''
    try:
        name = webcolors.rgb_to_name(requested_color)
    except ValueError:
        name = closest_color(arr)

    return name


def colorIdentification(imgList, color):
    '''
         The fuction finds rgb value of the most dominent color and then finds the actual/closest name of the color against the given rgb value by using get_color_name and closest_color() functions
         arguments:
                imgList(list)  : list of all the names present in the working directory
                 color(str) : the color you want to look for in the images
         returns: 
             returns name(str): actual or the closest name of the color for the given rgb value
     '''
    
    lst_names = []  # names of the all the images in the current directory

    for i in range(len(imgList)):
        try:
            temp_img = cv2.imread(imgList[i])  # reading images 
            img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)  # changing it to RGB format

            #    print(img.shape)
            img = img.reshape((img.shape[0] * img.shape[1], 3))  # coverting 3d to 2d array
            no_clusters = 3  # number of colors in image
            kmeans = KMeans(no_clusters)
            kmeans.fit(img)
            colors = kmeans.cluster_centers_  # these are pixel values(RGB values) , list depending on no_clusters
            labels = kmeans.labels_  # these are also list containing labels depending on no_clusters
            # to get the count of each cluster
            label_count = [0 for i in range(no_clusters)]  # just defining a simple list
            for ele in labels:  # counting lables 
                label_count[ele] += 1
            index_color = label_count.index(max(label_count))

            r = int(colors[index_color][0])
            g = int(colors[index_color][1])
            b = int(colors[index_color][2])
            rgb = (r, g, b)  # saving rgb value into the tuble so it passed in get_color_name Fuction
    
            name = get_color_name(rgb, colors[index_color])
            print('The Highest percentage color in ' + imgList[i] + ' is :' + name)
            if color.lower() in name.lower():
                lst_names.append(imgList[i])
        except:
            None
    return lst_names


def mergeImages(list_, dir_, savefileName):
    '''
         The fuction merge all the images in the given list which is being passed as the argument and save the output in the given directory
         arguments:
                list_(list)  : list of all names(str) for all the images you want to merge
                 dir_(str) : directory you want to save you output in.
                 savefileName(str): name of the file you want to save the output image with 
         Output: 
              saves the merged image outpute in the given directory with the given name
    '''
    owd = os.getcwd()  # save the current working directory in owd
    os.chdir(dir_)  # change the working directory

    images = [Image.open(x) for x in list_]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    os.chdir('results')
    new_im.save(savefileName + '.jpg')
    print(savefileName + '.jpg saved in ' + str(os.getcwd()))
    os.chdir(owd)  # change the directory back its its orignal directory  

#Main
#                      For spotting differences
# os.chdir(r'C:\Users\illenium\Scripts\ImageRepo\TestSpot')
# firstImage = 'One.PNG'
# secondImage = 'Two.png'
# spottingDifferences(firstImage, secondImage)

#                  For Color Identification in Images and merging them 
# imgList = os.listdir(r'C:\Users\illenium\Scripts\ImageRepo\TestColorDetec') # list of all the names of images in the current directory
# imgs = colorIdentification(imgList , 'blue')
# dir_ = r'C:\Users\illenium\Scripts\ImageRepo\TestColorDetec'
# mergeImages(imgs , dir_ , 'blueOutput')