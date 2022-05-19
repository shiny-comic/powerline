import subprocess
from traceback import print_exc

try:
    __version__ = subprocess.check_output(['git', 'describe', '--abbrev=0', '--tags']).strip().decode()
except Exception:
    print_exc()
    __version__ = '1.9.4'


def get_version():
    try:
        return __version__ + '.' + subprocess.check_output(['git', 'rev-list', '--count', __version__ + '..HEAD']).strip().decode()
    except Exception:
        print_exc()
        return __version__

