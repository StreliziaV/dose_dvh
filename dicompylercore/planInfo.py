#!/root/anaconda3/bin/python3
# -*- coding: utf-8 -*-
import json
import numpy
import struct
import sys
import os

from dicompylercore.commconf import structureType
from dicompylercore.commconf import PlayType

class PlanInfo:
    ref_rtplan_id = 0
    numberOfFractions = 25
    playType = PlayType.SLIDING_WINDOW

    def __init__(self):
        self.ref_rtplan_id = 0


class Structinfo:
    structId = 0
    stryucreType = structureType.STRUCTURE_PTV
    name = ''

    def __init__(self):
        id = 0
        name = ''

class StructurePara:
    structIndex = 0
    volume = 0
    dose = 0
    overweight = 0
    underweight = 0

    def __init__(self):
        self.structIndex = 0
        self.volume = 0
        self.dose = 0
        self.overweight = 0
        self.underweight = 0

    def __init__(self,istructIndex,ivolume,idose,ioverweight,iunderweight):
        self.structIndex = istructIndex
        self.volume = ivolume
        self.dose = idose
        self.overweight = ioverweight
        self.underweight = iunderweight


class BeamInfo:
    beamId = 0
    beamName = ""
    couchAngle = 0
    gantryAngle = 0
    collimatgorAngle = 0
    weight = 0
    mu = 0

    def __init__(self):
        self.beamId = 0
        self.couchAngle = 0
        self.gantryAngle = 0
        self.collimatgorAngle = 0


    #def __init__(self,ibeamId,icouchangle,igantryAngle,icollimatorAngle,iisocenter):
    #    self.beamId = ibeamId
    #    self.couchAngle = icouchangle
    #    self.gantryAngle = igantryAngle
    #    self.collimatgorAngle = icollimatorAngle
    #    self.iisocenter = iisocenter
        
        


