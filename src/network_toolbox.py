#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#===============================================================================
# Python3 Toolbox
# (c) 2011-2020 by Toussaint OTTAVI, t.ottavi@medi.fr
#===============================================================================
#
# General-purpose networking functions.
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

Name = "Python Toolbox - Networking library"
Version = "0.5"
VersionDate = "23/05/2020"

#===============================================================================
# Imports 
#===============================================================================

from netifaces import interfaces, ifaddresses, AF_INET

import socket


################################################################################
#                                                                              #
#                                 IPv4                                         #
#                                                                              #
################################################################################   


#===============================================================================
# Get the current host name
#===============================================================================

def GetHostName():
  return socket.gethostname()


#===============================================================================
# Get the default local IP address (old method) (only address)
#===============================================================================
 
def GetDefaultIPAddressOld():
  try:
    address = socket.gethostbyname_ex(socket.gethostname())[2][0]
  except:
    address = "127.0.0.1"
  return address  


#===============================================================================
# Get the default local IP address (with netiface) 
# Result is a tuple (address, netmask, broadcast)  
#===============================================================================
 
def GetDefaultIPAddress():
  try:
    addresses = GetIPInterfaceList()
    for i in addresses:
      (addr, mask, broadcast) = i    
      if addr<>"127.0.0.1":
        address = i
        break
  except:
    address = ("127.0.0.1", "255.0.0.0", "127.0.0.1")
  return address  


#===============================================================================
# Obtain a list of all ip address of all interfaces via netifaces library
# Each interface is a tuple (ip, netmask, broadcast)
#===============================================================================

def GetIPInterfaceList():
  ip_list = []
  for interface in interfaces():                                            # need to import netifaces
    try:
      for link in ifaddresses(interface)[AF_INET]:
        ad = link['addr']
        nm = link['netmask']
        br = "127.0.0.1" if interface == "lo" else link['broadcast']        # netifaces does not return "broadcast" for loopback, we "simulate" it
        ip_list.append((ad, nm, br))
    except:
      print "libnetwork: Unable to get parameters of interface %s :" % (interface)

  return ip_list


#===============================================================================
# Find a free local port, starting from start_port
#===============================================================================

def FindFreeLocalPort(interface='127.0.0.1', start=50000, max_ports=512 ):

  UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  
  for port in range(start, start + max_ports):
    try:
      addr = (interface, port)
      UDPSock.bind(addr)
      break
    except:
      port = port + 1
  
  UDPSock.close()
  return port


#===============================================================================
# A TRIER 
#===============================================================================

# 
# def netmask_valid(netmask):
#     elems = netmask.split('.')
#     if len(elems) != 4:
#         return False
# 
#     mask = 0
#     for i in range(4):
#         mask |= (int(elems[i]) << ((3 - i) * 8))
# 
#     neg = ~mask & 0xFFFFFFFF
# 
#     return (((neg + 1) & neg) == 0)
# 
# 
# def ip_to_int(ip):
#     elems = ip.split('.')
# 
#     num = 0
#     for i in range(4):
#         num |= (int(elems[i]) << ((3 - i) * 8))
# 
#     return num
# 
# 
# def int_to_ip(num):
#     ip = []
#     for i in range(4):
#         ip.append(str((num >> ((3 - i) * 8)) & 255))
# 
#     return '.'.join(ip)
# 
# 
# def find_broadcast(ip, netmask):
#     i = ip_to_int(str(ip))
#     n = ip_to_int(str(netmask))
# 
#     return int_to_ip((n & i) | ~n)
# 
# 
# def guess_broadcast(ip):
#     elems = ip.split('.')
# 
#     if ip == '0.0.0.0':
#         return '255.255.255.255'
#     elif int(elems[0]) == 10:
#         return '10.255.255.255'
#     elif int(elems[0]) == 192 and int(elems[1]) == 168:
#         return '192.168.%s.255' % elems[2]
#     elif int(elems[0]) == 172 and int(elems[1]) == 16:
#         return '172.31.255.255'
#     elif int(elems[0]) == 169 and int(elems[1]) == 254:
#         return '169.254.255.255'
#     else:
#         return find_broadcast(ip, '255.255.255.0')
# 
# 
# def format_ip_address(address):
#     return ''.join(map(lambda n: "%03d" % int(n), address.split('.')))
# 




################################################################################
#                                                                              #
#                              M A I N                                         #
#                                                                              # 
################################################################################

if __name__ == "__main__":
  print ("%s - (c) Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr" %(Name))
  print ("Version %s, date : %s" % (Version, VersionDate))
  print ("This is a library, to be called from other modules. It does nothing by itself.")