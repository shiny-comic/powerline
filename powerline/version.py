import subprocess
from traceback import print_exc

__version__ = "1.9.4"

def get_version():
    try:
        return __version__ + '.dev9999+git.' + str(subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip())
    except Exception:
        print_exc()
        return __version__

