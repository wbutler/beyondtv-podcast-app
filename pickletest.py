import pickle
import random

random.seed()

try:
    # Read in some data
    inFile = open('tempdata.pk', 'r')
    data = pickle.load( inFile )
    print( "Reading old data:\n%s\n" % str(data) )
    inFile.close()

except:
    # Couldn't read in any data
    print( "No old data available.\n" )


data = [random.randrange(10), random.randrange(10), random.randrange(10)]
print( "Generating new data:\n%s\n" % str(data) )
outFile = open('tempdata.pk', 'w')
pickle.dump( data, outFile )
outFile.close()
