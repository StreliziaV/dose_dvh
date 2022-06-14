#!/root/anaconda3/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import struct
import sys
import os
import math
import json



class configPara:
      
    def __init__(self):
        self.mode = 'gen_test_data_base'
        #self.dicom_raw_dir = dicom_raw_dir_defaultvalue
        #self.infer_data_dir = dicom_infer_dir_defaultvalue
        #self.dicom_npz_dir = dicom_npz_dir_defaultvalue
        self.test_dir = './test'
        self.output_size = 256
        self.patientID = '28802_20181224'
        self.train_dataset_mode = 'single'
        self.intep = 'nearest'
        self.use_dose_for_cmp = 1

        self.inputpath = ""     #input path
        self.outputpath = ""    #output path
        self.cfgpath = ""       #config path

    def SetInputpath(self,inputPath,outputPath):
        self.inputpath = inputPath
        self.outputpath = outputPath


    def SetdicomDir(self,dicomrawdir,dicominfer,dicomnpa):
        self.dicom_raw_dir = dicomrawdir
        self.infer_data_dir = dicominfer
        self.dicom_npz_dir = dicomnpa





class configParapix:
    def __init__(self):
        self.which_g_model = 'pix2pix'
        self.mode = 'test'
        self.dataset_name = ''
        self.batch_size = 1
        self.epochs = 10000
        self.ngf = 64
        self.ndf = 64
        self.input_nc = 4
        self.output_nc = 1
        self.lr = 0.00002  # input path
        self.L1_lambda = 90.0  # output path
        self.beta1 = 0.5  # config path
        self.checkpoint_dir = "./checkpoint"
        self.sample_dir = "./sample"
        self.test_dir = "./test"
        self.patientID = "28802_20181224"
        self.layers_per_block = "2,2,2,2"
        self.growth_k = 16
        self.patch_size = '32,64,64'
        self.channel = 3
        self.gpu_max_memory = 0.3
        self.gpu_ids = '0'

        self.inputPath = ''
        self.outputPath = ''
        self.inferPath = ''

        def SetInoutPath(self,inputPath,outputPath):
            self.inputPath = inputPath
            self.outputPath = outputPath




#read bin file
def readbinFile(filename,width,heigh,zsize):
    print('read binary file %s'%filename)
    fid = open(filename,'rb+')

    dataList = []
    for i in range(width * heigh*zsize):
        data = fid.read(4)
        val = struct.unpack('f',data)[0]
        #print(val)
        dataList.append(val)
    fid.close()
    return dataList


def getndarrayFrombinFile(filename,width,heigh,zsize):
    print('read binary file %s'%filename)
    fid = open(filename,'rb+')

    dataList = []
    for i in range(width * heigh*zsize):
        data = fid.read(4)
        val = struct.unpack('f',data)[0]
        #print(val)
        dataList.append(val)
    fid.close()
    return dataList


def readstructMaskFile(filename,width,heigh,zSize):
    print('read binary file %s'%filename)
    fid = open(filename,'rb+')

    dataList = []
    for i in range(width * heigh*zSize):
        data = fid.read(8)
        val = struct.unpack('Q',data)[0]

        #print(val)
        dataList.append(val)
    fid.close()

    test = np.reshape(dataList,(width,heigh,zSize))
   # getIdsFromMask(dataList)
    return dataList

# get structinfo ID
def getIdsFromMask(dataList):
    maxid = 0
    ids = []
    vns = []
    ll = len(dataList)
    for i in range(0,len(dataList)):
        if (dataList[i] > 0):
            tmpvar = math.ceil(math.log(dataList[i],2))
            if maxid < tmpvar:
                maxid = tmpvar
        
        
    for i in range(0,maxid):
        vn = 0
        for j in range(0,len(dataList)):
            if (dataList[j] & 2^i) > 0:
                vn = vn + 1
            
        if vn > 0:
            ids.append(i)
            vns.append(vn)
    return ids

# get structinfo ID
def writeBinFile(outputPath,dataList):
    with open('dose.bin','wb') as fp:
        for x in dataList:
            a = struct.pack('f',x)
            fp.write(a)

# write dose json
def writedoseJson(outputPath,xOldSize,yOldSize,numSlices,xPixelSpacing,yPixelSpacing,zPixelSacing,xoffset,yoffset,zOffset,xSize,ySize):
    dicrows = {}
    dicrows["rows"] = ySize
    dicrows["cols"] = xSize
    dicrows["numSlice"] = numSlices

    xnewRes = xOldSize / xSize * xPixelSpacing
    ynewRes = yOldSize / ySize * yPixelSpacing


    dicrows["xPixelSpacing"] = xnewRes#xSize / 256 * xPixelSpacing    #189 / 256 * 3
    dicrows["yPixelSpacing"] = ynewRes#ySize / 256 * yPixelSpacing
    dicrows["zPixelSpacing"] = zPixelSacing

    dicrows["precision"] = 4
    dicrows["doseGridScaling"] = 0.00007287
    dicrows["doseUnit"] = "cGy"
    dicrows["doseDataSize"] = xSize * ySize * numSlices

    dicrows["xStart"] = xoffset - xPixelSpacing / 2 + xnewRes / 2
    dicrows["yStart"] = yoffset - yPixelSpacing / 2 + ynewRes / 2
    dicrows["zStart"] = zOffset


    doseAtrrs = []
    for iLayer in range(0,numSlices):
        iBegin = xSize * ySize * iLayer
        iEnd = xSize * ySize * (iLayer + 1) - 1
        doseAtrr = {}
        doseAtrr["index"] = iLayer
        doseAtrr["beginPos"] = iBegin
        doseAtrr["endPos"] = iEnd
        doseAtrr["indexValue"] = zOffset + iLayer * zPixelSacing

        doseAtrrs.append(doseAtrr)

    dicrows["doseAtrr"] = doseAtrrs

    jsonStr = json.dumps(dicrows)
    jsonStr = jsonStr + '\n'
    outputfilename = outputPath + 'dose.json'
    with open(outputfilename,'a') as f:
        f.write(jsonStr)





# write json
def writestructMaskPos(posMap):
    dicrows = {}
    for struname in posMap.keys():
        tmpArray = posMap[struname]
        dicrows["name"] = struname

        points = []
        for i in range(len(tmpArray)):
            tmpPos = tmpArray[i]
            points.append(tmpPos[0])
            points.append(tmpPos[1])
            points.append(tmpPos[2])

        dicrows["points"] = points

    jsonStr = json.dumps(dicrows)
    with open('xyz.json','a') as f:
        f.write(jsonStr)
        f.write('\n')

def writeBinfiles(doseAttr,filename):
    with open(filename,'wb+') as fp:
        for x in range(len(doseAttr)):
            for y in range(len(doseAttr[x])):
                a = struct.pack('f',doseAttr[x][y])
                fp.write(a)


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path,i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
           
            



   
        





    


        

    




    













