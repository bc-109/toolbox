# !/usr/bin/python3
# -*- coding: UTF-8 -*-

# ===============================================================================
# Python3 Toolbox
# (c) 2011-2022 by Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr
# ===============================================================================
#
# Asterisk AMI interface :
#   Allows to talk with Asterisk via Asterisk Management Interface
#   using Panoramisk library (https://github.com/gawel/panoramisk)
#
# ===============================================================================

# ===============================================================================
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
# ===============================================================================

Name = "Asterisk AMI interface"
Version = "0.1"
VersionDate = "30/12/2022"


# ===============================================================================
# Imports
# ===============================================================================

# ---- Python standard imports

import asyncio
import logging


# ---- Third-party module imports (install with pip)

import panoramisk


###############################################################################
#                                                                             #
#                          ASTERISK AMI INTERFACE                             #
#                                                                             #
###############################################################################

# ==============================================================================
# Main Panoramisk class
# ==============================================================================

class cPanoramiskManager ():
  
  # ---------------------------------------------------------------- Constructor
  
  def __init__ (self, host, port, username, secret):
    
    self.host = host
    self.port = port
    self.username = username
    self.secret = secret
    
    self.callback = self.Callback
    
    self.manager = panoramisk.Manager (host=self.host,
                                       port=self.port,
                                       username=self.username,
                                       secret=self.secret,
                                       ping_delay=10,  # Delay after startup
                                       ping_interval=10,  # Periodically ping AMI
                                       reconnect_timeout=2)  # Timeout reconnect if connection lost
  
  
  # ------------------------------------- Start Asterisk AMI AsyncIO TCP session
  
  def Start (self):
    
    self.manager.on_connect = self.OnConnect
    self.manager.on_login = self.OnLogin
    self.manager.on_disconnect = self.OnDisconnect
    
    logging.info ("Starting Asterisk Manager Interface AsyncIO task")
    self.manager.connect (run_forever=True, on_startup=self.OnStartup, on_shutdown=self.OnShutdown)
  
  
  # ----------------------------------------------------------------- On Connect
  
  def OnConnect (self, mngr: panoramisk.Manager):
    logging.info ('Connected to %s:%s AMI socket successfully' % (mngr.config ['host'], mngr.config ['port']))
  
  
  # ------------------------------------------------------------------- On Login
  
  def OnLogin (self, mngr: panoramisk.Manager):
    logging.info ('Connected user:%s to AMI %s:%s successfully' % (
    mngr.config ['username'], mngr.config ['host'], mngr.config ['port']))
  
  
  # -------------------------------------------------------------- On Disconnect
  
  def OnDisconnect (self, mngr: panoramisk.Manager, exc: Exception):
    logging.info (
      'Disconnect user:%s from AMI %s:%s' % (mngr.config ['username'], mngr.config ['host'], mngr.config ['port']))
    logging.debug (str (exc))
    
    
  # ----------------------------------------------------------------- On Startup
  
  async def OnStartup (self, mngr: panoramisk.Manager):
    await asyncio.sleep (0.1)
    logging.info ('Asterisk AMI session started. Registering all events...')
    self.manager.register_event ('*', callback=self.callback)
  
  
  # ---------------------------------------------------------------- On Shutdown
  async def OnShutdown (self, mngr: panoramisk.Manager):
    await asyncio.sleep (0.1)
    logging.info ('Shutdown AMI connection on %s:%s' % (mngr.config ['host'], mngr.config ['port']))
  
  
  # --------------------------------------------------- Send command to Asterisk
  
  async def SendCommand (self, command):
    
    logging.info  ("Sending command : [%s]" % (command))
    answer = await self.manager.send_command (command)
    
    logging.info  ("Command sent. Received answer : [%s]" % (answer))


  # ------------------------------------------------ Callback when data received
  # (Override with your own method)
  # Default just prints all Asterisk messages to the console
  
  async def Callback (self, mngr: panoramisk.Manager, msg: panoramisk.Message):
    
    try:
      if msg is not None:
      
        event = msg.Event
        logging.info  ("[%s] %s" %(event, msg))
    
    except:
      logging.info  ("Exception processing message")


################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              #
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr" % (Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")