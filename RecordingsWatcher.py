import os
import sys
import Config
import Debug
# Initialization - make sure we're allowed to read the recordings directory
if (not os.access( Config.TV_SOURCE_DIR, os.R_OK ) ):
    Debug.LogEntry( "Unable to read recordings directory", Debug.ERROR )
    sys.exit( -1 )

def GetAvailableFiles( stringsList ):
    matchingFiles = {}
    rawFileList = os.listdir( Config.TV_SOURCE_DIR )

    # Clean the list so we only have relevant video files
    cleanFileList = set()
    for fileName in rawFileList:
        for extension in Config.TV_SOURCE_EXTENSIONS:
            if( fileName.find( extension ) != -1 ):
                cleanFileList.add( fileName )
    
    
    # Debug.LogEntry( "Video files matching extension:", Debug.DEBUG )
    # for fileName in cleanFileList:
    #    Debug.LogEntry( " "+fileName, Debug.DEBUG )

    # Sort files per podcast
    for searchString in stringsList:
        matchingFiles[searchString] = set()
        for fileName in cleanFileList:
            if( fileName.find( searchString ) != -1 ):
                matchingFiles[searchString].add( fileName )

    for podcast in matchingFiles.keys():
        Debug.LogEntry( "  "+podcast, Debug.DEBUG )
        for fileName in matchingFiles[podcast]:
            Debug.LogEntry( "  "+fileName, Debug.DEBUG )

    return matchingFiles
