import DbHelper
import sqlite3 as sql
import videoNoob 

import subprocess
from subprocess import PIPE, STDOUT


out = subprocess.run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file_location])
