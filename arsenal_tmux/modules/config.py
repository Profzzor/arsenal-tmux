import os
import subprocess
from os.path import dirname, abspath, expanduser, join

# Base paths
DATAPATH = join(dirname(dirname(abspath(__file__))), 'data')
BASEPATH = dirname(dirname(dirname(abspath(__file__))))
HOMEPATH = expanduser("~")
FORMATS = ["md", "yml"]
EXCLUDE_LIST = ["README.md"]
FUZZING_DIRS = ["/usr/local/share/wordlists/**/*.txt"]

CHEATS_PATHS = [
    join(DATAPATH, "cheats"),  # DEFAULT
    join(BASEPATH, "my_cheats"),
    join(HOMEPATH, ".cheats"),
    "/opt/my-resources/my-cheats",
    "/opt/my-resources/setup/arsenal-cheats"
]

messages_error_missing_arguments = 'Error missing arguments'

# Set lower delay to use ESC key (in ms)
os.environ.setdefault('ESCDELAY', '25')
os.environ['TERM'] = 'xterm-256color'

# Function to get tmux session's initial directory
def get_tmux_session_path():
    try:
        # Run tmux command to get session path
        result = subprocess.run(
            ['tmux', 'display-message', '-p', '#{session_path}'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # Fallback to current directory if not in tmux or error occurs
        return os.getcwd()

# Determine savevarfile path
if os.environ.get('ARSENAL_LOCAL'):
    savevarfile = join(HOMEPATH, "arsenal.json")
else:
    # Use tmux session's initial directory if in tmux, else fall back to os.getcwd()
    savevarfile = join(get_tmux_session_path(), "arsenal.json")
    
PREFIX_GLOBALVAR_NAME = "arsenal_prefix_cmd"