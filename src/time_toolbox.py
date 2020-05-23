#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#===============================================================================
# Python3 Toolbox
# (c) 2011-2020 by Toussaint OTTAVI, t.ottavi@medi.fr
#===============================================================================
#
# Time-related functions
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

# TODO: Reorder / clean up
# TODO: Check Python 3 compatibility

Name = "Python Toolbox - Time library"
Version = "0.5"
VersionDate = "23/05/2020"


#===============================================================================
# Imports 
#===============================================================================

import time


################################################################################
#                                                                              #
#                            TIME PROCEDURES                                   #
#                                                                              # 
################################################################################

#===============================================================================
# Converts a Time Structure to seconds (float)
#===============================================================================

def StructToFloat (struct):
  try:
    secs = time.mktime(struct)
  except:
    secs=0
  return secs


#===============================================================================
# Converts a float into a Time Structure
#===============================================================================

def FloatToStruct (secs):
  try:
    struct = time.localtime (secs) 
  except:
    struct=None
  return struct


#===============================================================================
# Converts a float into a string
#===============================================================================

def FloatToString (secs):
  try:
    st =time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(secs))
  except:
    st = "<Conversion Error>"
  return st


#===============================================================================
# Converts a string into a float
#===============================================================================

def StringToFloat (st):
  try:
    secs = time.mktime(time.strptime(st,"%d/%m/%Y %H:%M:%S"))
  except:
    secs = 0
  return secs  


#===============================================================================
# Actual time in seconds (float)    
#===============================================================================

def NowFloat():
  try:
    secs = time.time()
  except:
    secs = 0
  return secs
  
  
#===============================================================================
# Actual seconds in string
#===============================================================================

def NowString():
  try:
    st = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
  except:
    st="<Error>"
  return st


#===============================================================================
# Converts time (secs) to string
#===============================================================================

def TimeToString(tm):
  try:
    st = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(tm))
  except:
    st = "Error"
  return st


#===============================================================================
# Converts string to time (secs)
#===============================================================================

def StringToTime (st):
  try:
    tm = time.mktime(time.strptime(st,"%d/%m/%Y %H:%M:%S"))
  except:
    tm = 0
  return tm
    

  
# TODO

# time.time() : renvoie now en float
# time.localtime (): renvoie now en tuple
# now en float: time.mktime(time.localtime()) ou time.time() (renvoient la mêm chose)


# Prendre un string et renvoyer un float :
# time.mktime(time.strptime(st,"%d/%m/%Y %H:%M:%S"))

# Prendre un tuple et renvoyer un string :
# time.strftime("%d/%m/%Y %H:%M:%S", float)

# Prendre un float et renvoyer un string :
# time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(f))


################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              # 
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr" %(Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")
