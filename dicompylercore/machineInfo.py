#!/root/anaconda3/bin/python3
# -*- coding: utf-8 -*-
import json
import numpy
import struct
import sys
import os



class MachineInfo:
    machineName = ""
    machineUid = 1
    source = "photon"
    minPairGap = 5
    maxleafspeed = 20
    leafSpan = 325
    bSupportleafCross = True
    bSplit = False
    bjawFixed = False
    maxHalfOverLap = 20.2
    energy = 6
    maxDoseRate = 600
    
    mlcSetting = []


    def __init__(self):
        machineName = 0

class JawSetting:
    xjawleftMaxPos = 125
    xjawleftMinPos = -200
    xjawrightMaxPos = 125
    xjawrightMinPos = -125
    
    yjawlowerMaxPos = 0
    yjawlowerMinPos = -200
    yjawupperMaxPos = 200
    yjawupperMinPos = 0

    def __init__(self):
        xjawleftMaxPos = 125




class Leaves:
    index = 0
    leafYPos = -200
    nextLeafYPos = -190
    minPosLeftLeaf = -200
    maxPosLeftLeaf = 125
    minPosRightLeaf = -125
    maxPosRightLeaf = 200


class MlcSetting:
    count = 40
    sAD = 1000
    leafesVec = []    #leaves 数组