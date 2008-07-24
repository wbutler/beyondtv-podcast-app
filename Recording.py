import datetime
import os
import re
import Debug

class Recording:
    title = ""
    author = ""
    subtitle = ""
    summary = ""
    guid = ""
    pubDate = datetime.datetime.min
    duration = 0
    pathToFile = ""

    def __init__( self, path="" ):
        self.pathToFile = path

    def __str__( self ):
        retStr = "("
        retStr = retStr + str(self.title) + ","
        retStr = retStr + str(self.author) + ","
        retStr = retStr + str(self.subtitle) + ","
        retStr = retStr + str(self.summary) + ","
        retStr = retStr + str(self.guid) + ","
        retStr = retStr + str(self.pubDate) + ","
        retStr = retStr + str(self.duration) + ","
        retStr = retStr + str(self.pathToFile) + ")"
        return retStr

    def LookupDetails( self ):

        # Extract just the filename from the path
        dirName, fileName = os.path.split( self.pathToFile )

        # Get the title
        self.title = fileName[:fileName.find("-")]

        # Get the date
        try:
            dateStr = re.search( '[0-9]{4}-[0-9]{2}-[0-9]{2}', fileName ).group(0)
            self.pubDate = datetime.datetime( int(dateStr[0:4]), int(dateStr[5:7]), int(dateStr[8:10]) )
        except:
            Debug.LogEntry( "Error computing date for recording: %s" % str(self), Debug.ERROR )

        # Build a guid
        self.guid = hash(self.title + str(self.pubDate))

        # Get the duration
        try:
            inPipe, outPipe = os.popen4( "ffmpeg -i \"%s\"" % self.pathToFile )
            for line in outPipe.readlines():
                if( line.find( "Duration" ) != -1 ):
                    timeStr = re.search( '[0-9]{2}:[0-9]{2}:[0-9]{2}', line ).group(0)
                    if( timeStr[0:2] != "00" ):
                        self.duration = timeStr
                    else:
                        self.duration = timeStr[3:]
        except:
            Debug.LogEntry( "Error finding duration for recording: %s" % str(self), Debug.ERROR )

        # Get the summary
        self.summary = "BeyondTV Recording"
