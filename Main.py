import os
import sys
import fcntl
import time
import Config

# Before we do anything, let's acquire the run lock to make
# sure that we're the only instance running.
runFilePath = os.path.join( Config.CONFIG_DIR, Config.RUN_FILE)
lockFile = open( runFilePath, 'a+' )
try:
    fcntl.flock( lockFile, fcntl.LOCK_EX|fcntl.LOCK_NB )
except:
    print( "Another instance is already running." )
    sys.exit( 0 )


# Process command line options. Right now, there's only one
# possible option, which specifies that we should run in test
# mode. In this mode, we don't transcode any files or update
# any catalogs, but we do all the bookkeeping and log what
# the results would have been.
testMode = False
try:
    if sys.argv[1] == '-t':
        print( "Running in test mode." )
        testMode = True
except:
    pass


import Debug
import RecordingsWatcher
import StorageManager
import Transcoder

queryStrings = StorageManager.GetSearchStrings( )
results = RecordingsWatcher.GetAvailableRecordings( queryStrings )
requests = StorageManager.GetTranscodeRequests( results )

if len( requests ) == 0:
    Debug.LogEntry( "No new files. Exiting.", Debug.NORMAL )
    sys.exit( 0 )

prunedRequests = RecordingsWatcher.PruneRecordings( requests )

if len( prunedRequests ) == 0:
    Debug.LogEntry( "No requests for transcoder. Exiting.", Debug.NORMAL )
    sys.exit( 0 )

convertedRecording = Transcoder.ConvertFile( prunedRequests[0] )
StorageManager.Submit( convertedRecording )
StorageManager.WritePodcasts( )
