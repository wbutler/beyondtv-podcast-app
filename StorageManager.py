import os
import pickle
import re
import shutil
import sys

import Config
import Debug
import Podcast
import Recording


# This function looks at the config files and returns a list of
# strings that specify the search inputs for each of the podcasts. 
def GetSearchStrings( ):

    searchStrings = Podcasts.keys()

    Debug.LogEntry( "Search strings: %s" % str(searchStrings), Debug.DEBUG )
    return searchStrings

def GetTranscodeRequests( availableRecordingSets ):

    Debug.LogEntry( "In GetTranscodeRequests", Debug.DEBUG )

    requestList = []
    for searchString in availableRecordingSets.keys():
        for recording in availableRecordingSets[searchString]:
            if not Podcasts[searchString].Contains( recording ):
                if Podcasts[searchString].IsRecent( recording ):
                    requestList.append( recording )

    # Sort the list so the most recently recorded video is first
    requestList.sort( lambda i1, i2: cmp(i2.pubDate, i1.pubDate) )

    Debug.LogEntry( "Requested files list:", Debug.DEBUG )
    for recording in requestList:
        Debug.LogEntry( "  "+str(recording), Debug.DEBUG )

    return requestList



# Adds a finished recording to the store and writes
# updated XML files and hash file
def Submit( recording ):

    Debug.LogEntry( "Storing recording: %s" % str(recording), Debug.DEBUG )

    for podcast in Podcasts.keys():
        pass

    # Add the file to the relevant podcasts
    for search in Podcasts.keys():
        if re.search( search, recording.pathToFile ):
            Debug.LogEntry( "Recording %s matches podcast %s" % (str(recording), str(Podcasts[search])), Debug.DEBUG )
            Podcasts[search].AddRecording( recording )

    # Store the updated podcasts array
    Debug.LogEntry( "Ready to write podcast metadata to file.", Debug.DEBUG )
    for podcast in Podcasts.values():
        Debug.LogEntry( str(podcast), Debug.DEBUG )
        for recording in podcast.Recordings:
            Debug.LogEntry( "  %s" % str(recording), Debug.DEBUG )

    try:
        outFile = open( PodcastFile, 'w' )
        pickle.dump( Podcasts, outFile )
        outFile.close()
    except:
        Debug.LogEntry( "Error writing to podcast metadata file. Exiting.", Debug.ERROR )
        sys.exit( -1 )

    # Store the hash of this file
    FileHashes.append( recording.guid )
    try:
        outFile = open(os.path.join( Config.CONFIG_DIR, Config.HASHES_FILE ), 'w')
        pickle.dump( FileHashes, outFile )
        outFile.close()
    except:
        Debug.LogEntry( "Error writing to hash file. Exiting.", Debug.ERROR )
        sys.exit( -1 )

def WritePodcasts( ):
    for podcast in Podcasts.values():
        podcast.WriteXML()

# Initialization code
Debug.LogEntry( "Initializing StorageManager", Debug.DEBUG )
searchFilePath = os.path.join( Config.CONFIG_DIR, Config.SEARCHES_FILE )
Debug.LogEntry( "Looking for searches file at %s" % searchFilePath, Debug.DEBUG )
PodcastFile = os.path.join( Config.CONFIG_DIR, Config.PODCAST_METADATA_FILE )

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
SearchStrings = []
for i in range( len(cleanLines)/Config.LINES_PER_SEARCH_RECORD ):
    newItem = []
    for element in cleanLines[i*Config.LINES_PER_SEARCH_RECORD:i*Config.LINES_PER_SEARCH_RECORD+Config.LINES_PER_SEARCH_RECORD]:
        newItem.append( element )
    SearchObjects.append( newItem )
    Debug.LogEntry( "Adding item to SearchObjects list: %s" % str(newItem), Debug.DEBUG )
    SearchStrings.append( newItem[0] )

# Read in old file hashes
FileHashes = []
Debug.LogEntry( "Reading old file hashes from %s" % os.path.join( Config.CONFIG_DIR, Config.HASHES_FILE ), Debug.DEBUG )
try:
    inFile = open(os.path.join( Config.CONFIG_DIR, Config.HASHES_FILE ), 'r')
    FileHashes = pickle.load( inFile )
    Debug.LogEntry( "Hash read complete.", Debug.DEBUG )
    inFile.close()
except:
    Debug.LogEntry( "No file hashes found. Assuming a new install.", Debug.NORMAL )

    # We don't have records of old files, so the repository directory is in an
    # unknown state. Unlink it and recreate it to clean it out.
    Debug.LogEntry( "Unlinking directory at %s." % Config.PODCAST_RECORDING_WWW_DIR, Debug.NORMAL )
    if not os.access( Config.PODCAST_RECORDING_WWW_DIR, os.W_OK ):
        Debug.LogEntry( "Access to videos directory denied. Exiting.", Debug.ERROR )
        sys.exit( -1 )
    try:
        shutil.rmtree( Config.PODCAST_RECORDING_WWW_DIR )
        os.mkdir( Config.PODCAST_RECORDING_WWW_DIR )
    except:
        Debug.LogEntry( "Failed to reset videos directory. Exiting.", Debug.ERROR )

    Debug.LogEntry( "Videos directory reset.", Debug.DEBUG )
    

# Read in podcast storage records
Podcasts = {}
PodcastFile = os.path.join( Config.CONFIG_DIR, Config.PODCAST_METADATA_FILE )
Debug.LogEntry( "Reading podcast metadata from %s" % PodcastFile, Debug.DEBUG )
try:
    inFile = open( PodcastFile, 'r' )
    Podcasts = pickle.load( inFile )
    Debug.LogEntry( "Podcast read complete.", Debug.DEBUG )
    inFile.close()

except:
    Debug.LogEntry( "No podcasts file present. Rebuilding from searches.", Debug.NORMAL )

# Verify that we have a podcast object for every search
for search in SearchObjects:
    if search[0] in Podcasts.keys():
        Debug.LogEntry( "Search %s matches %s" % (search[0], str(Podcasts[search[0]])), Debug.DEBUG )
    else:
        Debug.LogEntry( "Search %s not in podcasts list." % search[0], Debug.DEBUG )
        newPodcast = Podcast.Podcast( Search = search[0], Title = search[1], RssFileName = search[2] )
        Podcasts[search[0]] = newPodcast
        Debug.LogEntry( "Adding new podcast to list:", Debug.DEBUG )
        Debug.LogEntry( str(Podcasts[search[0]]), Debug.DEBUG )

        # Make sure that every podcast has a place for its files to land
        Debug.LogEntry( "Creating new storage directory for %s at %s" % ( newPodcast.Title, newPodcast.RecordingDir ), Debug.DEBUG )
        try:
            if os.path.exists( newPodcast.RecordingDir ):
                os.rmdir( newPodcast.RecordingDir )
            os.mkdir( newPodcast.RecordingDir )
        except:
            Debug.LogEntry( "Error creating storage directory %s" % newPodcast.RecordingDir, Debug.DEBUG )
        

# Verify that there is no podcast without an entry in
# the searches list
for podcast in Podcasts.values():
    if not podcast.Search in SearchStrings:
        Debug.LogEntry( "Podcast %s does not match any search. Deleting." % str(podcast), Debug.DEBUG )
        del Podcasts[podcast.Search]

Debug.LogEntry( "Final list of podcasts to service:", Debug.DEBUG )
for podcast in Podcasts.values():
    Debug.LogEntry( "  %s" % str(podcast), Debug.DEBUG )


Debug.LogEntry( "StorageManager initialization complete", Debug.DEBUG )
