import platform

from vpnporthole.system.docker import Docker
from vpnporthole.system.shell import popen, Pexpect
from vpnporthole.system.path import TmpDir, TmpFifo, abs_path


if platform.system() == 'Darwin':
    from vpnporthole.system.darwin import route_add, route_del, docker_host, resolver_add, resolver_del
elif platform.system() == 'Linux':
    from vpnporthole.system.debian import route_add, route_del, docker_host, resolver_add, resolver_del
else:
    raise NotImplementedError(platform.system())

__all__ = ['Docker', 'popen', 'Pexpect', 'TmpDir', 'TmpFifo', 'abs_path', 'route_add', 'route_del',
           'docker_host', 'resolver_add', 'resolver_del']
