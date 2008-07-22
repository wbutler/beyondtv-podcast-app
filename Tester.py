import Config
import Debug
import RecordingsWatcher

strs = ["Daily", "Colbert", "Soup"]
files = []
results = RecordingsWatcher.GetAvailableFiles(strs)
for fileSet in results.values():
    for fileName in fileSet:
        files.append( fileName )

print RecordingsWatcher.RemoveGrowingFiles( files )
