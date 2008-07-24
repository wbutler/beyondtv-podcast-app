import copy
import os
import Config
import Debug

def ConvertFile( inputRecording ):
    Debug.LogEntry( "Beginning transcoder module with %s" % str( inputRecording ), Debug.DEBUG )

    encoderString = "podencoder -o %s %s" % ( Config.PODCAST_RECORDING_WWW_DIR, inputRecording.pathToFile )
    Debug.LogEntry( "Executing shell command: %s" % encoderString, Debug.NORMAL )
