import config
import os
import sys
import time

# Available logging levels; output at higher values is a
# superset of output at lower levels. Use these values as
# input to SetLogLevel
NORMAL = 0
ERROR = 1
DEBUG = 2

# Default level of logging for the application
RUNTIME_LOG_LEVEL = NORMAL

        
def GetCurrentTimeString( ):
    return time.strftime( "%x %X", time.localtime(time.time()))

def SetLogLevel( newLevel ):
    RUNTIME_LOG_LEVEL = newLevel

def LogEntry( text, logLevel ):
    try:
        if (logLevel <= RUNTIME_LOG_LEVEL):
            logFile = open( os.path.join(config.LOG_DIR, config.LOG_FILE), "a" )
            logFile.write( GetCurrentTimeString() + " " + text + "\n" )
            logFile.close()
    except IOError:
        print( "Error writing to log file. Halting program." )
        sys.exit( -1 )


# Initialization code: make sure we can get to the log file
if( not os.access( config.LOG_DIR, os.W_OK ) ):
    print( "Unable to access log file. Halting program." )
    sys.exit( -1 )

# Start the log
LOG_FILE_FULL_NAME = os.path.join(config.LOG_DIR, config.LOG_FILE)
if( os.path.exists( LOG_FILE_FULL_NAME ) ):
    os.unlink( LOG_FILE_FULL_NAME )
LogEntry( "Initializing the log.", RUNTIME_LOG_LEVEL )
