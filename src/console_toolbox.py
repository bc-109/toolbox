#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#===============================================================================
# Python3 Toolbox
# (c) 2011-2020 by Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr
#===============================================================================
#
# Colsole toolbox (keyboard and screen output)
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

Name = "Python Toolbox - Console tools"
Version = "0.2"
VersionDate = "29/11/2020"


#===============================================================================
# Imports 
#===============================================================================

# Python standard imports

import asyncio


################################################################################
#                                                                              #
#                            PRINT TOOLS                                       #
#                                                                              # 
################################################################################    


#===============================================================================
# Prints with no carriage return
#===============================================================================

def print_nocr (item):
  print(item, end=" ")


#===============================================================================
# Prints on the same line 
#===============================================================================

def print_sameline (item):
  print(item, end='\r', flush=True)


################################################################################
#                                                                              #
#                            KEYBOARD CLASSES                                  #
#                                                                              # 
################################################################################    

#===============================================================================
# Checks platform and declares the right getch() function
#===============================================================================

import platform

#---------------------------------------------- Non-blocking GetChar for Windows

if platform.system() == "Windows":
  import msvcrt
  def getch():
    if msvcrt.kbhit() :
      k = msvcrt.getch()
    else:
      k=None
    return k    

#------------------------------------- Non-blocking GetChar for Linux (UNTESTED)

else:
  import tty, termios, sys
  def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch   


#===============================================================================
# Main keyboard class 
#===============================================================================

class cKeyboard():

  #----------------------------------------------------------------- Constructor
  
  def __init__(self):
    pass
  
  
  #-------------------------------------------------- Schedule AsyncIO coroutine
  
  def Start(self, loop):
    loop.create_task (self.WaitForKeyPressed(), name="Keyboard task") 
    
      
  #------------------------------------- AsyncIO coroutine - Check if keypressed
  
  async def WaitForKeyPressed(self):  
  
    print ('Keyboard task started.')
    while True:
      k = getch()
      if k is not None :
        print ('================================================================')
        print ("Keyboard : pressed %s " % k)
        print ('================================================================')
        # if k == b'\x03':
        #  print ('CTRL+C')
        #  raise (KeyboardInterrupt)
        
        if k == b' ':
          pass           # Do something HERE
          
      await asyncio.sleep(0.1) 



################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              # 
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, TK1BI, bc-109 Soft, t.ottavi@medi.fr" %(Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")