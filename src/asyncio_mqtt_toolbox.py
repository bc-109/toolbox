#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# ===============================================================================
# Python3 Toolbox
# (c) 2011-2022 by Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr
# ===============================================================================
#
# MQTT AsyncIO library :
#   Allows MQTT operations with AsyncIO
#   using gmqtt library (https://github.com/wialon/gmqtt)
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

Name = "AsyncIO MQTT toolbox"
Version = "0.1"
VersionDate = "30/12/2022"

# ===============================================================================
# Imports
# ===============================================================================

# ---- Python standard imports

import asyncio


# ---- Third-party module imports (install with pip)

import gmqtt


###############################################################################
#                                                                             #
#                                MQTT CLASS                                   #
#                                                                             #
###############################################################################

# ==============================================================================
# Main MQTT client class using gmqtt
# ==============================================================================

# KNOWN PROBLEMS :
#
#  - GMQTT methods such as 'connect' run on the default running loop.
#    I didn't find how to specify the event loop to use.
#    If you created your own event loop, 'connect' does crash because
#    it awaits on a different loop !
#      -> Initialize your loop with get_event_loop() and not new_event_loop()
#
#  - If connection is closed by peer, we receive the callback "OnDisconnect",
#    but GMQTT still tries to write on socket, and generates
#    [TRYING WRITE TO CLOSED SOCKET]
#

class cGMQTTClient ():
  
  # ---------------------------------------------------------------- Constructor
  
  def __init__ (self, loop, logger, hostname='127.0.0.1', client_id="default-mqtt-client"):
    
    self.loop = loop
    self.logger = logger
    self.hostname = hostname               # MQTT broker hostname or IP
    self.client_id = client_id             # used both as instance name and MQTT client_id
    self.port = 1883
    
    self.connected = 'DISCONNECTED'        # DISCONNECTED, CONNECTING, CONNECTED, FAILED
    self.canceled = False
    
    self.logger.info ("MQTT initializing client %s " % (self.client_id))
    self.client = gmqtt.Client (self.client_id)
    if self.client is None:
      self.logger.info ("  Error initializing client %s " % (self.client_id))
    else:
      self.client.set_config ({'reconnect_retries': 0, 'reconnect_delay': 0})    # does not seem to work
      self.client.on_connect = self.OnConnect
      self.client.on_message = self.OnMessage
      self.client.on_disconnect = self.OnDisconnect
      self.client.on_subscribe = self.OnSubscribe
  
  
  # ------------------------------------------- Start MQTT session to the broker
  
  def Start (self):
    
    self.logger.info ("%s MQTT starting session to %s:%s " % (self.client_id, self.hostname, self.port))
    self.loop.create_task (self.MainLoop (), name = "%s MainLoop" % self.client_id)
  
  
  # ----------------------------------------------- Main asynchronous process
  
  async def MainLoop (self):

    self.connected = 'CONNECTING'
    while not self.canceled:
      
      try:

        # ---- Start / Try to connect to server
        
        if (self.connected == 'FAILED') or (self.connected == "DISCONNECTED"):
          self.logger.info ("%s Main Loop - Previous MQTT connection failed. Will retry in 5s..." % self.client_id)
          await asyncio.sleep(5)
          
        self.logger.info ("%s Main Loop - MQTT connecting to broker..." % self.client_id)
        await self.client.connect (self.hostname)
        self.logger.info ("%s Main Loop - MQTT connected to broker." % self.client_id)
    
        while self.connected == 'CONNECTED' :
          # We are connected / nothing to do here.
          print("...connected")
          await asyncio.sleep(1)
        
      
      # ---- Task canceled (receiving Ctrl+C or termination signal)
      
      except asyncio.CancelledError:
        self.logger.info ("%s Main Loop - Received STOP request" % self.client_id)
        
        # Clean up things here
        
        if self.connected == 'CONNECTED':
          self.logger.info ("%s Main Loop - Disconnecting from MQTT broker..." % self.client_id)
          await self.client.disconnect ()
          self.logger.info ("%s Main Loop - MQTT broker disconnected." % self.client_id)
  
        self.logger.info ("%s Main Loop - Task stopped gracefully." % self.client_id)
        self.canceled = True
  
      # ---- Communication errors
      
      except ConnectionRefusedError :
        self.logger.info ("%s Main Loop - Connection refused." % self.client_id)
        self.connected = 'FAILED'
        
      except TimeoutError :
        self.logger.info ("%s Main Loop - Connection timeout." % self.client_id)
        self.connected = 'FAILED'
  
      # ---- Unhandled exception
      
      except:
        self.logger.info ("%s Main Loop - Unhandled exception." % self.client_id)
        self.connected = 'FAILED'
        raise



  # ------------------------------------------------ On successful connection
  
  def OnConnect (self, client, flags, rc, properties):
    self.logger.info ('%s > MQTT Callback : client connected to broker.' % self.client_id)
    self.connected = 'CONNECTED'
    # client.subscribe ('TEST/#', qos=0)


  # ----------------------------------------------------------- On Disconnect

  def OnDisconnect (self, client, packet, exc=None):
    self.logger.info ('%s > MQTT Callback : disconnected from broker.' % self.client_id)
    self.connected = 'DISCONNECTED'


  # ----------------------------------------------------- On received message
  
  def OnMessage (self, client, topic, payload, qos, properties):
    self.logger.info ('%s > MQTT Callback : received message [%s] %s:', self.client_id, topic, payload)
  
  
  
  # --------------------------------------------------------- On Subscription
  
  def OnSubscribe (self, client, mid, qos, properties):
    print ('%s MQTT Subscribed' % self.client_id)
  


################################################################################
#                                                                              #
#                                 M A I N                                      #
#                                                                              #
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr" % (Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")