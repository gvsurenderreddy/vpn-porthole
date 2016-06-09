
[proxy]
    [[__many__]]
        http_proxy = string(default='')

[profile]
    [[__many__]]
        username = string()
        password = string(default='')
        vpn = string()
        [[[subnets]]]
            ___many___ = boolean()