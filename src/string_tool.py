#!/usr/bin/python
# -*- coding: UTF-8 -*-

#===============================================================================
# Python Toolbox
# (c) 2011 by Toussaint OTTAVI, t.ottavi@medi.fr
#===============================================================================
#
# mystring unit
# - Provides various string-related procedures
#
#===============================================================================

Version = "0.4"
VersionDate = "15/03/2015"


#===============================================================================
# Imports 
#===============================================================================

import string, time


################################################################################
#                                                                              #
#                           P R O C E D U R E S                                #
#                                                                              # 
################################################################################


#===============================================================================
# Returns string from separator to end of line (if multiline files)
#===============================================================================

def StringToEndAfter(s, separator):
  try:
    tmp = s.partition(separator)[2].splitlines()[0]
  except:
    tmp = ""  
  return tmp


#===============================================================================
# Return string from separator to end
#===============================================================================

def StringAfter(s, separator):
  try:
    tmp = s.partition(separator)[2]
  except:
    tmp = ""  
  return tmp


#===============================================================================
# Return string between two separators
#===============================================================================

def StringBetween(s, sep1, sep2):
  try:
    pos1 = string.find(s, sep1) + len(sep1)
    pos2 = string.find(s, sep2)
    tmp = s[pos1:pos2]
  except:
    tmp = ''
  return tmp


#===============================================================================
# Returns True if string contains substring
#===============================================================================

def StringContains (s, sub):
  flag = False
  if s<>"":
    if string.find(s, sub)<>-1:
      flag= True 
  return flag  

#===============================================================================
# Removes all non alphanumeric characters from a string 
#===============================================================================

def StringToAlphaNum (s):
  ret = ''
  try:
    for c in s:
      if not(c.isalnum() or c==' '): 
        c='-'
      ret = ret + c 
  except:
    pass
  return ret


#===============================================================================
# Normalize string : only keep 32..127 ascii codes
#===============================================================================

def StringNormalize (s):
  ret = ''
  try:
    for c in s:
      cc=ord(c)
      if cc>=32 and cc<127:
        r = c
      else:
        r = '?'
      ret = ret + r 
  except:
    pass
  return ret


#===============================================================================
# Removes multiple spaces in a string
#===============================================================================


def RemoveMultipleSpaces (s):
  ret = ''
  try:
    ret = " ".join(s.split())
  except:
    pass
  return ret


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
    

################################################################################
#                                                                              #
#                           E N C O D I N G S                                  #
#                                                                              # 
################################################################################

#===============================================================================
# Convert utf-8 to Unicode
#===============================================================================

def utf82unicode (s):
  r = ""
  try:
    r = s.decode('utf8', 'replace')
  except:
    r = "<Decoding Error>"
  return r


#===============================================================================
# Convert Ascii to Unicode
#===============================================================================

def ascii2unicode (s):
  r = ""
  try:
    r = s.decode('ascii','replace')
  except:
    r = "<Decoding Error>"
  return r

#===============================================================================
# Convert latin1 to Unicode
#===============================================================================

def latin12unicode (s):
  r = ""
  try:
    r = s.decode('latin1','replace')
  except:
    r = "<Decoding Error>"
  return r
   
    
#===============================================================================
# Convert Unicode to Ascii
#===============================================================================
 
def unicode2ascii (s): 
  r = ""
  try:
    r = s.encode('ascii','replace')
  except:
    r = "<Encoding Error>"    
  return r 
   

#===============================================================================
# Convert Unicode to utf-8
#===============================================================================
 
def unicode2utf8 (s): 
  r = ""
  try:
    r = s.encode('utf8','replace')
  except:
    r = "<Encoding Error>"    
  return r 


#===============================================================================
# Convert Unicode to latin-1 (=iso-8859-1)
#===============================================================================

def unicode2latin1 (s):   
  r = ""
  try:
    r = s.encode('latin1','replace')
  except:
    r = "<Encoding Error>"    
  return r 


################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              # 
################################################################################

if __name__ == "__main__":
  print ("Python Toolbox - String library - (c) Toussaint OTTAVI, t.ottavi@medi.fr")
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library unit, to be called from other modules. It does nothing by itself.")
   
