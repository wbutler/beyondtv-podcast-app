import os

LOG_DIR = os.path.expanduser("~")
LOG_FILE = ".tvpodcastlogs"

TV_SOURCE_DIR = "/mnt/tv"
TV_SOURCE_EXTENSIONS = ["avi"]

# Amount of time in seconds to sleep in order to see
# if a file in the store is still growing, i.e. still
# being recorded and thus not ready for processing.
GROWTH_CHECK_WAIT_PERIOD = 5
