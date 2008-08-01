
import os
import sys
import time
import Config
import Debug
import Recording

# Initialization - make sure we're allowed to read the recordings directory
if (not os.access( Config.TV_SOURCE_DIR, os.R_OK ) ):
    Debug.LogEntry( "Unable to read recordings directory", Debug.ERROR )
    sys.exit( -1 )

# Given a list of substrings to match, the function will examine the
# recordings directory, find the video files with the appropriate
# extension, and return a dictionary matching the search strings to
# sets of available files that contain those strings in their names.
def GetAvailableRecordings( stringsList ):
    matchingRecordings = {}
    rawFileList = os.listdir( Config.TV_SOURCE_DIR )

    # Clean the list so we only have relevant video files
    cleanFileList = set()
    for fileName in rawFileList:
        for extension in Config.TV_SOURCE_EXTENSIONS:
            if( fileName[len(fileName)-len(extension):]==extension ):
                cleanFileList.add( fileName )
    
    # Sort files per podcast
    for searchString in stringsList:
        matchingRecordings[searchString] = set()
        for fileName in cleanFileList:
            if( fileName.find( searchString ) != -1 ):
                newRecording = Recording.Recording(os.path.join( Config.TV_SOURCE_DIR, fileName ))
                newRecording.LookupDetails( )
                matchingRecordings[searchString].add( newRecording )

    for podcast in matchingRecordings.keys():
        Debug.LogEntry( podcast, Debug.DEBUG )
        for recording in matchingRecordings[podcast]:
            Debug.LogEntry( "  "+str(recording), Debug.DEBUG )

    return matchingRecordings


##CHANGE THIS TO USE ARRAYS INSTEAD OF DICTS
# Given a list of filenames in its store, we return only those files
# whose sizes are not growing and therefore those files which are
# done recording and ready for encoding as a podcast
def PruneRecordings( recordingsList ):
    oldSize = {}
    newSize = {}
    for recording in recordingsList:
        fullPath = recording.pathToFile
        if( not os.access( fullPath, os.R_OK ) ):
            Debug.LogEntry( "Unable to access file: %s" % fullPath, Debug.ERROR )
        else:
            oldSize[fullPath] = os.path.getsize(fullPath)

    time.sleep( Config.GROWTH_CHECK_WAIT_PERIOD )

    for fullPath in oldSize.keys():
        newSize[fullPath] = os.path.getsize(fullPath)

    Debug.LogEntry( "File growth check:", Debug.DEBUG )

    finishedRecordings = []
    for fullPath in oldSize.keys():
        Debug.LogEntry( "  %s: was %dB, now %dB" % (fullPath, oldSize[fullPath], newSize[fullPath]), Debug.DEBUG )
        if oldSize[fullPath] == newSize[fullPath]:
            finishedRecordings.append( fullPath )
            Debug.LogEntry( "    Adding to list.", Debug.DEBUG )

    return finishedRecordings
