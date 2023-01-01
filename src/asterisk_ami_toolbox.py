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
  
  def __init__ (self, loop, logger, taskname, host, port, username, secret):
    
    self.loop = loop
    self.logger = logger
    self.taskname = taskname              # Namre of the task in AsyncIO
    self.host = host                      # MQTT broker
    self.port = port
    self.username = username
    self.secret = secret
    
    self.callback = self.Callback
    
    self.connected = 'DISCONNECTED'        # DISCONNECTED, CONNECTING, LOGGING, CONNECTED, FAILED
    self.canceled = False
    
    self.manager = panoramisk.Manager (host=self.host,
                                       port=self.port,
                                       username=self.username,
                                       secret=self.secret,
                                       ping_delay=10,  # Delay after startup
                                       ping_interval=10,  # Periodically ping AMI
                                       reconnect_timeout=2)  # Timeout reconnect if connection lost
    if self.manager is None:
      self.logger.info ("Error initializing Panoramisk manager %s " % (self.taskname))
    else:
      self.manager.on_connect = self.OnConnect
      self.manager.on_login = self.OnLogin
      self.manager.on_disconnect = self.OnDisconnect
  
  
  #---------------------------------------- Schedule start of Asterisk main loop

  def Start(self):
    self.logger.info ("%s Starting main asynchronous loop..." % self.taskname)
    self.loop.create_task (self.MainLoop (), name="%s MainLoop" % self.taskname)
  
  
  #------------------------------------------ Asterisk AMI TCP session main loop
  
  
  # OLD MainLoop
  #  self.manager.connect (run_forever=True, on_startup=self.OnStartup, on_shutdown=self.OnShutdown)

  async def MainLoop (self):
  
    self.connected = 'NONE'
    while not self.canceled:
    
      try:
      
        # ---- Start / Try to connect to server
      
        if (self.connected == 'FAILED') or (self.connected == "DISCONNECTED"):
          self.logger.info ("%s (Main Loop) Previous Asterisk connection failed. Will retry in 5s..." % self.taskname)
          await asyncio.sleep (5)
      
        self.logger.info ("%s (Main Loop) Connecting to Asterisk at %s:%s..." % (self.taskname, self.host, self.port))
        await self.manager.connect (run_forever=False, on_startup=self.OnStartup, on_shutdown=self.OnShutdown)
        self.connected = 'CONNECTING'
        
        while self.connected != 'READY':
          # print ("...Waiting for connection and login")
          await asyncio.sleep (1)

        self.logger.info ("%s (Main Loop) Registering Asterisk events..." % self.taskname)
        self.manager.register_event ('*', callback=self.callback)
        
        while self.connected == 'READY':
          # We are connected and logged in
          # print ("...Asterisk normal loop - READY")
          await asyncio.sleep (1)
    
    
      # ---- Task canceled (receiving Ctrl+C or termination signal)
    
      except asyncio.CancelledError:
        self.logger.info ("%s (Main Loop) Received STOP request" % self.taskname)
        # Clean up things here
      
        if self.connected in ('CONNECTED', 'LOGGING', 'READY'):
          self.logger.info ("%s (Main Loop) Disconnecting from Asterisk..." % self.taskname)
          await self.manager.close ()
          self.logger.info ("%s (Main Loop) Asterisk disconnected." % self.taskname)
      
        self.logger.info ("%s (Main Loop) Task stopped gracefully." % self.taskname)
        self.canceled = True
    
      # ---- Communication errors
    
      except ConnectionRefusedError:
        self.logger.info ("%s (Main Loop) Connection refused." % self.taskname)
        self.connected = 'FAILED'
    
      except TimeoutError:
        self.logger.info ("%s (Main Loop) Connection timeout." % self.taskname)
        self.connected = 'FAILED'
    
      # ---- Unhandled exception
    
      except:
        self.logger.info ("%s (Main Loop) Unhandled exception." % self.taskname)
        self.connected = 'FAILED'
        raise


  # ----------------------------------------------------------------- On Connect
  
  def OnConnect (self, mngr: panoramisk.Manager):
    self.logger.info ('%s > Connected to AMI socket. Trying to login with [%s]...' % (self.taskname, self.username))
    self.connected = 'LOGGING'
    
  
  # ------------------------------------------------------------------- On Login
  
  def OnLogin (self, mngr: panoramisk.Manager):
    self.logger.info ('%s > User [%s] logged in to AMI. Ready.' % (self.taskname, mngr.config ['username']))
    self.connected = 'READY'
  
  
  # -------------------------------------------------------------- On Disconnect
  
  def OnDisconnect (self, mngr: panoramisk.Manager, exc: Exception):
    self.logger.info ('%s > User [%s] disconnected from AMI.' % (self.taskname, mngr.config ['username']))
    # self.logger.debug (str (exc))
    self.connected = 'DISCONNECTED'
    
    
  # ----------------------------------------------------------------- On Startup
  
  async def OnStartup (self, mngr: panoramisk.Manager):
    self.logger.info ('%s > Asterisk AMI startup complete.' % self.taskname)

  
  # ---------------------------------------------------------------- On Shutdown
  async def OnShutdown (self, mngr: panoramisk.Manager):
    self.logger.info ('%s > Shutdown AMI connection.' % (self.taskname))
  
  
  # --------------------------------------------------- Send command to Asterisk
  
  async def SendCommand (self, command):
    
    self.logger.info  ("Sending command : [%s]" % (command))
    answer = await self.manager.send_command (command)
    self.logger.info  ("Command sent. Received answer : [%s]" % (answer))


  # ------------------------------------------------ Callback when data received
  # (Override with your own method)
  # Default just prints all Asterisk messages to the console
  
  async def Callback (self, mngr: panoramisk.Manager, msg: panoramisk.Message):
    
    try:
      if msg is not None:
        event = msg.Event
        self.logger.info  ("[%s] %s" %(event, msg))
    
    except:
      self.logger.info  ("Callback - Exception processing message")


################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              #
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr" % (Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")