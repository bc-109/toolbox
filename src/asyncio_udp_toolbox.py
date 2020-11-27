#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#===============================================================================
# Python3 Toolbox
# (c) 2011-2020 by Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr
#===============================================================================
#
# AsyncIO UDP client and server
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

Name = "Python Toolbox - AsyncIO UDP client and server library"
Version = "0.1"
VersionDate = "09/11/2020"


#===============================================================================
# Imports 
#===============================================================================

# standard Python imports

import asyncio


# Toolbox library imports (get those files and put them in the same folder as your app)

# from network_toolbox import CheckUpdateHost
from string_toolbox import DumpBufferHexa


################################################################################
#                                                                              #
#                             ASYNCIO UDP CLIENT                               #
#                                                                              # 
################################################################################



#===============================================================================
# UDP Client class - Simple UDP client, connects to an UDP "server"
#===============================================================================

class cUDPClient (asyncio.DatagramProtocol):
 
  
  #----------------------------------------------------------------- Constructor
  
  def __init__(self, _name, _server, _port, _loop, _logger):                       
   
    # ip addresses and sockets
    self.taskname = _name
    self.server_address = _server                                            # Can be IP or FQDN
    self.server_ip = _server   # Not working, netifaces does not install under Windows  CheckUpdateHost (self.server_address, self._logger)     # Is always IP. 0.0.0.0 if DNS resolution failed.
    self.server_port = _port
       
    self.loop = _loop                # AsyncIO loop object 
    self.logger = _logger            # Logger object
    self.debug =  True               # Global flag for more verbose output   
    
    
  #-------------------------------------------------------------- When connected
  
  def connection_made(self, transport):
    self.logger.info('UDP connection made')
    self.transport = transport
    # self._system_maintenance = self._loop.create_task(self.maintenance_loop())     # (No maintenance loop in the basic client)


  #------------------------------------------------- Datagram received by client 

  def datagram_received(self, _data, _sockaddr):
    
    if self.debug :
      self.logger.debug('RX packet from %s (length : %d bytes)\n%s\n----', _sockaddr, len(_data), DumpBufferHexa(_data))

    # Validate that we receveived this packet from the right master - security check !
    if _sockaddr != (self.server_ip, self.server_port):
      self.logger.warning ('Unexpected RX packet from %s:%s' % (_sockaddr))
      
    else : 
      
      # Process _data here
      print('rx')
      pass
    
 
#---------------------------------------------------------- Send packet to server
    
  def send_server(self, _packet):

    # if True : # self.debug:  
      # self.logger.debug('TX Packet to %s:%s (length : %d bytes)\n%s\n----',self.server_ip, self.server_port, len(_packet), DumpBufferHexa(_packet))
      # print('TX Packet to %s:%s (length : %d bytes)\n%s\n----',self.server_ip, self.server_port, len(_packet), DumpBufferHexa(_packet))
         
    try:   
      print ("Send_Server")  
      self.transport.sendto(_packet, (self.server_ip, self.server_port))
    except:
      print('EXCEPTION sending UDP packet')   




################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              # 
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr" %(Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")