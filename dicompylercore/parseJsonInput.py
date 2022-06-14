#!/root/anaconda3/bin/python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------
#
#filename:
#author:
#date:
#last_modified:
#Description
#
#----------------------------------------------------------------
import json
import numpy
import struct
import sys
import os
import matplotlib.pyplot as plt

from dicompylercore.planInfo import PlanInfo
from dicompylercore.planInfo import Structinfo
from dicompylercore.planInfo import StructurePara
from dicompylercore.machineInfo import MachineInfo
from dicompylercore.machineInfo import JawSetting
from dicompylercore.machineInfo import Leaves
from dicompylercore.machineInfo import MlcSetting
from dicompylercore.LinkCtinfo import LinkCtInfo
from dicompylercore.planInfo import BeamInfo

from dicompylercore.commconf import structureType
from dicompylercore.commconf import PlayType

from dicompylercore.Converbinfile import getIdsFromMask
from dicompylercore.Converbinfile import writedoseJson
from dicompylercore.Converbinfile import writestructMaskPos
from dicompylercore.Converbinfile import writeBinfiles

jsonfile_rootdir = 'C:\\Users\\xuweilan\\Desktop\\autoPlanInputParams.json'

currentFilePath = os.path.abspath(__file__)
currentFileDir = os.path.dirname(currentFilePath) + os.sep
libpath = currentFileDir




class ParseJsonInput:
    infilename = ""


    def __init__(self):
        self.infilename = ''
        self.planInfo = PlanInfo()
        self.structInfos = []
        self.structParas = []
        self.beams = []
        self.machineInfo = MachineInfo()
        self.jawSetting = JawSetting()

        self.mlcsetting = MlcSetting()
        self.linkctinfo = LinkCtInfo()
        self.doseinfo = LinkCtInfo()

    def setInfilename(self,inputfilePath):
        self.infilename = inputfilePath




# read json file
    def readMachine(self, machinefJson):
        #machineInfo = MachineInfo()
        self.machineInfo.machineName = machinefJson["machineName"]
        self.machineInfo.machineUid = machinefJson["machineUid"]
        self.machineInfo.source = machinefJson["source"]
        self.machineInfo.minPairGap = machinefJson["minPairGap"]
        self.machineInfo.maxleafspeed = machinefJson["maxleafspeed"]
        self.machineInfo.leafSpan = machinefJson["leafSpan"]
        self.machineInfo.bSupportleafCross = machinefJson["bSupportleafCross"]
        self.machineInfo.bSplit = machinefJson["bSplit"]
        self.machineInfo.bjawFixed = machinefJson["bjawFixed"]
        self.machineInfo.maxHalfOverLap = machinefJson["maxHalfOverLap"]
        self.machineInfo.energy = machinefJson["energy"]
        self.machineInfo.maxDoseRate = machinefJson["maxDoseRate"]

        jawsettingJson = machinefJson["jawSetting"]
        jawSettingsJson = jawsettingJson["jaws"]
        xjawSettingJson = jawSettingsJson["xjaw"]
        yjawSettingJson = jawSettingsJson["yjaw"]


        self.jawSetting.xjawleftMaxPos = xjawSettingJson["leftMaxPos"]
        self.jawSetting.xjawleftMinPos = xjawSettingJson["leftMinPos"]
        self.jawSetting.xjawrightMaxPos = xjawSettingJson["rightMaxPos"]
        self.jawSetting.xjawrightMinPos = xjawSettingJson["rightMinPos"]

        self.jawSetting.yjawlowerMaxPos = yjawSettingJson["lowerMaxPos"]
        self.jawSetting.yjawlowerMinPos = yjawSettingJson["lowerMinPos"]
        self.jawSetting.yjawupperMaxPos = yjawSettingJson["upperMaxPos"]
        self.jawSetting.yjawupperMinPos = yjawSettingJson["upperMinPos"]

        mlcSettingJson = machinefJson["mlcSetting"]
        self.mlcsetting.count = mlcSettingJson["count"]
        jsleaves = mlcSettingJson["leaves"]
        for item in range(0,len(jsleaves)):
            jsitem = jsleaves[item]
            tmpleaves = Leaves()
            tmpleaves.index = jsitem["index"]
            tmpleaves.leafYPos = jsitem["leafYPos"]
            tmpleaves.nextLeafYPos = jsitem["nextLeafYPos"]
            tmpleaves.minPosLeftLeaf = jsitem["minPosLeftLeaf"]
            tmpleaves.maxPosLeftLeaf = jsitem["maxPosLeftLeaf"]
            tmpleaves.minPosRightLeaf = jsitem["minPosRightLeaf"]
            tmpleaves.maxPosRightLeaf = jsitem["maxPosRightLeaf"]

            self.mlcsetting.leaves.append(tmpleaves)
        #mlcSetting.leafesVec = leaves[40]



# read plan and ct info
    def readPlanInfo(self,planJson):
        #planInfo = PlanInfo()
        self.planInfo.ref_rtplan_id = planJson["planId"]

        ctinfoJson = planJson["patientctInfo"]
        self.linkctinfo.numSlices = ctinfoJson["numSlices"]
        self.linkctinfo.xSize = ctinfoJson["xSize"]
        self.linkctinfo.ySize = ctinfoJson["ySize"]
        self.linkctinfo.xOffset = ctinfoJson["xOffset"]
        self.linkctinfo.yOffset = ctinfoJson["yOffset"]
        self.linkctinfo.zOffset = ctinfoJson["zOffset"]
        self.linkctinfo.xPixelSpacing = ctinfoJson["xPixelSpacing"]
        self.linkctinfo.yPixelSpacing = ctinfoJson["yPixelSpacing"]
        self.linkctinfo.zPixelSacing = ctinfoJson["zPixelSpacing"]

        self.linkctinfo.winlevel = ctinfoJson["winlevel"]
        self.linkctinfo.winwidth = ctinfoJson["winwidth"]
        self.linkctinfo.rescalIntercept = ctinfoJson["rescalIntercept"]
        self.linkctinfo.rescalSlope = ctinfoJson["rescalSlope"]

        self.linkctinfo.imageOrientationPatient.clear()
        imageOriJobject = ctinfoJson["imageOrientationPatient"]
        for item in range(0, len(imageOriJobject)):
            self.linkctinfo.imageOrientationPatient.append(imageOriJobject[item])

        imagePosObj = ctinfoJson["imagePositionPatient"]
        for item in range(0, len(imagePosObj)):
            self.linkctinfo.imagePositionPatient.append(imagePosObj[item])

        pixelSpacObj = ctinfoJson["pixelSpacing"]
        for item in range(0, len(pixelSpacObj)):
            self.linkctinfo.pixelSpacing.append(pixelSpacObj[item])

        self.linkctinfo.patientPostion = ctinfoJson["patientPosition"]
        self.linkctinfo.photometricInterpretation = ctinfoJson["photometricInterpretation"]
        self.linkctinfo.samplesPerPixel = ctinfoJson["samplesPerPixel"]

        ctinfoJson = planJson["dosegrid"]
        self.doseinfo.numSlices = ctinfoJson["zSize"]
        self.doseinfo.xSize = ctinfoJson["xSize"]
        self.doseinfo.ySize = ctinfoJson["ySize"]
        self.doseinfo.xOffset = ctinfoJson["xStart"]
        self.doseinfo.yOffset = ctinfoJson["yStart"]
        self.doseinfo.zOffset = ctinfoJson["zStart"]
        self.doseinfo.xPixelSpacing = ctinfoJson["xSpacing"]
        self.doseinfo.yPixelSpacing = ctinfoJson["ySpacing"]
        self.doseinfo.zPixelSacing = ctinfoJson["zSpacing"]


        # below is beam
        # beamJsons = planJson["beams"]
        # for i in range(0,len(beamJsons)):
        #     tmpbeam = BeamInfo()
        #     tmpbeam.beamId = beamJsons[i]["beamId"]
        #     tmpbeam.beamName = beamJsons[i]["beamName"]
        #     tmpbeam.couchAngle = beamJsons[i]["couchAngle"]
        #     tmpbeam.gantryAngle = beamJsons[i]["gantryAngle"]
        #     tmpbeam.collimatorAngle = beamJsons[i]["collimatorAngle"]
        #     self.beams.append(tmpbeam)


        #ctfilePath = "D:\\2371-DAO\\input\\";
        #self.linkctinfo.readCTData(self.infilename)
       # writedoseJson(ctfilePath,self.linkctinfo.xSize,self.linkctinfo.ySize,self.linkctinfo.numSlices,self.linkctinfo.xPixelSpacing,self.linkctinfo.yPixelSpacing,self.linkctinfo.zPixelSacing,self.linkctinfo.zOffset)
        #self.linkctinfo.readStructmaskData(self.infilename)

# read structinfo
    def readStructInfo(self,structJson):
        structInfoJsonList = structJson["structInfoList"]
        for item in range(0,len(structInfoJsonList)):
            tmpstructInfo = Structinfo()
            tmpstructInfo.name = structInfoJsonList[item]["stdName"]
            tmpstructInfo.structId = structInfoJsonList[item]["id"]

            tmpstructType = structInfoJsonList[item]["structureType"]
            if tmpstructType == "STRUCTURE_PTV":
                tmpstructInfo.stryucreType = structureType.STRUCTURE_PTV
            elif tmpstructType == "STRUCTURE_OAR":
                tmpstructInfo.stryucreType = structureType.STRUCTURE_OAR
            else:
                tmpstructInfo.stryucreType = structureType.STRUCTURE_BODY
            self.structInfos.append(tmpstructInfo)

    def GetStructNamebyStructID(self,structID):
        strName = ''
        for i in range(len(self.structInfos)):
            tmpstructInfo = self.structInfos[i]
            if tmpstructInfo.structId == int(structID):
                strName = tmpstructInfo.name
                break
        return strName

    def GetStructIDbyStrductInfo(self,structNumber):
        allind = []
        bstr = bin(structNumber)
        bstr = bstr[::-1]
        count = 0
        instr = 0
        for eachchar in bstr:
            count += 1
            if eachchar == '1':
                allind.append(count - 1)
        if int(bin(structNumber).replace('0b','')) != 0:
            instr = str(allind[0])

        return instr



# read structparss
    def readStructParas(self,structParaJson):
        structParaJsonList = structParaJson["structParaList"]
        for item in range(0,len(structParaJsonList)):
            tmpstructPara = StructurePara()
            tmpstructPara.dose = structParaJsonList[item]["structParaIndex"]
            tmpstructPara.dose = structParaJsonList[item]["volume"]
            tmpstructPara.dose = structParaJsonList[item]["dose"]
            tmpstructPara.dose = structParaJsonList[item]["underweight"]
            tmpstructPara.dose = structParaJsonList[item]["overweight"]
            self.structParas.append(tmpstructPara)

    def readJsoninput(self):
        inputfile = self.infilename + "/autoPlanInputParams.json"
        jsfile = open(inputfile,'r')
        tempJson = json.load(jsfile)
        machinfJson = tempJson["machineUnitInfo"]        #解析machineUnitInfo
        planJson = tempJson["planInfo"]                  #解析planInfo
        structInfoJson = tempJson["structInfo"]          #解析structInfo
        structureParaJson = tempJson["structureParas"]   #解析structureParas
        structInfoJason = tempJson["structInfo"]

        self.readPlanInfo(planJson)

        self.readStructInfo(structInfoJason)
        #self.readMachine(machinfJson)
        return tempJson

    def GetDoseGrid(self,infilename):
        inputfile = infilename + "/autoPlanInputParams.json"
        print(inputfile)
        jsfile = open(inputfile, 'r')
        tempJson = json.load(jsfile)
        planJson = tempJson["planInfo"]  # 解析planInfo

        ctinfoJson = planJson["dosegrid"]
        doseGridinfo = LinkCtInfo()

        doseGridinfo.numSlices = ctinfoJson["zSize"]
        doseGridinfo.xSize = ctinfoJson["xSize"]
        doseGridinfo.ySize = ctinfoJson["ySize"]
        doseGridinfo.xOffset = ctinfoJson["xStart"]
        doseGridinfo.yOffset = ctinfoJson["yStart"]
        doseGridinfo.zOffset = ctinfoJson["zStart"]
        doseGridinfo.xPixelSpacing = ctinfoJson["xSpacing"]
        doseGridinfo.yPixelSpacing = ctinfoJson["ySpacing"]
        doseGridinfo.zPixelSacing = ctinfoJson["zSpacing"]

        return doseGridinfo

    def GetCTGrid(self,infilename):
        inputfile = infilename + "/autoPlanInputParams.json"
        jsfile = open(inputfile, 'r')
        tempJson = json.load(jsfile)
        planJson = tempJson["planInfo"]  # 解析planInfo

        ctinfoJson = planJson["patientctInfo"]
        linkctinfo = LinkCtInfo()

        linkctinfo.numSlices = ctinfoJson["numSlices"]
        linkctinfo.xSize = ctinfoJson["xSize"]
        linkctinfo.ySize = ctinfoJson["ySize"]
        linkctinfo.xOffset = ctinfoJson["xOffset"]
        linkctinfo.yOffset = ctinfoJson["yOffset"]
        linkctinfo.zOffset = ctinfoJson["zOffset"]
        linkctinfo.xPixelSpacing = ctinfoJson["xPixelSpacing"]
        linkctinfo.yPixelSpacing = ctinfoJson["yPixelSpacing"]
        linkctinfo.zPixelSacing = ctinfoJson["zPixelSpacing"]

        linkctinfo.winlevel = ctinfoJson["winlevel"]
        linkctinfo.winwidth = ctinfoJson["winwidth"]
        linkctinfo.rescalIntercept = ctinfoJson["rescalIntercept"]
        linkctinfo.rescalSlope = ctinfoJson["rescalSlope"]

        linkctinfo.imageOrientationPatient.clear()
        imageOriJobject = ctinfoJson["imageOrientationPatient"]
        for item in range(0,len(imageOriJobject)):
            linkctinfo.imageOrientationPatient.append(imageOriJobject[item])

        imagePosObj = ctinfoJson["imagePositionPatient"]
        for item in range(0,len(imagePosObj)):
            linkctinfo.imagePositionPatient.append(imagePosObj[item])

        pixelSpacObj = ctinfoJson["pixelSpacing"]
        for item in range(0,len(pixelSpacObj)):
            linkctinfo.pixelSpacing.append(pixelSpacObj[item])

        linkctinfo.patientPostion = ctinfoJson["patientPosition"]
        linkctinfo.photometricInterpretation = ctinfoJson["photometricInterpretation"]
        linkctinfo.samplesPerPixel = ctinfoJson["samplesPerPixel"]

        return linkctinfo



        

    def GetStructName(self):
        structNameArray = []
        for i in range(len(self.structInfos)):
            structName = self.structInfos[i].name
            structNameArray.append(structName)
        return structNameArray


    def GetStructInfoCounts(self):
        return len(self.structInfos)

    def GetNumSlice(self):
        return self.linkctinfo.numSlices


    def CalPointbyIndex(self,row,col,slice):
        xStart = self.linkctinfo.xOffset
        yStart = self.linkctinfo.yOffset
        zStart = self.linkctinfo.zOffset

        xPixelSpacing = self.linkctinfo.xPixelSpacing
        yPixelSpacing = self.linkctinfo.yPixelSpacing
        zPixelSpacing = self.linkctinfo.zPixelSpcing

        xPos = xStart + row * xPixelSpacing
        yPos = yStart + col * yPixelSpacing
        zPos = zStart + slice * zPixelSpacing

        return xPos,yPos,zPos

########################output dose #############################
    def loadnpzfile(self,npzdir):
        npzfiles = [name for name in os.listdir(npzdir)if name.endswith('.npz')]
        filename = 'dose.bin'
        for i in range(len(npzfiles)):
            npzfile = npzfiles[i]
            npzpath = os.path.join(npzdir,npzfile)
            dose=numpy.load(npzpath)
            tmpdoseArry = dose['dose']
            doseArray = numpy.reshape(tmpdoseArry,(256,256))
            plt.imshow(doseArray)
            plt.show()
            writeBinfiles(doseArray,filename)

  #  def GetXYZPosition(self,layerdata):




######################Converet##################################
    def ConvertContourPoint(self):
        dimx = self.linkctinfo.xSize
        dimy = self.linkctinfo.ySize
        dimz = self.linkctinfo.numSlices


        data_np = numpy.array(self.linkctinfo.structmask,dtype = numpy.uint64)
        #etIdsFromMask(data_np)
        data = numpy.reshape(data_np,(dimz,dimx,dimy))
        posMap = {}
        posAttr = []

        for sliceLayer in range(dimz):
                #if sliceLayer != 12:
                    #continue

                dataLayer = data[sliceLayer,:,:]  #768 * 768
                uniques = numpy.unique(dataLayer) #0 256 214 512
                test_mask = numpy.zeros(shape=[dimx,dimy,len(uniques)],dtype=int)

                for i in range(len(uniques)):   #structindex  288 is PTV
                    structId = self.GetStructIDbyStrductInfo(uniques[i])
                    struName = self.GetStructNamebyStructID(structId)

                    if structId == 0 or struName == '':
                        continue

                    print('slicelayer,structId,structName :{}/{}-{}'.format(sliceLayer, structId,struName))

                    ind_mask=numpy.argwhere(dataLayer==uniques[i]) #找出某一层里structid=某个数的值(482076,2)482076个2维数组
                    indx_mask=ind_mask[:,0]  #符合条件的所有行
                    indy_mask=ind_mask[:,1]  #符合条件的所有列

                    tmpmask = numpy.zeros_like(dataLayer)

                    for j in range(ind_mask.size//2):  #482076
                        tmpmask[indx_mask[j],indy_mask[j]] = 1  #将符合条件的所有网格置1
                    sumpoint = 0
                    #plt.imshow(tmpmask)
                    #plt.show()
                    for m in range(dimx):
                        for n in range(dimy):

                            test_mask[m,n,i] = tmpmask[m,n]  #每一层的勾画信息,i 是structid

                            if (tmpmask[m,n] > 0):
                                sumpoint=sumpoint+1
                                xPos = self.linkctinfo.xOffset + m * self.linkctinfo.xPixelSpacing
                                yPos = self.linkctinfo.yOffset + n * self.linkctinfo.yPixelSpacing
                                zPos = self.linkctinfo.zOffset + sliceLayer * self.linkctinfo.zPixelSacing
                                tmpPosArray = [xPos,yPos,zPos]
                                #print('row,col,xpos,ypos,zpos :{}/{}:{},{},{}'.format(m,n,xPos,yPos,zPos))
                                posAttr.append(tmpPosArray)

                    if struName in posMap:
                        tmpArray = posMap[struName]
                        for pos in range(len(posAttr)):
                            tmpArray.append(posAttr[pos])
                            posMap[struName] = tmpArray
                    else:
                         posMap[struName] = posAttr


        writestructMaskPos(posMap) #输出json文件
        #dicrows = {}
        #for struname in posMap.keys():
        #    tmpArray = posMap[struname]
        #    dicrows["name"] = struname

        #    points = []
        #    for i in range(tmpArray):
        #        tmpPos = tmpArray[i]
        #        points.append(tmpPos[0])
        #        points.append(tmpPos[1])
        #        points.append(tmpPos[2])

        #    dicrows["points"] = points

        #jsonStr = json.dump(dicrows)
        #with open('xyz.json','a') as f:
        #    f.write(jsonStr)
        #    f.write('\n')



########################below is output###########################
    def updateBeamInfo(beamId,beamInfo):
        for item in range(0,len(beamInfo)):
            i = i+1

######################get parameters##############################
    def getStructTypebyindex(self,structIndex):
        type = 0
        for item in range(0,len(self.structInfos)):
            if (self.structInfos[item].structId == structIndex):
                type = self.structInfos[item].stryucreType


    def getCancerClassbyindex(self,structIndex):
        cancerStr = ""
        for item in range(0,len(self.structInfos)):
            if (self.structInfos[item].structId == structIndex):
                cancerStr = self.structInfos[item].cancerClass


####################################################################
def readdoseattr(infilename):
    inputfile = infilename + "/OutPutBeam/dose.json"
    jsfile = open(inputfile, 'r')
    tempJson = json.load(jsfile)

    refdose = LinkCtInfo()
    ySize = tempJson["rows"]
    xSize = tempJson["cols"]
    numSlices = tempJson["numSlice"]
    xPixelSpacing = tempJson["xPixelSpacing"]
    yPixelSpacing = tempJson["yPixelSpacing"]
    zPixelSacing = tempJson["zPixelSpacing"]
    xoffset = tempJson["xStart"]
    yoffset = tempJson["yStart"]
    zOffset = tempJson["zStart"]

    refdose.xSize = xSize
    refdose.ySize = ySize
    refdose.numSlices = numSlices
    refdose.xPixelSpacing = xPixelSpacing
    refdose.yPixelSpacing = yPixelSpacing
    refdose.zPixelSacing = zPixelSacing
    refdose.xOffset = xoffset
    refdose.yOffset = yoffset
    refdose.zOffset = zOffset

    return refdose


##############################main#################################
#  need input json  & output json & internal dir
if __name__ == '__main__':
    print('len(sys.argv):%d'%len(sys.argv))
    if len(sys.argv) < 4:
        print('usage:runopt.py runopt optDir')
        exit()

    interfaceName = sys.argv[2]
    outputDir = sys.argv[3]
    optDir = sys.argv[1]
    internalDir = sys.argv[1]

    if len(sys.argv) >= 5:
        internalDir = sys.argv[4]










   