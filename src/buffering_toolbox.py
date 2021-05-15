#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#===============================================================================
# Python3 Toolbox
# (c) 2011-2020 by Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr
#===============================================================================
#
# Queue and buffering toolbox (Various functions about queues and buffering)
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

Name = "Python Toolbox - Queue and buffering tools"
Version = "0.2"
VersionDate = "15/05/2021"


#===============================================================================
# Imports 
#===============================================================================

# Python standard imports

import asyncio
import queue
import numpy as np



################################################################################
#                                                                              #
#                              CUSTOM QUEUE CLASS                              #
#                                                                              # 
################################################################################

#===============================================================================
# Custom queue class, derived from standard Queue, with clear() method
#===============================================================================

class cMyQueue(queue.Queue):

  #------------------------------------------------- Clears all items of a queue
  # (https://stackoverflow.com/questions/6517953/clear-all-items-from-the-queue)
  
  def clear(self):
  
    with self.mutex:
      unfinished = self.unfinished_tasks - len(self.queue)
      if unfinished <= 0:
        if unfinished < 0:
          raise ValueError('Queue clearing : error, task_done() called too many times')
        self.all_tasks_done.notify_all()
      self.unfinished_tasks = unfinished
      self.queue.clear()
      self.not_full.notify_all()
      
      
################################################################################
#                                                                              #
#                              CIRCULAR BUFFER                                 #
#                                                                              # 
################################################################################      

#===============================================================================
# Perpetual circular buffer 
#===============================================================================

# Stores data in blocks in a NymPy array. When filled, writes over the oldest data 
# (without cheching whether it has been processed or not).
# Typically used for storing the last <x> seconds of a voice message.

class cCircularBuffer():

  #----------------------------------------------------------------- Constructor
  
  def __init__(self, dtype=np.float32, blocksize=160, maxblocks = 20):
    
    self.dtype      = dtype                                # Data type of one element
    self.blocksize  = blocksize                            # Number of elements in a block
    self.maxblocks  = maxblocks                            # Total number of blocks stored in the buffer
    self.buffersize = self.maxblocks * self.blocksize
    self.buffer     = np.zeros(shape=(self.buffersize), dtype=self.dtype)     # Empty NumPy array of required size 
    
    self.pointer    = 0                                    # Position for inserting data
    self.filled     = False
    
    
  #---------------------------------------------------------- Add data to buffer
  # Add data in the buffer at the pointer position
  # TODO : check if data is numpy array 
  # TODO : try/except
  
  def AddData(self, data):
    
    l = len(data)
    if l == self.blocksize:
      beg = self.pointer
      end = self.pointer + self.blocksize
      self.buffer[beg:end] = data
      self.pointer = end
      if self.pointer >= self.buffersize:
        self.filled = True
        self.pointer = 0  
      else:
        self.filled = False      
    else:
      print ("ERROR CircularBuffer AddData : wrong data size, must be equal to blocksize")  

  
  #--------------------------------------------------- Extracts data from buffer
  # Full data buffer is extracted from position of pointer
  
  def GetData(self):
    
    if self.pointer == 0 :
      res = self.buffer
    else :
      part1 = self.buffer[self.pointer:self.buffersize]
      part2 = self.buffer[0:self.pointer]
      res = np.concatenate((part1, part2))  
    return res
  
  
  #------------------------- Checks if circular buffer made a full filling cycle
  
  def CheckFilled(self):
    #print ("CheckFilled Pointer : %d  Filled : %s " % (self.pointer, self.filled))
    return self.filled



################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              # 
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, TK1BI, bc-109 Soft, t.ottavi@medi.fr" %(Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")