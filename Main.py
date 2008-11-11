import os
import sys
import fcntl

import Config

def AcquireRunLock( ):
    runFilePath = os.path.join( Config.CONFIG_DIR, Config.RUN_FILE)
    lockFile = open( runFilePath, 'r' )
    try:
        fcntl.flock( lockFile, fcntl.LOCK_EX|fcntl.LOCK_NB )
    except IOError:
        print( "Another instance is already running." )
        sys.exit( 0 )

AcquireRunLock( )
sleep(20)
sys.exit(0)

import Debug
import RecordingsWatcher
import StorageManager
import Transcoder

queryStrings = StorageManager.GetSearchStrings( )
results = RecordingsWatcher.GetAvailableRecordings( queryStrings )
requests = StorageManager.GetTranscodeRequests( results )

if len( requests ) == 0:
    Debug.LogEntry( "No new files. Exiting.", Debug.NORMAL )
    ReleaseRunLock( )
    sys.exit( 0 )

prunedRequests = RecordingsWatcher.PruneRecordings( requests )

if len( prunedRequests ) == 0:
    Debug.LogEntry( "No requests for transcoder. Exiting.", Debug.NORMAL )
    ReleaseRunLock( )
    sys.exit( 0 )

convertedRecording = Transcoder.ConvertFile( prunedRequests[0] )
StorageManager.Submit( convertedRecording )
StorageManager.WritePodcasts( )
