#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# ===============================================================================
#   Python3 Toolbox
#   (c) 2011-2022 by Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr
# ===============================================================================
#
#   This is a template for writing full AsyncIO software, with proper signal
#   handling and task shutdown.
#
# ===============================================================================
#
#    This is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
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
#
# ===============================================================================


# ===============================================================================
# Info & version Number
# ===============================================================================

__appname__     = "asyncio_template"
__description__ = "Template for writing AsyncIO software with proper task cancelation"
__author__      = 'Toussaint OTTAVI, TK1BI, bc-109 Soft'
__copyright__   = '(c) 2022 by Toussaint OTTAVI, TK1BI, bc-109 Soft'
__license__     = 'GNU GPLv3'
__maintainer__  = __author__
__email__       = 't.ottavi@medi.fr'
__version__     = '0.1'
__versiondate__ = '20221230'


# ===============================================================================
# Imports
# ===============================================================================

# Python standard imports

print ('Importing standard libs...')
pass


# Imports from my personal toolbox library

print ('Importing personal toolbox libs...')
from asyncio_toolbox import *
from asyncio_udp_toolbox import *
from logging_toolbox import *


###############################################################################
#                                                                             #
#                            ASYNCIO DERIVED CLASSES                          #
#                                                                             #
###############################################################################


#==============================================================================
# Test class (derive this from the required AsyncIO class)
#==============================================================================

class cTestClass():
  
  #---------------------------------------------------------------- Constructor

  def __init__(self, loop, name):

    # Call init of parent class if needed
    # super().__init__(loop, parameters)

    # Specific settings for this subclass
    self.loop = loop
    self.name = name
    self.running = False


  # ---------------------------------------------- Start related AsyncIO tasks

  def Start (self):
    
    logger.info ("%s starting AsyncIO task : Main Loop..." % self.name )
    self.loop.create_task (self.MainLoop (), name="%s main loop" % self.name)

    logger.info ("%s starting AsyncIO task : Heartbeat..." % self.name )
    self.loop.create_task (self.HeartBeat (), name="%s heartbeat" % self.name)


  # ---------------------- Example of main asynchronous process for this class

  async def MainLoop (self):
    
    try:
      while True:
      
        # ---- Start / Connect to server
        logger.info ("%s Main Loop - Starting / connecting..." % self.name)
        # await self.client.connect (self.hostname)
        logger.info ("%s Main Loop - Connected / running." % self.name)
        self.running = True
      
        # ---- Do something
        await asyncio.sleep(10)
        
        # ---- Await for external event
        # await self.stopflag.wait ()
        # logger.info ("  Received STOP event")
      
        # ---- Await for disconnect event
        # await self.client.disconnect ()
        logger.info ("%s Main Loop - Stopped / disconnected." % self.name)
        self.running = False
        
        # ---- Pause before restarting
        await asyncio.sleep (3)

    except asyncio.CancelledError :
      logger.info ("%s Main Loop - Received cancelation request" % self.name)
      # --- Clean up things here
      pass
      logger.info ("%s Main Loop - Task terminated gracefully." % self.name)


  #---------------------------------- Example of heartbeat task for this class

  async def HeartBeat(self):
  
    try:
      while True:
        # ---- Do something
        if self.running:
          logger.info ("%s Heartbeat" % self.name)
        
        # ---- Sleep
        await asyncio.sleep (1)
  
    except asyncio.CancelledError:
      logger.info ("%s Heartbeat - Received cancelation request" % self.name)
      # Clean up things here
      logger.info ("%s Heartbeat - Task terminated gracefully." % self.name)


################################################################################
#                                                                              #
#                                 M A I N                                      #
#                                                                              #
################################################################################

if __name__ == "__main__":
  
  # ------------------------------------------------------------------ Constants
  
  HOSTNAME = '127.0.0.1'
  TESTNAME = 'Test Name'
  
  
  #------------------------------------------------------------- Initializations
  
  # ---- Startup text
  
  print ()
  print ("%s - %s" % (__appname__, __description__))
  print ("%s" % (__copyright__))
  print ("Version %s (%s)" % (__version__, __versiondate__))
  print ()
  
  # ---- Logger
  
  logger = CreateLogger (__appname__)
  logger.info ('------')
  logger.info ('%s program starting. Use Ctrl+C or send signal to stop.' % (__appname__))
  
  
  # ---- Get current event loop or create a new one
  
  loop = asyncio.get_event_loop ()
  # loop = asyncio.new_event_loop ()
  
  
  # ---- Instantiate AsyncIO classes
  
  logger.info ('Initializing test class...')
  Test = cTestClass (loop, 'TESTNAME')

  
  # ------------------------------------------------------- Main asynchronous loop
  
  # ---- Set shutdown signals
  
  SetShutdownSignals (loop, logger)

  # ---- Start AsyncIO instances tasks
  
  logger.info ('------')
  logger.info ("Starting asynchronous tasks...")

  Test.Start ()
  
  # ---- Start main loop
  
  try:
    # loop.set_debug(True)                        # Useful for deep AsyncIO debugging
    loop.run_forever ()
  
  # Exceptions
  
  except KeyboardInterrupt:  # Windows only; on Linux, shutdown is managed by signals
    logger.info ('------')
    logger.info ('CTRL+C : Keyboard Interrupt')
    logger.info ('Shutting down pending tasks...')
    loop.run_until_complete (AsyncIOShutdown (loop, logger))
  
  except:
    logger.info ('------')
    logger.info ("UNHANDLED EXCEPTION :")
    logger.info ('Shutting down pending tasks...')
    loop.run_until_complete (AsyncIOShutdown (loop, logger))
    raise
  
  finally:
    logger.info ('Closing AsyncIO loop...')
    loop.close ()
    logger.info ('Terminated.')





