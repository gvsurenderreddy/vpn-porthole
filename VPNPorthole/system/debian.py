
def docker_host():
    return False

def route_get(subnet):
    # ip route list |  grep "$1" | cut -d' ' -f 1-3
    pass

def route_add(subnet, ip):
    # sudo ip route add $1 via $2
    pass

def route_del(subnet):
    if route_get(subnet):
        # sudo ip route del $via 2>/dev/null || true
        pass

def resolver_add(ip):
    # echo "nameserver $container_ip  # $name" | sudo tee -a /etc/resolvconf/resolv.conf.d/head >/dev/null
    # sudo sudo resolvconf -u
    pass

def resolver_del(ip):
    # if grep "$name" /etc/resolvconf/resolv.conf.d/head >/dev/null; then
    #     sudo sed -i "/  # $name/d" /etc/resolvconf/resolv.conf.d/head
    #     sudo sudo resolvconf -u
    # fi
    pass

