from xml.dom.minidom import Document
import random

# Text constants
TTL_TIMEOUT = "60"
TITLE = "BeyondTV Test Podcast"
LINK = "http://192.168.1.105/testpodcast.xml"
LANGUAGE = "en-us"
COPYRIGHT_NOTICE = " 2008 Flaming Penguin Heavy Industries"
SUBTITLE = "Subtitle"
AUTHOR = "Author"
SUMMARY = "Summary"
DESCRIPTION = "Description"
OWNER_NAME = "Owner Name"
OWNER_EMAIL = "owner@email.com"
IMAGE_LINK = "http://192.168.1.105/pirate.png"
CATEGORY = "Television"

# Our test item
TEST_ITEM_TITLE = "Daily Show test"
TEST_ITEM_AUTHOR = "Test item author"
TEST_ITEM_SUBTITLE = "Test item subtitle"
TEST_ITEM_SUMMARY = "Test item summary"
TEST_ITEM_URL = "http://192.168.1.105/trek.avi.mp4"
TEST_ITEM_TYPE = "audio/x-m4v"
TEST_ITEM_GUID = str(int(random.random() * 10000000000))
TEST_ITEM_DATE = "Wed, 17 July 2008 12:00:00 GMT"
TEST_ITEM_DURATION = "30:00"
TEST_ITEM_KEYWORD = "Test item keywords"

def addTextElement( document, parentElement, name, text ):
    newElement = document.createElement( name )
    parentElement.appendChild( newElement )
    newText = doc.createTextNode( text )
    newElement.appendChild( newText )

def addPodcastItem( document, parentElement, title, author, subtitle, summary, url, type, guid, date, duration, keywords):
    itemElement = document.createElement( "item" )
    parentElement.appendChild( itemElement )
    addTextElement( document, itemElement, "title", title )
    addTextElement( document, itemElement, "itunes:author", author )
    addTextElement( document, itemElement, "itunes:subtitle", subtitle )
    addTextElement( document, itemElement, "itunes:summary", summary )
    enclosureElement = document.createElement( "enclosure" )
    enclosureElement.setAttribute( "url", url )
    enclosureElement.setAttribute( "type", type )
    itemElement.appendChild( enclosureElement )
    addTextElement( document, itemElement, "guid", guid )
    addTextElement( document, itemElement, "pubDate", date )
    addTextElement( document, itemElement, "itunes:duration", duration )
    addTextElement( document, itemElement, "itunes:keywords", keywords )

doc = Document()

rssElement = doc.createElement( "rss" )
rssElement.setAttribute( "version", "2.0" )
rssElement.setAttribute( "xmlns:itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd" )
doc.appendChild( rssElement )

channelElement = doc.createElement( "channel" )
rssElement.appendChild( channelElement )

addTextElement( doc, channelElement, "ttl", TTL_TIMEOUT )
addTextElement( doc, channelElement, "title", TITLE )
addTextElement( doc, channelElement, "link", LINK )
addTextElement( doc, channelElement, "language", LANGUAGE )
addTextElement( doc, channelElement, "copyright", COPYRIGHT_NOTICE )
addTextElement( doc, channelElement, "itunes:subtitle", SUBTITLE )
addTextElement( doc, channelElement, "itunes:author", AUTHOR )
addTextElement( doc, channelElement, "itunes:summary", SUMMARY )
addTextElement( doc, channelElement, "description", DESCRIPTION )

ownerElement = doc.createElement( "itunes:owner" )
channelElement.appendChild( ownerElement )
addTextElement( doc, ownerElement, "itunes:name", OWNER_NAME )
addTextElement( doc, ownerElement, "itunes:email", OWNER_EMAIL )

imageElement = doc.createElement( "itunes:image" )
imageElement.setAttribute( "href", IMAGE_LINK )
channelElement.appendChild( imageElement )

addTextElement( doc, channelElement, "itunes:category", CATEGORY )


# Add our items to the channel

addPodcastItem( doc, channelElement, TEST_ITEM_TITLE, TEST_ITEM_AUTHOR, TEST_ITEM_SUBTITLE, TEST_ITEM_SUMMARY, TEST_ITEM_URL, TEST_ITEM_TYPE, TEST_ITEM_GUID, TEST_ITEM_DATE, TEST_ITEM_DURATION, TEST_ITEM_KEYWORD )

print doc.toprettyxml(indent = "\t", encoding = "UTF-8")
# print doc.toxml( encoding = "UTF-8" )
