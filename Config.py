import os

LOG_DIR = os.path.join( os.path.expanduser("~"), ".tvpodcast" )
LOG_FILE = "logs.txt"

TV_SOURCE_DIR = "/mnt/tv"
TV_SOURCE_EXTENSIONS = ["avi"]

PODCAST_RECORDING_WWW_DIR = "/www/videos"

# Amount of time in seconds to sleep in order to see
# if a file in the store is still growing, i.e. still
# being recorded and thus not ready for processing.
GROWTH_CHECK_WAIT_PERIOD = 5
