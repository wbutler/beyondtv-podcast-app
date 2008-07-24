import Config
import Debug
import RecordingsWatcher
import StorageManager
import Transcoder


queryStrings = StorageManager.GetSearchStrings( )
results = RecordingsWatcher.GetAvailableRecordings( queryStrings )
requests = StorageManager.GetTranscodeRequests( results )



