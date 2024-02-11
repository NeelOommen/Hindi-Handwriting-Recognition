import os

class data_manager:
    def __init__(self) -> None:
        self.filePath = ''
        self.thumbnailPath = ''
        self.outputPath = '..\\Hindi-Handwriting-Recognition\\processing_cache\\temp_output\\'
        self.switchToPreprocessing = None
        self.switchToLabelling = None
        self.arePathsValid = False
        self.img_cache = None
        self.img_preserve = None
        self.lower_threshold = 0
        self.upper_threshold = 255
        self.blur_factor =  7

    def setBlurFactor(self, factor):
        self.blur_factor = factor

    def getBlurFactor(self):
        return self.blur_factor

    def setLowerThreshold(self, limit):
        self.lower_threshold = limit

    def setUpperThreshold(self, limit):
        self.upper_threshold = limit

    def setPreservedImage(self, img):
        self.img_preserve = img

    def setImgCache(self,img):
        self.img_cache = img

    def getImageCache(self):
        return self.img_cache

    def setProcessingSwitchFunction(self, func):
        self.switchToPreprocessing = func

    def setLabellingSwitchFunction(self, func):
        self.switchToLabelling = func

    def returnProcessingSwitchFunction(self):
        return self.switchToPreprocessing
    
    def returnLabellingSwitchFunction(self):
        return self.switchToLabelling

    def validatePaths(self):
        if(self.filePath == None or self.thumbnailPath == None):
            self.arePathsValid = False
        else:
            self.arePathsValid = True
    
    def setPaths(self, filepath, thumbnailpath):
        self.filePath = filepath
        self.thumbnailPath = thumbnailpath

        self.validatePaths()

    def setOutputPath(self, oPath):
        self.outputPath = oPath

    def getFileName(self):
        return self.filePath
    
    def getThumbnail(self):
        return self.thumbnailPath
    
    def getOutputPath(self):
        return self.outputPath

    def __del__(self):
        os.remove(self.filePath)
        os.remove(self.thumbnailPath)