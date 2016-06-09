import os
from vpnporthole.system.shell import popen
import subprocess


def docker_host():
    return True


# def route_get(subnet):
#     # local route=$(netstat -nr | grep $(echo "$1" | sed -e 's/\.0//g') | head -1 | awk '{print $1" "$2}')
#     # if [ -z "$route" ]; then
#     #     return
#     # fi
#     # while ! echo $route | grep "\..\../" >/dev/null; do
#     #     route=$(echo $route | sed -e 's/\//.0\//')
#     # done
#     # echo $route
#     pass

def local_cmd(args):
    p = popen(args)
    p.wait()


def host_ssh(args):
    machine = os.environ['DOCKER_MACHINE_NAME']

    base = ['docker-machine', 'ssh', machine]
    base.extend(args)
    local_cmd(base)


def host_ip():
    machine = os.environ['DOCKER_MACHINE_NAME']

    args = ['docker-machine', 'ip', machine]
    p = popen(args, stdout=subprocess.PIPE)
    for line in p.stdout:
        pass
    p.wait()

    return line.strip().decode('utf-8')


def route_add(subnets, ip):

    host_ssh(['/usr/bin/sudo', '/usr/local/sbin/iptables',
              '-t', 'nat',
              '-A', 'POSTROUTING',
              '-o', 'docker0',
              '-j', 'MASQUERADE'])

    host_ssh(['/usr/bin/sudo', '/usr/local/sbin/iptables',
              '-A', 'FORWARD',
              '-i', 'eth1',
              '-j', 'ACCEPT'])

    for subnet in subnets:
        host_ssh(['/usr/bin/sudo', '/usr/local/sbin/ip', 'route', 'add', str(subnet), 'via', ip])

        local_cmd(['/usr/bin/sudo', 'route', '-n', 'add', str(subnet), host_ip()])
    pass


def route_del(subnets):
    for subnet in subnets:
        local_cmd(['/usr/bin/sudo', 'route', '-n', 'delete', str(subnet)])

        host_ssh(['/usr/bin/sudo', '/usr/local/sbin/ip', 'route', 'del', str(subnet)])

    # if route_get(subnet):
    #     # sudo route -n delete $via &>/dev/null
    #     pass


def resolver_add(ip, port):
    # networksetup -getdnsservers 'Wi-Fi' 8.8.8.8 8.8.4.4
    # networksetup -setdnsservers 'Wi-Fi'
    pass


def resolver_del(ip, port):
    pass
