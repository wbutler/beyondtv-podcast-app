import datetime

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
