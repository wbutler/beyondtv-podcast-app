import Config
import Debug
import Recording

# This function looks at the config files and returns a list of
# strings that specify the search inputs for each of the podcasts. 
def GetSearchStrings( ):
    return ["Trek", "Daily", "Colbert", "Soup"]


def GetTranscodeRequests( availableRecordingSets ):

    Debug.LogEntry( "Computing work item priorities.", Debug.DEBUG )

    requestList = []
    for searchString in availableRecordingSets.keys():
        for recording in availableRecordingSets[searchString]:
            requestList.append( recording )

    # Sort the list so the most recently recorded video is first
    requestList.sort( lambda i1,i2: cmp( i2.pubDate, i1.pubDate ) )

    for recording in requestList:
        Debug.LogEntry( "  "+str(recording), Debug.DEBUG )

    return requestList
