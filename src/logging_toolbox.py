#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#===============================================================================
# Python3 Toolbox
# (c) 2011-2022 by Toussaint OTTAVI, bc-109 Soft, t.ottavi@medi.fr
#===============================================================================
#
#
#    This is a simple logger for other Dragon modules.
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

__appname__     = "logging_toolbox"
__description__ = "General-purpose logging methods to be used in other projects"
__author__      = 'Toussaint OTTAVI, TK1BI, bc-109 Soft'
__copyright__   = '(c) 2019 by Toussaint OTTAVI, TK1BI, bc-109 Soft'
__credits__     = ''
__license__     = 'GNU GPLv3'
__maintainer__  = __author__
__email__       = 't.ottavi@medi.fr'
__version__     = '0.2'
__versiondate__ = '20221231'


#==============================================================================
# History
#==============================================================================

'''
- 20221231 : v0.2 Standalone library
- 20190509 : v0.1 Initial version for DRAGON project
'''


################################################################################
#                                                                              #
#                                SHORTCUTS                                     #
#                                                                              #
################################################################################

# ===============================================================================
# SuperDebug enables lots of additional prints for AsyncIO debugging purposes
# without polluting log files.
# ===============================================================================

SUPER_DEBUG = True  # Enable SuperDebug globally here / use dprint() in code


def dprint (txt):
  if SUPER_DEBUG:
    print ('  ... %s' % txt)
  
  
################################################################################
#                                                                              #
#                                   LOGGING                                    #
#                                                                              #
################################################################################

import logging
import os

# ==== Default log level values values
# Possible values are :
#   logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG
# Useful values are :
#   logging.INFO : standard logging
#   logging.DEBUG : includes debugging information and packet dump / decoding

# NOTE : It's not needed to change the global values here. You can change values
#        individually for each system in the config file.

LOG_DEFAULT_FILE_LEVEL = logging.INFO
LOG_DEFAULT_CONSOLE_LEVEL = logging.INFO


# ===============================================================================
# Default path for log files
# ===============================================================================

import platform

if platform.system () == "Windows":
  LOG_DEFAULT_PATH = os.getenv ('temp')
else:
  LOG_DEFAULT_PATH = "/var/log"


# ===============================================================================
# Create specific logger
# ===============================================================================

def CreateLogger (name, file_level=LOG_DEFAULT_FILE_LEVEL, console_level=LOG_DEFAULT_CONSOLE_LEVEL):
  
  # Create logger object
  try:
    print ('LOGGER Initializing...')
    logger = logging.getLogger (name)
    logger.setLevel (logging.DEBUG)  # This is the global level. Must be higher than other individual values. Don't change.
    formatter_timed = logging.Formatter ('%(asctime)s %(name)s %(levelname)s %(message)s')
    formatter_normal = logging.Formatter ('%(name)s %(levelname)s %(message)s')
  except:
    print ('LOGGER Exception creating logger.')
    logger = None
  
  if logger is not None:
    
    # Create an application subfolder in the default log folder
    try:
      print ('LOGGER Base directory for log files is %s' % LOG_DEFAULT_PATH)
      log_folder_name = os.path.join (LOG_DEFAULT_PATH, name)
      if not os.path.exists (log_folder_name):
        print ('LOGGER Subfolder %s does not exist, creating it...' % log_folder_name)
        os.makedirs (log_folder_name)
      else:
        print ('LOGGER Subfolder %s already exists.' % log_folder_name)
    except:
      pass
      
    # Create file handler : all log messages are written there
    try:
      log_filename = os.path.join (log_folder_name, name + ".log")
      print ('LOGGER Trying to use log file %s' % (log_filename))
      fh = logging.FileHandler (log_filename)
      fh.setLevel (file_level)
      fh.setFormatter (formatter_timed)
      logger.addHandler (fh)
      print ('LOGGER Log file ready.')
    except:
      print ('LOGGER Exception creating log file. Check filename, path and access rights.' % log_filename)
    
    # Create console handler : all log messages are also written on the screen
    try:
      print ('LOGGER Creating console output handler...')
      ch = logging.StreamHandler ()
      ch.setLevel (console_level)
      ch.setFormatter (formatter_normal)
      logger.addHandler (ch)
      print ('LOGGER Console output ready.')
    except:
      print ('LOGGER Exception creating console log output handler.')
  
  return logger


# ===============================================================================
# Returns a loglevel name in plain text
# ===============================================================================

LOG_LEVELS = {'CRITICAL': logging.CRITICAL,
              'ERROR'   : logging.ERROR,
              'WARNING' : logging.WARNING,
              'INFO'    : logging.INFO,
              'DEBUG'   : logging.DEBUG}


def GetLogLevelTextFromValue (loglevel):
  levelname = {value: name for name, value in LOG_LEVELS.items ()} [loglevel]
  return levelname


# ===============================================================================
# Configure a specific logger according to system settings from config file
# ===============================================================================
# (If no specified value or invalid value, use default logging options)

def ConfigureLoggerLevel (conf_console_level, conf_file_level):
  final_console_level = LOG_LEVELS [
    conf_console_level] if conf_console_level in LOG_LEVELS.keys () else LOG_DEFAULT_CONSOLE_LEVEL
  final_file_level = LOG_LEVELS [conf_file_level] if conf_file_level in LOG_LEVELS.keys () else LOG_DEFAULT_FILE_LEVEL
  
  final_console_text = GetLogLevelTextFromValue (final_console_level)
  final_file_text = GetLogLevelTextFromValue (final_file_level)
  
  return final_console_level, final_file_level, final_console_text, final_file_text


################################################################################
#                                                                              #
#                                  M A I N                                     #
#                                                                              #
################################################################################

if __name__ == '__main__':
  print ("%s - %s" % (__appname__, __description__))
  print ("%s" % (__copyright__))
  print ("Version %s (%s)" % (__version__, __versiondate__))
  print ("This software is a library, to be called from other modules. It does nothing by itself.")


