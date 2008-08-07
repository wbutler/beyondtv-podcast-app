import os
import sys

import Config

def AcquireRunLock( ):
    runFilePath = os.path.join( Config.CONFIG_DIR, Config.RUN_FILE)
    if os.path.exists( runFilePath ):
        print( "Another instance is already running." )
        sys.exit( 0 )
    else:
        runFile = open( runFilePath, 'w' )
        runFile.write( "Running" )
        runFile.close()

def ReleaseRunLock( ):
    runFilePath = os.path.join( Config.CONFIG_DIR, Config.RUN_FILE)
    Debug.LogEntry( "Removing file %s" % runFilePath, Debug.DEBUG )
    os.remove( runFilePath )
    
AcquireRunLock( )

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

ReleaseRunLock( )
