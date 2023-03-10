#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#===============================================================================
# Python3 Toolbox
# (c) 2011-2020 by Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr
#===============================================================================
#
# AsyncIO TCP client and server 
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

Name = "Python Toolbox - AsyncIO TCP client and server library"
Version = "0.1"
VersionDate = "23/05/2020"


#===============================================================================
# Imports 
#===============================================================================

import asyncio


################################################################################
#                                                                              #
#                            ASYNCIO TCP SERVER                                #
#                                                                              # 
################################################################################

#===============================================================================
# Main TCP Server class
# (one instance = one server that can accept multiple connections)
#===============================================================================

class cTCPServer():

  #----------------------------------------------------------------- Constructor
  
  def __init__(self, loop, name, local_address, local_port):  
  
    self.loop = loop                                  # AsyncIO running loop
    self.server_name = name
    self.tcp_local_address = local_address            # TCP server will bind to that IP
    self.tcp_local_port = local_port                  # TCP server will listen on that port
    self.clients = cTCPConnectedClients()             # List of clients connected to this server

  

  #---------------------------------------------------------------- Start Server
  
  def start_server(self, name=None):
    if name==None:
      name="TCP server at %s:%d" %(self.tcp_local_address, self.tcp_local_port)
    self.loop.create_task(self.serve(), name=name)


  #---------------------------------------------------------------- Stop Server
  
  async def stop_server (self):
    print ('%s : Closing transport for all connected clients...' % self.server_name)
    self.clients.DisconnectAll()
    
    print ('%s : Closing server task...' % self.server_name)
    self.server.close()
    await self.server.wait_closed()        

  
  #-------------------------------------------------------- Create AsyncIO server
  # If you derive cTCPServer, you'll have to override this one with your own 
  # derived cTCPServerProtocol 
  
  async def create_server(self):
    self.server = await self.loop.create_server( lambda: cTCPServerProtocol(parent=self), self.tcp_local_address, self.tcp_local_port)


  #--------------------------------------------------- Starting / stopping server
  
  async def serve(self):

    # Starting TCP server
     
    self.canceled = False
    self.started = False
    while not self.started:

      try:    
        print ("%s : Starting TCP server at %s:%d " % (self.server_name, self.tcp_local_address, self.tcp_local_port) )
        await self.create_server()
              
        print ("%s : TCP server started on port %d " % (self.server_name, self.tcp_local_port) )  
        self.started = True
    
      except OSError : 
        print("%s : Unable to start server on port %d; port may be already in use." % (self.server_name, self.tcp_local_port))
                            
      except:
        print("%s : Unhandled exception when starting TCP server. " % self.server_name)
        raise          
    
      if self.started : break
         
      print("%s : Retrying in 10 seconds..." % self.server_name)
      await asyncio.sleep(10) 
          
    
    # Main server loop
    
    try:
      await self.server.start_serving()
      while not self.canceled:
        await asyncio.sleep(1)
              
    except asyncio.CancelledError : 
      print("%s : Server canceled." % self.taskname)
      self.canceled = True
                                               
    except:
      print("%s : Unhandled exception when serving. " % self.server_name)
      raise

    finally:
      print ("%s : Stopping TCP server..." % self.server_name)
      await (self.stop_server())       
      print ("%s : TCP Server stopped." % self.server_name)


#===============================================================================
# Main TCP Server Protocol class. 
# (A new instance is created for every incoming connection)
#===============================================================================

class cTCPServerProtocol(asyncio.Protocol):

  #----------------------------------------------------------------- Constructor
          
  def __init__(self, parent):    
    self.parent = parent                           # Parent cTCPServer object                             
    self.server_name = self.parent.server_name
    self.client_name = '<No client details available>'
    self.transport = None
 
  #---------------------------------------------------------- Display procedures
  
  def __str__(self):
    return self.client_name
  
  def __repr__(self):
    return self.client_name
      

  #------------------------------------------------------------- Connection Made
  
  def connection_made(self, transport):
    
    self.transport = transport
    peername = transport.get_extra_info('peername')                           # peername is a tuple
    print('%s : Incoming connection from %s' % (self.server_name, peername))
    # print ('Self is :')
    # print (self)
    
    try:
      ip,port = peername
    except:
      ip = '0.0.0.0'
      port = 0
    self.client_ip = ip
    self.client_port = port  
          
    # Add to the list of the connected clients      
    already_client = self.parent.clients.IsMember(ip, port)
    if already_client is None:
      print ('%s : Connection accepted from %s:%s' %(self.server_name, ip, port))
      self.parent.clients.AddMember (ip, port, self)   
    else: 
      print ("ERROR - Incoming connection from an already connected client") 
      # TODO : reuse existing connexion / replace transport (or delete / add)
    
    # Debug : print list of connected clients  
    print ("%s : %s" % (self.server_name, self.parent.clients))  



  #---------------------------------------------- Callback when data is received

  def data_received(self, data):

    # print('%f : Data received from %s' % (self.taskname, self.peername)) 
    
    # decoded = data.decode()
    # print(decoded)
    
    # text = DumpBufferHexa (data)
    # print(text)

    # Do something with received data
    
    print ("%s : Data received from client :" % (self.server_name)) 
    # print (self)
    # print (data)
    
  
  #-------------------------------------------- Callback when connection is lost
  
  def connection_lost(self, exc):        # exc is an exception; can be none
    
    # Check / remove from the list of connected clients    
    print('%s : Client %s:%d disconnected' % (self.server_name, self.client_ip, self.client_port))
    self.parent.clients.RemoveMember (self.client_ip, self.client_port)   
  
    # Debug : print list of connected clients
    # print ("%s : %s" % (self.server_name, self.parent.clients))  
    

  #--------------------------------------------------------- Send data to client

  def send_data(self, data):
    # print('%f : Sending data to %s' % (self.taskname, self.peername)) 
    self.transport.write(data)    
    


#===============================================================================
# Class representing the list of all TCP clients connected to a server 
#===============================================================================

# Connected clients are stored in a dict :
#  Key is a tuple (source_ip, source_port)
#  Data is cTCPserverProtocol object          
                                                   
class cTCPConnectedClients(object):
   
  #----------------------------------------------------------------- Constructor
  
  def __init__(self):   
    self.clients = {}                            # Dict of the connected clients
                                                                                        

  #---------------------------------------- Get dictionnary of connected clients
  
  def Get(self):
    return self.clients
  

  #---------------------------------------------------------- Display procedures
  
  def __str__(self):
    return self.Display()
 
  def __repr__(self):
    return self.Display()

  def Display(self):
    d = "Currently connected clients : \n"
    if self.clients == {}:
      d = d + "  <Empty>\n"
    else:
      for c in self.clients:
        d = d + "  %s\n" % (self.clients[c])
    return d 


  #--------------------------------- Is (ip,port) already a connected client ? 

  def IsMember (self, ip, port) :

    key = '%s:%d' % (ip, port)
    if key in self.clients :               # Is it a member of the list?            
      result  = self.clients[key]          # Get the object
    else:
      result = None
      
    return result
        

  #----------------------------- Add a client to the list of connected clients
  
  def AddMember (self, ip, port, client_protocol ):
    
    key = '%s:%d' % (ip, port)
    client = cTCPConnectedClient (client_protocol, ip, port)    # Instantiate new client tracking object
    self.clients[key] = client                                  # Create it in the clients list         

    return client


  #------------------------------------------------ Remove a client from list
   
  def RemoveMember (self, ip, port):
 
    to_remove = self.IsMember (ip, port)
    if to_remove is not None:
      key = '%s:%d' % (ip, port)
      del self.clients[key]

  #------------------------------------------------------ Disconnect all clients
  
  def DisconnectAll (self):
    print("Disconnecting all connected  clients :")
    if self.clients == {}:
      print("  <No client connected")
    else:
      for c in self.clients:
        print ("  %s" % (self.clients[c]))
        self.clients[c].transport.close()
               
    

#===============================================================================
# Class representing one of the TCP connected clients
#===============================================================================

class cTCPConnectedClient(object):
        
  #----------------------------------------------------------------- Constructor
  
  def __init__(self, client_protocol, client_ip, client_port):
    self.protocol = client_protocol
    self.transport = self.protocol.transport
    self.ip = client_ip
    self.port = client_port


  #---------------------------------------------------------- Display procedures

  def __str__(self):
    return self.Display()
 
  def __repr__(self):
    return self.Display()
  
  def Display(self):
    try:
      # s = "  %s:%d" % (self.ip, self.port)
      s = "  %s:%d %s" % (self.ip, self.port, self.protocol)
    except:
      s = "<Display error>"
    return s
    

################################################################################
#                                                                              #
#                          ASYNCIO TCP CLIENT                                  #
#                                                                              # 
################################################################################  

#===============================================================================
# TCP Client class
# (Connects to a TCP server)
#===============================================================================

class cTCPClient():

  #----------------------------------------------------------------- Constructor
  
  def __init__(self, loop, name, tcp_address, tcp_port, source_address='', source_port=0):
    
    self.loop = loop
    self.taskname = name
    self.tcp_address = tcp_address
    self.tcp_port = tcp_port
    
    self.tcp_source_address = source_address         
    self.tcp_source_port = source_port               
    self.tcp_source_port_origin = source_port 
    self.local_addr = (source_address, source_port)  # Tuple required by loop.create_connection()

    self.PORT_RETRIES = 128          # Max attempts of source_port increment in case of previous socket locked in MAX_RETRY
  
  
  #-------------------------------------------------------- Create AsyncIO task
  # If you derive cTCPClient, you'll have to override this one with your own 
  # derived cTCPServerProtocol 
  
  async def create_connection(self):
    #loop = asyncio.get_running_loop()
    print ("%s : TCP Client - Creating connection to %s:%d from %s:%d" %(self.taskname, self.tcp_address, self.tcp_port, self.tcp_source_address, self.tcp_source_port))
    self.transport, self.protocol = await self.loop.create_connection( lambda: cTCPClientProtocol(parent=self), self.tcp_address, self.tcp_port, local_addr=self.local_addr)


  #------------------------------------------------------ Schedule AsyncIO task
  
  def start_client (self, name=None):
    if name==None:
      name="TCP connection to %s:%d" %(self.tcp_address, self.tcp_port)
    self.loop.create_task(self.connect(), name=name)
    
    
  #------------------------------------------------------- Connection management
  
  async def connect (self):
   
    # Try to connect to TCP server
  
    self.connected = False
    self.canceled = False
    while not (self.canceled):
      
      try:
        print ("%s : TCP Client - Connecting to %s:%d... " % (self.taskname, self.tcp_address, self.tcp_port) )
        await self.create_connection()
        self.connected = True
        
      except ConnectionRefusedError:
        print("%s : TCP client - Connection refused." % self.taskname)
        
      except asyncio.CancelledError : 
        print("%s : TCP Client - Connection canceled - Stopping." % self.taskname)
        self.canceled = True
        self.connected = False
          
      except TimeoutError :
        print("%s : TCP Client - Unable to connect to %s : Timeout." % (self.taskname, self.tcp_address))
           
      except OSError :
        print("%s : TCP Client - OS error (possibly wrong source IP or source port)." % (self.taskname))
        self.connected = False 
        self.PORT_RETRIES = self.PORT_RETRIES - 1
        if self.PORT_RETRIES > 0:
          self.tcp_source_port = self.tcp_source_port + 1   
          print("%s : TCP Client - Incrementing source port. Will retry from %s:%d)." % (self.taskname, self.tcp_source_address, self.tcp_source_port))  
        else:
          self.tcp_source_port = self.tcp_source_port_origin              
          print("%s : TCP Client - Reverting back to original source port. Will retry from %s:%d)." % (self.taskname, self.tcp_source_address, self.tcp_source_port))  
        self.local_addr = (self.tcp_source_address, self.tcp_source_port)
      
      except:
        print("%s : TCP Client - Unknown exception. " % self.taskname)
        raise

             
      if self.connected :        
        
        # We are connected. We do nothing here. Just wait for callbacks or external signals
        
        try:
          print ("%s : TCP Client - Connected, entering reception loop" % self.taskname)
          while self.connected:
            await asyncio.sleep(1)
            # print('Connected : %s' % (self.connected))
        
        except asyncio.CancelledError : 
          print("%s : TCP Client - Task canceled"  % self.taskname)
          self.canceled = True
                
        except asyncio.TimeoutError :
          print("%s : TCP Client - Timeout" % self.taskname)    
          self.connected = False
          
        except asyncio.InvalidStateError:
          print("%s : TCP Client - Invalid State"  % self.taskname)
          self.canceled = True
          
        except:
          print ("%s : TCP Client - Unknown exception" % self.taskname)
          raise
              
              
      if not self.canceled  :      
         
        # Connection was lost, but not canceled. We'll retry later.
            
        print ("%s : TCP Client - Retry in 1 second" % self.taskname)
        try :
          await asyncio.sleep(1)                     
        except asyncio.CancelledError : 
          print("%s : TCP Client - Retry canceled." % self.taskname)
          self.canceled = True
    
    # end while
    
    print ("%s : TCP Client - Closing transport." % self.taskname)
    self.transport.close()  
  

#===============================================================================
# TCP Client Protocol class
#===============================================================================

class cTCPClientProtocol(asyncio.Protocol):

  
  #----------------------------------------------------------------- Constructor
  
  def __init__(self, parent):
    self.parent = parent
    self.taskname = parent.taskname
    self.tcp_address = parent.tcp_address
    self.tcp_port = parent.tcp_port
    self.transport = None


  #------------------------------------------------------------- Connection Made
  
  def connection_made(self, transport):
    self.transport = transport
    # transport.write(self.message.encode())
    # print('Data sent: {!r}'.format(self.message))


  #---------------------------------------------- Callback when data is received
  
  def data_received(self, data):
    
    print('%s : Data received:' % self.taskname) 
    
    # print (data.decode())  
    # print (DumpBufferHexa (data))

    self.buffer = self.buffer + data       # Incomplete message may be in the buffer from previous call; just add to it
      
    # Do what you want with self.buffer
    pass
      
    
  #-------------------------------------------- Callback when connection is lost
  
  def connection_lost(self, exc):
    print('%s : The server closed the connection' % self.taskname)
    self.parent.connected = False 
    

################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              # 
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr" %(Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")