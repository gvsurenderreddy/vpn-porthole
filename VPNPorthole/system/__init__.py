import platform

from VPNPorthole.system.docker import Docker
from VPNPorthole.system.shell import popen, Pexpect
from VPNPorthole.system.path import TmpDir, TmpFifo, abs_path


if platform.system() == 'Darwin':
    from VPNPorthole.system.darwin import route_add, route_del, docker_host, resolver_add, resolver_del
elif platform.system() == 'debian':
    from VPNPorthole.system.debian import route_add, route_del, docker_host, resolver_add, resolver_del
else:
    raise NotImplementedError(platform.system())

__all__ = ['Docker', 'popen', 'Pexpect', 'TmpDir', 'TmpFifo', 'abs_path', 'route_add', 'route_del',
           'docker_host', 'resolver_add', 'resolver_del']
