import platform

from VPNPorthole.system.docker import Docker
from VPNPorthole.system.shell import popen, Pexpect
from VPNPorthole.system.path import TmpDir, TmpFifo, abs_path


if platform.system() == 'Darwin':
    from VPNPorthole.system.darwin import *
elif platform.system() == 'debian':
    from VPNPorthole.system.debian import *
else:
    raise NotImplementedError(platform.system())
