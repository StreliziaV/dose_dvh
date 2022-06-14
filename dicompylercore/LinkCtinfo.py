#!/root/anaconda3/bin/python3
# -*- coding: utf-8 -*-
import json
import numpy
import struct
import sys
import os

from dicompylercore.Converbinfile import readbinFile
from dicompylercore.Converbinfile import readstructMaskFile

class LinkCtInfo:
    name = ""
    numSlices = 129
    xSize = 512
    ySize = 512
    xOffset = 0
    yOffset = 0
    zOffset = 0
    xPixelSpacing = 0
    yPixelSpacing = 0
    zPixelSacing  = 0
    filePath = ""
    dataList = []
    structmask = []
    imageOrientationPatient = []
    imagePositionPatient = []
    patientPostion = ''
    pixelSpacing = []
    photometricInterpretation = ''
    samplesPerPixel = 1
    winwidth = 1
    winlevel = 1
    rescalIntercept = -1024
    rescalSlope = 1

    def __init__(self):
        self.name = ""
        self.numSlices = 0
        self.xSize = 0
        self.ySize = 0
        self.xOffset = 0
        self.yOffset = 0
        self.zOffset = 0
        self.xPixelSpacing = 0
        self.yPixelSpacing = 0
        self.zPixelSacing = 0


    def readCTData(self,ctfilePath):
       self.filePath = ctfilePath + "ctdata.bin"
       dataList = readbinFile(self.filePath,self.xSize,self.ySize)
       structmask = readbinFile(self.filePath,self.xSize,self.ySize)

    def readStructmaskData(self,ctfilePath):
       self.filePath = ctfilePath + "structMask.bin"
       structmask = readstructMaskFile(self.filePath,self.xSize,self.ySize)


   


class DoseGridInfo:
    numSlice = 129
    xSize = 512
    ySize = 512
    xOffset = 0
    yOffset = 0
    zOffset = 0
    xPixelSpacing = 0
    yPixelSpacing = 0
    zPixelSpacing = 0

    def __init__(self,innumSlice,inxSize,inySize,inxOffset,inyOffset,inzOffset,inxPixelSpacing,inyPixelSpacing,inzPixelSpacing):
        self.numSlice = innumSlice




