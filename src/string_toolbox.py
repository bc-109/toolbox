#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#===============================================================================
# Python3 Toolbox
# (c) 2011-2020 by Toussaint OTTAVI, t.ottavi@medi.fr
#===============================================================================
#
# String toolbox
# - Provides various string-related procedures
# - Python3 string / bytes conversion 
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

Name = "Python Toolbox - String library"
Version = "0.5"
VersionDate = "23/05/2020"


################################################################################
#                                                                              #
#                          SUBSTRINGS / SEPARATORS                             #
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
    pos1 = s.find(sep1) + len(sep1)
    pos2 = s.find(sep2)
    tmp = s[pos1:pos2]
  except:
    tmp = ''
  return tmp


#===============================================================================
# Returns True if string contains substring
#===============================================================================

def StringContains (s, sub):
  flag = False
  if s!="":
    if s.find(sub)!=-1:
      flag= True 
  return flag  


#===============================================================================
# Removes all non alphanumeric characters from a string 
#===============================================================================

def StringToAlphaNum (s):
  ret = ''
  try:
    for c in s:
      if c.isalnum() : 
        ret = ret + c 
  except:
    ret='<Conversion Error>'
  return ret


#===============================================================================
# Removes all non alphanumeric characters from a string (keep spaces) 
#===============================================================================

def StringToAlphaNumWithSpace (s):
  ret = ''
  try:
    for c in s:
      if not(c.isalnum() or c==' '): 
        c='-'
      ret = ret + c 
  except:
    '<Conversion Error>'
  return ret


#===============================================================================
# Removes all non alphanumeric characters from a string and replaces by a . 
#===============================================================================

def StringToAlphaNumDot (s):
  ret = ''
  try:
    for c in s:
      if c.isalnum() : 
        ret = ret + c 
      else:
        ret = ret + '.'  
  except:
    ret='<Conversion Error>'
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


################################################################################
#                                                                              #
#                             PYTHON3 CONVERSIONS                              #
#                                                                              # 
################################################################################


#===============================================================================
# Convert a single byte in integer format to a 'bytes' string type
#===============================================================================

# In  : 65
# Out : b'A'

def byte (n):
  try:
    # ret = (chr.to_bytes(1, byteorder='big'))
    ret = bytes([n])                           # Simpler
  except:
    ret = '?'.encode()
  return ret 


#===============================================================================
# Convert a normal string to a Python 3 'bytes' string
#===============================================================================

def StringToBytes (s):

# In  : 'ABCD' or b'ABCD'
# Out : b'ABCD  

  try:
    if isinstance(s,bytes):
      ret = s
    else:  
      ret = s.encode()
  except:
    ret = b''
  return ret 
 
 
#==============================================================================
# Convert a Python 3 'bytes' string to normal string 
#==============================================================================

def StringToNormal (s):
  
# In  : b'ABCD' or 'ABCD'
# Out : 'ABCD  

  try:
    if isinstance(s,str):
      ret = s
    else:     
      ret = s.decode()
  except:
    ret = ''
  return ret


#===============================================================================
# Convert a hexdecimal string to bits string, with zero fillings (16 bits)
#===============================================================================

# In  : b'41' or '41' (decimal 64)
# Out : '01000001'

def HexToBin(hexstr):
  try:
    num_of_bits = len(hexstr) * 4
    binstr = bin(int(hexstr, 16))[2:].zfill(int(num_of_bits))
  except:
    binstr='00000000'
  return binstr


#===============================================================================
# Convert a bits string to hexdecimal string
#===============================================================================

# In  : '1000001' or b'1000001'
# Out : '41' (decimal 64)

def BinToHex(binstr):
  try:
    ret = "{0:X}".format(int(binstr, 2))
  except:
    ret = "00000000"
  return ret  


#===============================================================================
# Convert a decimal value to hexadecimal string
#===============================================================================
 
# In  : 10
# Out : '0a'    
  
def DecToHex (n):
  try:
    ret = "{0:x}".format(n)
  except:
    ret = "00" 
  return ret


#===============================================================================
# Convert an hexadecimal string to decimal value 
#===============================================================================

# In : '0a'
# Out : 10

def HexToDec (s):
  try:
    ret = int(s, base=16)
  except:
    ret = 0
  return ret    
  
  
#===============================================================================
# Converts raw string to hex string 
#===============================================================================

# In  : b'ABC' or 'ABC'
# Out : '414243'

def RawToHex(s):
  try : 
    if isinstance(s,str): 
      s = StringToBytes(s)
    ret = "".join("%02X" % i for i in s)
  except:
    ret = "0"
  return ret  


#===============================================================================
# Converts hex string to raw string 
#===============================================================================

def HexToRaw (hexstr):

# In  : '414243'
# Out : b'ABC 

  rawstr = b''
  try:
    if isinstance(hexstr,bytes): 
      hexstr = StringToNormal(hexstr)
    num_of_bytes = len(hexstr) // 2
    for i in range(num_of_bytes):
      p = 2*i
      h = '0x'+hexstr[p:p+2]
      hint = int(h,base=16)
      hbin = bytes([hint])
      rawstr = rawstr + hbin
  except:
    rawstr=b''
  return rawstr    



################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              # 
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr" %(Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")
   
