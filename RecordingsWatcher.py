import os
import config
import Debug

if !os.access( config.TV_SOURCE_DIR, os.F_OK ):
    Debug.LogEntry( "Unable to open log file", Debug.ERROR )
