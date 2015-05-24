import Image
import numpy as np
import os
import re



                            
"""
Main class:
    Converts jpg images to 2d array gradients
"""
class IndivGradient:
    """
    contrast refers to the different ways to find contrast differences for each pixel
    res refers to resolution decrease (e.g. res=.5 will decrease size+resolution of image by 50%)
    """
    def __init__(self, file1,contrast=0, res=1):
        self.file = file1
        self.image = Image.open(file1)                               #original image
        self.image = self.image.resize((int(self.image.size[0]*res)
        ,int(self.image.size[1]*res)), Image.ANTIALIAS)              #resizes image (decreases resolution)
        arr = np.asarray(self.image)        
        self.row = arr.shape[0]                                      #row size of image
        self.col = arr.shape[1]                                      #column size of image   
        self.copy = np.copy(arr)         
        #self.removeLowGradient(100,arr=self.copy)                    #removes some tissues that screws up calculations
        self.gradient = np.empty(arr.shape)                          #original gradient change
        self.mod_gradient = np.empty(arr.shape)                      #modified gradient change
        #if contrast == 0:
            #self.gradientDiff(self.copy)  
        #self.scaleGrad()
        #self.saveGradImage()
    
    def gradientDiff(self,im_arr):
        """
        Passes in 2d image array and outputs gradient difference
        Algorithm: Each pixel in gradient results from the max of
        the difference between the current pixel and the pixels around it
        """
        for i in range(self.row):                                                      #iterate over rows
            for j in range(self.col):                                                  #iterate over columns
                value = []                                                              #stores all gradient values to find max gradient difference 
                try:       
                    if im_arr[i,j][0]>im_arr[i,j-1][0] and j != 0:                     #calculates gradient of above pixel
                        temp = im_arr[i,j][0]-im_arr[i,j-1][0]
                        value.append(temp)
                    else:
                        value.append(im_arr[i,j][0]-im_arr[i,j][0])
                    if im_arr[i,j][0]>im_arr[i-1,j][0] and i != 0:                     #calculates gradient of left pixel
                        temp = im_arr[i,j][0]-im_arr[i-1,j][0]
                        value.append(temp)
                    else:
                        value.append(im_arr[i,j][0]-im_arr[i,j][0])
                    if im_arr[i,j][0]>im_arr[i+1,j][0] and i != gradient.shape[0]-1:   #calculates gradient of right pixel
                        temp = im_arr[i,j][0]-im_arr[i+1,j][0]
                        value.append(temp)
                    else:
                        value.append(im_arr[i,j][0]-im_arr[i,j][0])
                    if im_arr[i,j][0]>im_arr[i,j+1][0] and j != gradient.shape[1]-1:   #calculates gradient of below pixel
                        temp = im_arr[i,j][0]-im_arr[i,j+1][0]
                        value.append(temp)
                    else:
                        value.append(im_arr[i,j][0]-im_arr[i,j][0])
                except Exception:
                    pass
                temp = max(value)
                self.gradient[i,j][0] = temp
                self.gradient[i,j][1] = temp
                self.gradient[i,j][2] = temp
        self.mod_gradient = np.copy(self.gradient)
    
    def removeLowGradient(self, intensity, arr):
        #sets all pixels below intensity value (intensity) to zero
        for i in range(self.row):
            for j in range(self.col):
                if arr[i,j][0] < intensity:
                    arr[i,j][0] = 0
                    arr[i,j][1] = 0
                    arr[i,j][2] = 0
    
    def printOrigImage(self):
        #prints original image
        self.image.show()
    
    def printGradImage(self, orig = False):
        #prints gradient image
        if orig == True:
            im = Image.fromarray(np.uint8(self.gradient))
            im.show()
        else:
            im = Image.fromarray(np.uint8(self.mod_gradient))
            im.show()
    
    def saveGradImage(self, orig = False):
        #saves gradient image
        im = Image.fromarray(np.uint8(self.gradient))
        im.save((self.file[:-4]+'TEST.jpg'))
    
    def removeGrad(self, x, y, row, col):
        #removes gradient of row*col at x and y coordinates
        for i in range(row):
            for j in range(col):
                self.mod_gradient[x+i][j+y][0],self.mod_gradient[x+i][j+y][1],self.mod_gradient[x+i][j+y][2] = 0,0,0
    
    def clearGrad(self):
        self.mod_gradient = np.copy(self.gradient)
    
    def scaleGrad(self):
        #scales gradient so it becomes more clear
        scale = 255/np.max(self.mod_gradient)
        for i in range(self.row):
            for j in range(self.col):
                val = int(self.mod_gradient[i,j][0]*scale)
                self.mod_gradient[i][j][0],self.mod_gradient[i][j][1],self.mod_gradient[i][j][2]=val,val,val
                          
a=IndivGradient("C:/Users/Standard.Admin-THINK.000/Desktop/Xray-Image-Matching-master/Xray-Image-Matching-master/0009_AP_4.5.10.jpg", res = .5)
#image = Image.open("C:/Users/Standard.Admin-THINK.000/Desktop/Xray-Image-Matching-master/Xray-Image-Matching-master/0009_AP_4.5.10.jpg")
#im_arr = np.asarray(image)    

