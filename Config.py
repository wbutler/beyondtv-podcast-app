import os

CONFIG_DIR = os.path.join( os.path.expanduser("~"), ".tvpodcast" )
SEARCHES_FILE = "searches.txt"
LOG_FILE = "logs.txt"
HASHES_FILE = "hashes.pk"
RUN_FILE = "RUNNING.txt"
PODCAST_METADATA_FILE = "podcasts.pk"

TV_SOURCE_DIR = "/mnt/tv"
TV_SOURCE_EXTENSIONS = ["avi"]

WWW_ROOT_DIR = "/www"
WWW_PODCAST_DIR = "/podcasts"
PODCAST_RECORDING_WWW_DIR = WWW_ROOT_DIR + WWW_PODCAST_DIR + "/videos"

WWW_ROOT_URL = "http://192.168.1.105"

# Amount of time in seconds to sleep in order to see
# if a file in the store is still growing, i.e. still
# being recorded and thus not ready for processing.
GROWTH_CHECK_WAIT_PERIOD = 1

# Number of lines in a single podcast specification
# in the searches file
LINES_PER_SEARCH_RECORD = 3

# Number of recordings per podcast to save before
# episodes are deleted to make room
MAX_PODCAST_SIZE = 3
