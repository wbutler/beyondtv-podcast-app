import Config
import os
import sys
import time

# Available logging levels; output at higher values is a
# superset of output at lower levels. Use these values as
# input to SetLogLevel
ERROR = 0
NORMAL = 1
DEBUG = 2

# Default level of logging for the application
RUNTIME_LOG_LEVEL = DEBUG

# If this file is present in the config dir, the app will not
# launch in order to preserve logging information for later
KILL_FILE_NAME = "FATALERROR.txt"
        
def GetCurrentTimeString( ):
    return time.strftime( "%x %X", time.localtime(time.time()))

#def SetLogLevel( newLevel ):
#    Debug.RUNTIME_LOG_LEVEL = newLevel

def LogEntry( text, logLevel ):
    try:
        if (logLevel <= RUNTIME_LOG_LEVEL):
            logFile = open( os.path.join(Config.CONFIG_DIR, Config.LOG_FILE), "a" )
            logFile.write( GetCurrentTimeString() + " " + text + "\n" )
            logFile.close()
    except IOError:
        print( "Error writing to log file at %s. Halting program." % LOG_FILE_FULL_NAME )
        sys.exit( -1 )

    if( logLevel == ERROR ):
        errorFile = open( os.path.join(Config.CONFIG_DIR, KILL_FILE_NAME), 'w' )
        errorFile.write( "Fatal error. See log file." )
        errorFile.close()


# Initialization code: make sure we can get to the log file
if( not os.access( Config.CONFIG_DIR, os.W_OK ) ):
    print( "Unable to access log file. Halting program." )
    sys.exit( -1 )

# If the kill file is present, don't run at all.
if( os.path.exists( os.path.join(Config.CONFIG_DIR, KILL_FILE_NAME) )):
    print( "Previous fatal error. Examine log file to debug." )
    sys.exit( -1 )

# Start the log
LOG_FILE_FULL_NAME = os.path.join(Config.CONFIG_DIR, Config.LOG_FILE)
if( os.path.exists( LOG_FILE_FULL_NAME ) ):
    os.unlink( LOG_FILE_FULL_NAME )
LogEntry( "Initializing the log at %s." % LOG_FILE_FULL_NAME, RUNTIME_LOG_LEVEL )
