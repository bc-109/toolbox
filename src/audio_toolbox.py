#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#===============================================================================
# Python3 Toolbox
# (c) 2011-2020 by Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr
#===============================================================================
#
# Audio toolbox
#
#===============================================================================

#===============================================================================
#    This is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

Name = "Python Toolbox - Audio processing tools"
Version = "0.1"
VersionDate = "29/11/2020"


#===============================================================================
# Imports 
#===============================================================================

# Python standard imports

import struct
import numpy
import math


################################################################################
#                                                                              #
#                                  LEVELING                                    #
#                                                                              # 
################################################################################
      
#===============================================================================
# Simple maximum absolute value of a buffer
#===============================================================================
      
def GetAudioLevel (audio):
  
  audio16 = struct.unpack("<160h", audio)       # Unpacks buffer in an array of int16
  audio_max = max(numpy.absolute(audio16))     
  return audio_max


#===============================================================================
# Vu-Meter class
#===============================================================================

class cVuMeter():
  
  #----------------------------------------------------------------- Constructor
  
  def __init__ (self):
    self.value_prev = 0              # last value from the previous block
    self.coef       = 0.9
    self.value      = 0              # Intermediate calculated value
    self.output     = 0              # Final value in log
    
  
  #------------------------------------------------------------------- Get value
  
  def Get(self):
    return self.output


  #------------------------------------------------ Update value from audio data

  def Update(self, audio):  
    audio16 = struct.unpack("<160h", audio)       # Unpacks buffer in an array of int16
    # self.AlgoRMSPower (audio16)
    self.AlgoCapacitor(audio16)
  
  
  #-- ALGO 1 ----------------------------------- Calculate variance and RMS power  
  # https://www.dsprelated.com/showthread/comp.dsp/40956-1.php

  def AlgoRMSPower(self, audio16):
    
    try:
      for sample in audio16:
        value = self.coef * self.value_prev + (1 - self.coef) * (sample ** 2)
        self.value_prev = value        
      self.output = 10 * math.log10(value)
    except:
      self.output = 0
    
  
  #-- ALGO 2 ------------------------------------------------ Simulate capacitor
  # https://dsp.stackexchange.com/questions/49172/how-to-simulate-analog-vu-meter-response-to-audio

  def AlgoCapacitor(self, audio16):

    c = 0
    kCharge = 0.1
    kDischarge = 0.001

    try:
      for sample in audio16:
        x1 = abs(sample)
        if x1 > c :
          c = c * (1-kCharge) + x1 * kCharge
        else:
          c = c * (1-kDischarge)
      self.output = 10 * math.log10(c)
    except:  
      self.output = 0


################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              # 
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, TK1BI, bc-109 Soft, t.ottavi@medi.fr" %(Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")