#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#===============================================================================
# Python3 Toolbox
# (c) 2011-2020 by Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr
#===============================================================================
#
# AsyncIO generic toolbox for starting / managing / stopping tasks
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

Name = "Python Toolbox - AsyncIO general library"
Version = "0.1"
VersionDate = "23/05/2020"


#===============================================================================
# Imports 
#===============================================================================

import asyncio
import platform
import signal 



################################################################################
#                                                                              #
#                             ASYNCIO SHUTDOWN                                 #
#                                                                              # 
################################################################################    
    

#===============================================================================
# Set event handlers on desired signals for shutdown (Linux only)
#===============================================================================


def SetShutdownSignals(loop):
    
  if platform.system() != "Windows":
    print('Shutdown : Initializing signals...')
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)  #  Not available on Windows
    for s in signals:
      loop.add_signal_handler(s, lambda s=s: asyncio.create_task(AsyncIOShutdown(loop, signal=s)))
  else:
    print ('Shutdown : Signals not supported (running in Windows)')
  

#===============================================================================
# AsyncIO graceful shutdown / Cancel pending tasks
#===============================================================================

async def AsyncIOShutdown(loop, signal=None):
  
  if platform.system() != "Windows":
    print (f"Shutdown : Received exit signal {signal.name}...")
   
  print ("Shutdown : Scheduling cancelation for all running tasks...")
  tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
  # print(tasks)
  for task in tasks:
    print(" - %s" % (task.get_name()))
    # print("Task details : %s" %(task))
    task.cancel()
  print (f"Shutdown : Requested cancelation for {len(tasks)} tasks...")
  await asyncio.gather(*tasks, return_exceptions=True)
  print (f"Shutdown : All tasks canceled. Stopping AsyncIO loop.")
  loop.stop()


  

################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              # 
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr" %(Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")