import Config
import Debug
import Recording

DEFAULT_TTL = "60"
DEFAULT_LANGUAGE = "en-us"
DEFAULT_COPYRIGHT = ""
DEFAULT_AUTHOR = ""
DEFAULT_CATEGORY = "Television"
DEFAULT_OWNER_NAME = "BeyondTV Podcast Generator"
DEFAULT_OWNER_EMAIL = ""

class Podcast:
    Search = ""
    Ttl = DEFAULT_TTL
    Title = ""
    Link = ""
    Language = DEFAULT_LANGUAGE
    Copyright = DEFAULT_COPYRIGHT
    Subtitle = ""
    Author = DEFAULT_AUTHOR
    Summary = ""
    Description = ""
    OwnerName = DEFAULT_OWNER_NAME
    OwnerEmail = DEFAULT_OWNER_EMAIL
    ImageLink = ""
    Category = DEFAULT_CATEGORY
    RssFileName = ""

    Recordings = []

    def __init__( self, Search, RssFileName, Ttl = "", Title = "", Link = "", Language = "", Copyright = "", Subtitle = "", Author = "", Summary = "", Description = "", ImageLink = "" ):
        self.Search = Search
        self.RssFileName = RssFileName
        if Ttl != "":
            self.Ttl = Ttl
        if Title != "":
            self.Title = Title
        if Link != "":
            self.Link = Link
        if Language != "":
            self.Language = Language
        if Copyright != "":
            self.Copyright = Copyright
        if Subtitle != "":
            self.Subtitle = Subtitle
        if Author != "":
            self.Author = Author
        if Summary != "":
            self.Summary = Summary
        if Description != "":
            self.Description = Description
        if ImageLink != "":
            self.ImageLink = ImageLink

    def __str__( self ):
        retstr = "("
        retstr = retstr + str(self.Search) + ","
        retstr = retstr + str(self.RssFileName) + ","
        retstr = retstr + str(self.Ttl) + ","
        retstr = retstr + str(self.Title) + ","
        retstr = retstr + str(self.Link) + ","
        retstr = retstr + str(self.Language) + ","
        retstr = retstr + str(self.Copyright) + ","
        retstr = retstr + str(self.Subtitle) + ","
        retstr = retstr + str(self.Author) + ","
        retstr = retstr + str(self.Summary) + ","
        retstr = retstr + str(self.Description) + ","
        retstr = retstr + str(self.OwnerName) + ","
        retstr = retstr + str(self.OwnerEmail) + ","
        retstr = retstr + str(self.ImageLink) + ","
        retstr = retstr + str(self.Category) + ")"        
        return retstr

    def IsRecent( self, recording ):
        if( len(self.Recordings) < Config.MAX_PODCAST_SIZE ):
            return True
        else:
            Recordings.sort( lambda i1, i2: cmp(i1.pubDate, i2.pubDate) )
            if( recording.pubDate > Recordings[0].pubDate ):
                return True
            else:
                return False
