
from PIL import Image
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.patches as patch

class LEGOImage():    
    def __init__(self,imagePath,Nx,Ny):
        self.Nx = Nx
        self.Ny = Ny
        self.imagePath = imagePath
        self.img = Image.open(self.imagePath)
        self.img = self.img.convert('L')
        self.cropImg()
        self.np_img = np.array(self.img)
#         self.boolMap = np.zeros(shape=(self.img.height,self.img.width))
        self.pixelMap = np.zeros(shape=(self.Nx,self.Ny))
        self.getPixelMap()
        
    def cropImg(self):
        edge = 25
        self.h=self.img.height
        self.w=self.img.width
        s=0
        if self.h>self.w:
            s=self.w
        else:
            s=self.h
        self.img=self.img.crop((0+edge,0+edge,s-edge,s-edge)) #Choose cropping params manually!
        self.h=self.img.height
        self.w=self.img.width
        self.img.show()
    
    
    def getPixelMap(self):
        Dx=np.int(self.w/self.Nx)
        Dy=np.int(self.h/self.Ny)
        for i in range(0,self.Nx):
            for j in range(self.Ny):
                sum=0
                try:
                    for n in range(0,Dx):
                        for m in range(0,Dy):
                            sum = sum + self.np_img[n+Dx*i,m+Dy*j]
                    self.pixelMap[i,j] = sum/(Dx*Dy)
                except:
                    print('Out of bounds!')
    def plotPixelMap(self):
        edge = 0.2
        plt.figure()
        for i in range(0,self.Nx):
            for j in range(0,self.Ny):
                if self.pixelMap[i][j] <= 255*1/3:
                    rect=patch.Rectangle([j+edge,-i+edge+self.Ny-1],1-2*edge,1-2*edge,color='black')
                    plt.gca().add_patch(rect)
                elif self.pixelMap[i][j] > 255*2/3:
                    rect=patch.Rectangle([j+edge,-i+edge+self.Ny-1],1-2*edge,1-2*edge,color='white')
                    plt.gca().add_patch(rect)
                elif self.pixelMap[i][j] > 255*1/3 and self.pixelMap[i][j] <= 255*2/3:
                    rect=patch.Rectangle([j+edge,-i+edge+self.Ny-1],1-2*edge,1-2*edge,color='gray')
                    plt.gca().add_patch(rect)
                plt.plot([0,self.Nx],[j,j],color='black',linewidth=0.1)
                plt.plot([i,i],[0,self.Ny],color='black',linewidth=0.1)
                plt.gca().set_xlim([0,self.Nx])
                plt.gca().set_ylim([0,self.Ny])
        plt.show()
        
def main():
    path = r'C:\Users\Oskar\eclipse-workspace\LEGO_pixel_art/img4.png'
#     path = r'C:\Users\Oskar\eclipse-workspace\LEGO_pixel_art/img2.PNG'
    imageObj = LEGOImage(path,50,50)
    imageObj.plotPixelMap()
    print('')

if __name__ == "__main__":
    main()