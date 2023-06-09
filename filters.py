from abc import *
from PIL import Image

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

class Filter(object, metaclass=ABCMeta):
    '''
    Filter class with abstract method that defines filter's transfromation
    '''
    @abstractmethod
    def filterFunction(self, pxl):
        pass 
    
    def apply(self, srcImage: Image.Image) -> Image.Image:
        '''
        Applies a specified filter to every pixel of an image data from srcImage
        '''
        newPixelData = []

        for pxldata in srcImage.getdata():
            newPixelData.append(self.filterFunction(pxldata))

        modified_image = Image.new(srcImage.mode, srcImage.size)
        modified_image.putdata(newPixelData)

        return modified_image

class BlackWhiteFilter(Filter):
    def filterFunction(self, pxl):
        r, g, b = pxl
        total = (r + g + b)//3 
        return (total, total, total)

class OnlyRedFilter(Filter):
    def filterFunction(self, pxl):
        r, g, b = pxl
        return (r, 0, 0)

class OnlyGreenFilter(Filter):
    def filterFunction(self, pxl):
        r, g, b = pxl
        return (0, g, 0)

class OnlyBlueFilter(Filter):
    def filterFunction(self, pxl):
        r, g, b = pxl
        return (0, 0, b)
    
class SepiaFilter(Filter):
    def filterFunction(self, pxl):
        (r, g, b) = pxl
        tr = 0.393*r + 0.769*g + 0.189*b
        tg = 0.349*r + 0.686*g + 0.168*b
        tb = 0.272*r + 0.534*g + 0.131*b
        tr = int(clamp(tr, 0, 255))
        tg = int(clamp(tg, 0, 255))
        tb = int(clamp(tb, 0, 255))
        return (tr, tg, tb)

class HueFilter(Filter):
    def filterFunction(self, pxl):
        (r, g, b) = pxl
        tr = -0.547*r + 1.500*g + 0.044*b
        tg = 0.409*r + 0.417*g + 0.174*b
        tb = 0.509*r + 1.350*g + -0.858*b
        tr = int(clamp(tr, 0, 255))
        tg = int(clamp(tg, 0, 255))
        tb = int(clamp(tb, 0, 255))
        return (tr, tg, tb)

class MaxSaturationFilter(Filter):
    def filterFunction(self, pxl):
        (r, g, b) = pxl
        tr = 2.570*r + -1.430*g + -0.144*b
        tg = -0.426*r + 1.570*g + -0.144*b
        tb = -0.426*r + -1.430*g + 2.860*b
        tr = int(clamp(tr, 0, 255))
        tg = int(clamp(tg, 0, 255))
        tb = int(clamp(tb, 0, 255))
        return (tr, tg, tb)
    
class MaxContrastFilter(Filter):
    def filterFunction(self, pxl):
        (r, g, b) = pxl
        tr = 2*r - 0.5
        tg = 2*g - 0.5
        tb = 2*b - 0.5
        tr = int(clamp(tr, 0, 255))
        tg = int(clamp(tg, 0, 255))
        tb = int(clamp(tb, 0, 255))
        return (tr, tg, tb)

class CustomFilter(Filter):
    def __init__(self, matrix) -> None:
        super().__init__()
        self.image_transform = matrix
    
    def filterFunction(self, pxl):
        return self.color_transform(pxl)
    
    def color_transform(self, pxl):
        r, g, b = pxl
        a = self.image_transform
        red = a[0][0]*r + a[0][1]*g + a[0][2]*b + a[0][3]
        green = a[1][0]*r + a[1][1]*g + a[1][2]*b + a[1][3]
        blue = a[2][0]*r + a[2][1]*g + a[2][2]*b + a[2][3]
        red = int(clamp(red, 0, 255))
        green = int(clamp(green, 0, 255))
        blue = int(clamp(blue, 0, 255))
        return (red, green, blue)
