import copy
import os
import shutil
import sys
from xml.dom.minidom import Document

import Config
import Debug
import Recording

DEFAULT_TTL = "60"
DEFAULT_LANGUAGE = "en-us"
DEFAULT_COPYRIGHT = "Copyright Notice TK"
DEFAULT_AUTHOR = "Author TK"
DEFAULT_CATEGORY = "Television"
DEFAULT_OWNER_NAME = "BeyondTV Podcast Generator"
DEFAULT_OWNER_EMAIL = "Owner Email TK"
DEFAULT_IMAGELINK = Config.WWW_ROOT_URL + "/pirate.png"
DEFAULT_SUBTITLE = "Subtitle TK"
DEFAULT_SUMMARY = "Summary TK"
DEFAULT_DESCRIPTION = "Description TK"

class Podcast:
    Ttl = DEFAULT_TTL
    Language = DEFAULT_LANGUAGE
    Copyright = DEFAULT_COPYRIGHT
    Author = DEFAULT_AUTHOR
    OwnerName = DEFAULT_OWNER_NAME
    OwnerEmail = DEFAULT_OWNER_EMAIL
    Category = DEFAULT_CATEGORY
    ImageLink = DEFAULT_IMAGELINK
    Subtitle = DEFAULT_SUBTITLE
    Summary = DEFAULT_SUMMARY
    Description = DEFAULT_DESCRIPTION

    def __init__( self, Search, RssFileName, Ttl = "", Title = "", Language = "", Copyright = "", Subtitle = "", Author = "", Summary = "", Description = "", ImageLink = "" ):
        self.Search = Search
        self.RssFileName = RssFileName
        self.__RecordingDir = os.path.join( Config.PODCAST_RECORDING_WWW_DIR, self.RssFileName[0:-4] )
        self.XmlDocument = None
        self.Recordings = []
        if Ttl != "":
            self.Ttl = Ttl
        self.Title = Title
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

    def GetRecordingDir( self ):
        return self.__RecordingDir

    def SetRecordingDir( self, x ):
        pass

    def GetLink( self ):
        return Config.WWW_ROOT_URL + Config.WWW_PODCAST_DIR + "/" + self.RssFileName

    def SetLink( self ):
        pass

    RecordingDir = property( GetRecordingDir, SetRecordingDir )
    Link = property( GetLink, SetLink )

    def IsRecent( self, recording ):
        if( len(self.Recordings) < Config.MAX_PODCAST_SIZE ):
            Debug.LogEntry( "Podcast %s is not full. Recording %s is considered recent." % (str(self.Title), recording.pathToFile), Debug.DEBUG )
            return True
        else:
            self.Recordings.sort( lambda i1, i2: cmp(i1.pubDate, i2.pubDate), reverse = True )
            if( recording.pubDate > self.Recordings[len(self.Recordings)-1].pubDate ):
                Debug.LogEntry( "Recording %s is recent for podcast %s." % (recording.pathToFile, str(self.Title)), Debug.DEBUG )
                return True
            else:
                Debug.LogEntry( "Recording %s is too old for podcast %s." % (recording.pathToFile, str(self.Title)), Debug.DEBUG )
                return False

    def AddRecording( self, recording ):
        Debug.LogEntry( "Adding recording %s to podcast %s." % (recording.pathToFile, self.Title), Debug.DEBUG )
        
        newRecording = copy.deepcopy( recording )
        Debug.LogEntry( "Copying %s to %s" % (newRecording.pathToFile, self.RecordingDir), Debug.DEBUG )

        try:
            shutil.copy( newRecording.pathToFile, self.RecordingDir )
        except:
            Debug.LogEntry( "Failed to copy %s to %s" % (newRecording.pathToFile, self.RecordingDir), Debug.DEBUG )
            sys.exit( -1 )
        newRecording.pathToFile = os.path.join(self.RecordingDir, os.path.basename( newRecording.pathToFile ))
        Debug.LogEntry( "File copy complete. New file at %s" % newRecording.pathToFile, Debug.DEBUG )

        if( len(self.Recordings) < Config.MAX_PODCAST_SIZE ):
            self.Recordings.append( newRecording )
        else:
            self.Recordings.sort( lambda i1, i2: cmp(i1.pubDate, i2.pubDate) )
            Debug.LogEntry( "In podcast %s, replacing %s with %s" % (self.Title, self.Recordings[0].pathToFile, recording.pathToFile), Debug.DEBUG )
            Debug.LogEntry( "Deleting %s" % self.Recordings[0].pathToFile, Debug.DEBUG )
            try:
                os.remove( self.Recordings[0].pathToFile )
            except:
                Debug.LogEntry( "Failed to delete %s" % self.Recordings[0].pathToFile, Debug.ERROR )
                sys.exit( -1 )
            self.Recordings[0] = newRecording
        
        self.Recordings.sort( lambda i1, i2: cmp(i1.pubDate, i2.pubDate), reverse = True )

    def XmlAddTextElement( self, parentElement, name, text ):
        newElement = self.XmlDocument.createElement( name )
        parentElement.appendChild( newElement )
        newText = self.XmlDocument.createTextNode( text )
        newElement.appendChild( newText )

    def XmlAddPodcastItem( self, parentElement, title = "", author = "", subtitle = "", summary = "", url = "", type = "audio/x-m4v", guid = "", date = "", duration = "", keywords = ""):
        itemElement = self.XmlDocument.createElement( "item" )
        parentElement.appendChild( itemElement )
        self.XmlAddTextElement( itemElement, "title", title )
        self.XmlAddTextElement( itemElement, "itunes:author", author )
        self.XmlAddTextElement( itemElement, "itunes:subtitle", subtitle )
        self.XmlAddTextElement( itemElement, "itunes:summary", summary )
        enclosureElement = self.XmlDocument.createElement( "enclosure" )
        enclosureElement.setAttribute( "url", url )
        enclosureElement.setAttribute( "type", type )
        itemElement.appendChild( enclosureElement )
        self.XmlAddTextElement( itemElement, "guid", guid )
        self.XmlAddTextElement( itemElement, "pubDate", date )
        self.XmlAddTextElement( itemElement, "itunes:duration", duration )
        self.XmlAddTextElement( itemElement, "itunes:keywords", keywords )

    def GenerateXMLString( self ):

        self.XmlDocument = Document()

        rssElement = self.XmlDocument.createElement( "rss" )
        rssElement.setAttribute( "version", "2.0" )
        rssElement.setAttribute( "xmlns:itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd" )
        self.XmlDocument.appendChild( rssElement )

        channelElement = self.XmlDocument.createElement( "channel" )
        rssElement.appendChild( channelElement )

        self.XmlAddTextElement( channelElement, "ttl", self.Ttl )
        self.XmlAddTextElement( channelElement, "title", self.Title )
        self.XmlAddTextElement( channelElement, "link", self.Link )
        self.XmlAddTextElement( channelElement, "language", self.Language )
        self.XmlAddTextElement( channelElement, "copyright", self.Copyright )
        self.XmlAddTextElement( channelElement, "itunes:subtitle", self.Subtitle )
        self.XmlAddTextElement( channelElement, "itunes:author", self.Author )
        self.XmlAddTextElement( channelElement, "itunes:summary", self.Summary )
        self.XmlAddTextElement( channelElement, "description", self.Description )

        ownerElement = self.XmlDocument.createElement( "itunes:owner" )
        channelElement.appendChild( ownerElement )
        self.XmlAddTextElement( ownerElement, "itunes:name", self.OwnerName )
        self.XmlAddTextElement( ownerElement, "itunes:email", self.OwnerEmail )

        imageElement = self.XmlDocument.createElement( "itunes:image" )
        imageElement.setAttribute( "href", self.ImageLink )
        channelElement.appendChild( imageElement )
        
        self.XmlAddTextElement( channelElement, "itunes:category", self.Category )

        for recording in self.Recordings:
            newUrl = Config.WWW_ROOT_URL + recording.pathToFile[len(Config.WWW_ROOT_DIR):]
            newDate = "hello"
            self.XmlAddPodcastItem( parentElement=channelElement, title=recording.title, author=recording.author, subtitle=recording.subtitle, summary=recording.summary, url = newUrl, guid=recording.guid, duration=recording.duration )

        return self.XmlDocument.toprettyxml(indent = "\t", encoding = "UTF-8")


    def WriteXML( self ):
        RssFilePath = os.path.join( Config.WWW_ROOT_DIR + Config.WWW_PODCAST_DIR, self.RssFileName )
        Debug.LogEntry( "Writing RSS file for %s to %s" % (self.Title, RssFilePath), Debug.DEBUG )
        XMLString = self.GenerateXMLString( )
        outFile = open( RssFilePath, 'w' )
        outFile.write( XMLString )
        outFile.close()
