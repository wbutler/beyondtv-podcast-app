import os
import pickle
import sys

import Config
import Debug
import Recording


# This function looks at the config files and returns a list of
# strings that specify the search inputs for each of the podcasts. 
def GetSearchStrings( ):
    searchStrings = []
    for element in SearchObjects:
        searchStrings.append( element[0] )

    Debug.LogEntry( "Search strings: %s" % str(searchStrings), Debug.DEBUG )
    return searchStrings

def GetTranscodeRequests( availableRecordingSets ):

    Debug.LogEntry( "In GetTranscodeRequests", Debug.DEBUG )

    requestList = []
    for searchString in availableRecordingSets.keys():
        for recording in availableRecordingSets[searchString]:
            if not recording.guid in FileHashes:
                requestList.append( recording )

    # Sort the list so the most recently recorded video is first
    requestList.sort( lambda i1,i2: cmp( i2.pubDate, i1.pubDate ) )

    Debug.LogEntry( "Requested files list:", Debug.DEBUG )
    for recording in requestList:
        Debug.LogEntry( "  "+str(recording), Debug.DEBUG )

    return requestList



# Adds a finished recording to the store and writes
# updated XML files and hash file
def Submit( recording ):

    Debug.LogEntry( "Storing recording: %s" % str(recording), Debug.DEBUG )

    # Store the hash of this file
    FileHashes.append( recording.guid )
    try:
        outFile = open(os.path.join( Config.CONFIG_DIR, Config.HASHES_FILE ), 'w')
        pickle.dump( FileHashes, outFile )
        outFile.close()
    except:
        Debug.LogEntry( "Error writing to hash file. Exiting.", Debug.ERROR )
        sys.exit( -1 )





# Initialization code
Debug.LogEntry( "Initializing StorageManager", Debug.DEBUG )
searchFilePath = os.path.join( Config.CONFIG_DIR, Config.SEARCHES_FILE )
Debug.LogEntry( "Looking for searches file at %s" % searchFilePath, Debug.DEBUG )

# Read lines out of the searches file
try:
    searchFile = open( searchFilePath, 'r' )
    lines = searchFile.readlines()
except:
    Debug.LogEntry( "Unable to read searches file. Halting program.", Debug.ERROR )
    sys.exit( -1 )

# Strip out comments and blank lines from the searches file
cleanLines = []
for rawLine in lines:
    line = rawLine.rstrip()
    if( len(line) > 0 and line[0] != '#' ):
        cleanLines.append( line )

# Make sure that we have the right number of lines
# in the searches file
if( len(cleanLines) % Config.LINES_PER_SEARCH_RECORD != 0 ):
    Debug.LogEntry( "Malformed searches file. Incomplete records present.", Debug.ERROR )
    sys.exit( -1 )

# Build search string/podcast name pairs
SearchObjects = []
for i in range( len(cleanLines)/Config.LINES_PER_SEARCH_RECORD ):
    newItem = []
    for element in cleanLines[i*Config.LINES_PER_SEARCH_RECORD:i*Config.LINES_PER_SEARCH_RECORD+Config.LINES_PER_SEARCH_RECORD]:
        newItem.append( element )
    SearchObjects.append( newItem )
    Debug.LogEntry( "Adding item to SearchObjects list: %s" % str(newItem), Debug.DEBUG )

# Read in old file hashes
FileHashes = []
Debug.LogEntry( "Reading old file hashes from %s" % os.path.join( Config.CONFIG_DIR, Config.HASHES_FILE ), Debug.DEBUG )
try:
    inFile = open(os.path.join( Config.CONFIG_DIR, Config.HASHES_FILE ), 'r')
    FileHashes = pickle.load( inFile )
    Debug.LogEntry( "Hash read complete.", Debug.DEBUG )
    inFile.close()
except:
    Debug.LogEntry( "No file hashes found. Assuming a new install.", Debug.ERROR )
    # TODO: We don't have any hashes. We need to rebuild the videos repository.

Debug.LogEntry( "StorageManager initialization complete", Debug.DEBUG )
