
from vpnporthole.system.shell import popen

def docker_host():
    return False


def route_add(subnets, ip):
    for subnet in subnets:
        args = ['/usr/bin/sudo', '/usr/local/sbin/ip', 'route', 'add', str(subnet), 'via', ip]
        p = popen(args)
        p.wait()


def route_del(subnets):
    for subnet in subnets:
        args = ['/usr/bin/sudo', '/usr/local/sbin/ip', 'route', 'del', str(subnet)]
        p = popen(args)
        p.wait()


def resolver_add(ip, poer):
    # echo "nameserver $container_ip  # $name" | sudo tee -a /etc/resolvconf/resolv.conf.d/head >/dev/null
    # sudo sudo resolvconf -u
    pass


def resolver_del(ip, port):
    # if grep "$name" /etc/resolvconf/resolv.conf.d/head >/dev/null; then
    #     sudo sed -i "/  # $name/d" /etc/resolvconf/resolv.conf.d/head
    #     sudo sudo resolvconf -u
    # fi
    pass
