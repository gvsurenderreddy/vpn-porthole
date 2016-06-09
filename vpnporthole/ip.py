from functools import reduce


class IPv4Address(object):
    def __init__(self, addr):
        if isinstance(addr, IPv4Address):
            self._raw = addr._raw
        elif isinstance(addr, str):
            self._raw = ip_to_int(addr)
        elif isinstance(addr, int):
            self._raw = addr
        else:
            raise ValueError('Can\'t convert "%s" to IPv4Address' % repr(addr))

    @property
    def int(self):
        return self._raw

    def __str__(self):
        return int_to_ip(self._raw)

    def __repr__(self):
        return '<IPv4Address %s>' % int_to_ip(self._raw)

    def __lt__(self, other):
        return self._raw < other._raw

    def __eq__(self, other):
        return self._raw == other._raw


class IPv4Subnet(object):
    def __init__(self, cidr):
        base, size = cidr.split('/', 1)
        self._size = int(size)
        base = self.__mask(IPv4Address(base).int, self._size)
        self._ip = IPv4Address(base)

    @staticmethod
    def __mask(addr, size):
        mask = 0xFFFFFFFF << (32 - size)
        assert isinstance(addr, int)
        return addr & mask

    def __contains__(self, ip_addr):
        addr = IPv4Address(ip_addr)
        return self.__mask(addr.int, self._size) == self.__mask(self._ip.int, self._size)

    def __getitem__(self, item):
        i = int(item)
        if i >= 0:
            return IPv4Address(self._ip.int + i)
        else:
            mask = 0xFFFFFFFF >> (self._size)
            raw = self._ip.int | mask
            return IPv4Address(raw + i + 1)

    def __str__(self):
        return '%s/%s' % (self._ip, self._size)

    def __repr__(self):
        return '<IPv4Address %s>' % self.__str__()


def ip_to_int(addr):
    fields = addr.split('.')
    assert len(fields) == 4
    assert all([int(x) >= 0 and int(x) <= 255 for x in fields])
    return reduce(lambda x, y: x * 0x100 + int(y), fields, 0)


def int_to_ip(raw):
    addr = []
    for _ in range(4):
        addr.append(str(raw % 0x100))
        raw //= 0x100

    assert raw == 0
    return '.'.join(reversed(addr))
