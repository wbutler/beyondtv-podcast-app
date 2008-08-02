import sys

import Config
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

