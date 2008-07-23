import Config
import Debug
import RecordingsWatcher
import Transcoder

strs = ["Daily", "Colbert", "Soup"]
files = []
results = RecordingsWatcher.GetAvailableRecordings(strs)

#for fileSet in results.values():
#    for fileName in fileSet:
#        files.append( fileName )

#RecordingsWatcher.RemoveGrowingFiles( files )
