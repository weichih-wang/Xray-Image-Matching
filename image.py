import Image
import numpy as np
import os
import re
import threading



                            
"""
Main class:
    Converts jpg images to 2d array gradients
    
    Still needs work on:
        implement multithreading to reduce run time
        change some numbers such as intensity and diff so only bone structures will be shown
        find a way to remove bone structues that are not part of the spinal cord
        find a new gradient algorithm that might work better than this one
        
"""
class IndivGradient:
    """
    contrast refers to the different ways to find contrast differences for each pixel
    res refers to resolution decrease (e.g. res=.5 will decrease size+resolution of image by 50%)
    file1 refers to file name
    grad_clean is a boolean variable to determine if you want to remove similar nearby pixels that might not have
    been removed with simple pixel intensity remove (removes issue with borders being created if the nearby pixel
    is barely above the intensity threshhold)
    diff (used in cleaning similar intensity values near threshhold function) refers to how close the intensity
    values of neighboring pixels have to be to be removed from the image
    """
    def __init__(self, file1,contrast=0, res=1,grad_clean = False, intensity, diff=0):
        self.file = file1
        self.image = Image.open(file1)                               #original image
        self.image = self.image.resize((int(self.image.size[0]*res)
        ,int(self.image.size[1]*res)), Image.ANTIALIAS)              #resizes image (decreases resolution)
        arr = np.asarray(self.image)        
        self.row = arr.shape[0]                                      #row size of image
        self.col = arr.shape[1]                                      #column size of image   
        self.grad_clean=grad_clean
        self.copy = np.copy(arr)         
        if grad_clean == False:
            self.removeLowGradient(intensity,arr=self.copy)                    #removes some tissues that screws up calculations
        else:
            self.removeLowGradientAndSim(intensity,arr=self.copy, diff_am=diff)
        self.gradient = np.empty(arr.shape)                          #original gradient change
        self.mod_gradient = np.empty(arr.shape)                      #modified gradient change
        if contrast == 0:
            self.gradientDiff(self.copy)  
        self.scaleGrad()
        self.saveGradImage()
    
    def gradientDiff(self,im_arr):
        """
        Passes in 2d image array and outputs gradient difference
        Algorithm: Each pixel in gradient results from the max of
        the difference between the current pixel and the pixels around it
        """
        for i in range(self.row):                                                      #iterate over rows
            for j in range(self.col):                                                  #iterate over columns
                value = [0]                                                             #stores all gradient values to find max gradient difference 
                try:       
                    if im_arr[i,j][0]>im_arr[i,j-1][0] and j != 0:                     #calculates gradient of above pixel
                        temp = im_arr[i,j][0]-im_arr[i,j-1][0]
                        value.append(temp)
                    if im_arr[i,j][0]>im_arr[i-1,j][0] and i != 0:                     #calculates gradient of left pixel
                        temp = im_arr[i,j][0]-im_arr[i-1,j][0]
                        value.append(temp)
                    if im_arr[i,j][0]>im_arr[i+1,j][0] and i != self.row-1:            #calculates gradient of right pixel
                        temp = im_arr[i,j][0]-im_arr[i+1,j][0]
                        value.append(temp)
                    if im_arr[i,j][0]>im_arr[i,j+1][0] and j != self.col-1:            #calculates gradient of below pixel
                        temp = im_arr[i,j][0]-im_arr[i,j+1][0]
                        value.append(temp)
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
    
    def removeLowGradientAndSim(self, intensity, arr, diff_am):
        #sets all pixels below intensity value (intensity) to zero
        #also removes pixels surrounding intensity that are extremely similar to each other
        for i in range(self.row):
            for j in range(self.col):
                clear = set()
                if arr[i,j][0] == 0:
                    pass
                elif arr[i,j][0] < intensity:
                    clear.add((i,j)) 
                    self.helperRemLowGrad(i-1,j,clear,arr,diff_am,intensity)
                    self.helperRemLowGrad(i+1,j,clear,arr,diff_am,intensity)
                    self.helperRemLowGrad(i,j-1,clear,arr,diff_am,intensity)
                    self.helperRemLowGrad(i,j+1,clear,arr,diff_am,intensity)
                for k,l in clear:
                    arr[k,l][0]=0
                    arr[k,l][1]=0
                    arr[k,l][2]=0
    
    def helperRemLowGrad(self, i, j, pixels, im_arr, val, intensity):
        if len(pixels)>500:
            return
        #helper method to remove pixels that are too similar to ones being removed
        if i < 0 or j < 0 or (i,j) in pixels or j >= self.col or i >= self.row:
            return
        if im_arr[i,j][0]==0:
            return
        value = [0]
        if j != 0:                                                 #calculates gradient of above pixel
            temp = int(im_arr[i,j][0])-int(im_arr[i,j-1][0])
            value.append(temp)
        if i != 0:                                                 #calculates gradient of left pixel
            temp = int(im_arr[i,j][0])-int(im_arr[i-1,j][0])
            value.append(temp)
        if i != self.row-1:                                        #calculates gradient of right pixel
            temp = int(im_arr[i,j][0])-int(im_arr[i+1,j][0])
            value.append(temp)
        if j != self.col-1:                                        #calculates gradient of below pixel
            temp = int(im_arr[i,j][0])-int(im_arr[i,j+1][0])
            value.append(temp)
        temp = max(value) 
        if temp <= val:
            pixels.add((i,j))
            self.helperRemLowGrad(i-1,j,pixels,im_arr,val,intensity)
            self.helperRemLowGrad(i+1,j,pixels,im_arr,val,intensity)
            self.helperRemLowGrad(i,j-1,pixels,im_arr,val,intensity)
            self.helperRemLowGrad(i,j+1,pixels,im_arr,val,intensity)
    
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
        im.save((self.file[:-4]+'TEST'+str(self.grad_clean)+'.jpg'))
    
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

def main():
    files = [f for f in os.listdir('./') if os.path.isfile(f)]
    i = re.compile('.*AP.*(?<!TEST)\.jpg$')                                #regex for frontal images
    lst = [f for f in files if i.match(f)]
    for f in lst:
        IndivGradient(f,res=.5, grad_clean=True, intensity = 140, diff=5)        
        IndivGradient(f,res=.5, grad_clean=False, intensity = 125)


if __name__ == "__main__":   
    main()           
                                                        
#a=IndivGradient("C:/Users/Standard.Admin-THINK.000/Desktop/Xray-Image-Matching-master/Xray-Image-Matching-master/0009_AP_4.5.10.jpg", res = .25, grad_clean=True)
#image = Image.open("C:/Users/Standard.Admin-THINK.000/Desktop/Xray-Image-Matching-master/Xray-Image-Matching-master/0009_AP_4.5.10.jpg")
#im_arr = np.asarray(image)    

#def __main__(

