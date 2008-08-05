import copy
import os
import tempfile

import Config
import Debug

def ConvertFile( inputRecording ):
    Debug.LogEntry( "Beginning transcoder module with %s" % str( inputRecording ), Debug.DEBUG )

    # Find a working directory
    tempDir = tempfile.gettempdir()
    Debug.LogEntry( "Using temporary directory at %s" % tempDir, Debug.DEBUG )

    # Construct our shell comand
    inputFilePath = inputRecording.pathToFile
    outputFilePath = os.path.join(tempDir, os.path.basename( inputFilePath )) + ".mp4"
    commandString = "cp \"%s\" \"%s\"" % (inputFilePath, outputFilePath)

    # Run the command
    Debug.LogEntry( "Executing shell command: %s" % commandString, Debug.NORMAL )
    ( stdout, stdin ) = os.popen4( commandString )
    results = stdin.readlines()
    Debug.LogEntry( "Command execution complete.", Debug.NORMAL )

    # Log the results
    # TODO: Fill this in.

    # Return a new recording object
    outputRecording = copy.deepcopy( inputRecording )
    outputRecording.pathToFile = outputFilePath

    Debug.LogEntry( "Transcoder complete: %s" % str(outputRecording), Debug.DEBUG )
    return outputRecording
