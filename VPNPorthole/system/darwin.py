
def docker_host():
    return True

def host_ssh(cmd):
    pass

def route_get(subnet):
    # local route=$(netstat -nr | grep $(echo "$1" | sed -e 's/\.0//g') | head -1 | awk '{print $1" "$2}')
    # if [ -z "$route" ]; then
    #     return
    # fi
    # while ! echo $route | grep "\..\../" >/dev/null; do
    #     route=$(echo $route | sed -e 's/\//.0\//')
    # done
    # echo $route
    pass

def route_add(subnet, ip):

    host_ssh('/usr/bin/sudo ip route add %s via %s' % (subnet, ip))
    host_ssh('/usr/bin/sudo iptables -t nat -A POSTROUTING -o docker0 -j MASQUERADE')
    host_ssh('/usr/bin/sudo iptables -A FORWARD -i eth1 -j ACCEPT')

    os.system('/usr/bin/sudo route -n add %s %s' % (subnet, host_ip()))
    pass

def route_del(subnet):
    os.system('/usr/bin/sudo route -n delete %s' % (subnet,))

    host_ssh('/usr/bin/sudo ip route del %s' % (subnet,))

    # if route_get(subnet):
    #     # sudo route -n delete $via &>/dev/null
    #     pass

def resolver_add(ip):
    # networksetup -getdnsservers 'Wi-Fi' 8.8.8.8 8.8.4.4
    # networksetup -setdnsservers 'Wi-Fi'
    pass

def resolver_del(ip):
    pass

