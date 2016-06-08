import sys
import os
from configobj import ConfigObj, SimpleVal, get_extra_values
from validate import Validator
from pkg_resources import resource_stream

from VPNPorthole.ip import IPv4Subnet


class Settings(object):
    __proxy = None

    def __init__(self, profile, config=None, proxy=None):
        self.profile = profile
        if config is None:
            config = self.__default_settings_path()
            if not os.path.isdir(os.path.dirname(config)):
                os.makedirs(os.path.dirname(config))
            if not os.path.isfile(config):
                with open(config, 'w+b') as fh:
                    fh.write(self.__default_settings_content())
                print("* Configure vpn-porthole in: %s" % config)
                exit(1)

        self.__confobj = self.__get_confobj(config)
        try:
            self.__profile = self.__confobj['profile'][profile]
        except KeyError:
            print('! Profile "%s" not found' % profile, file=sys.stderr)
            exit(1)
        if proxy:
            self.__proxy = self.__confobj['proxy'][proxy]

    @property
    def proxy(self):
        if not self.__proxy:
            return None
        return self.__proxy['http_proxy']

    @property
    def username(self):
        return self.__profile['username']

    @property
    def password(self):
        pwd = self.__profile['password']
        if not pwd:
            import getpass
            pwd = getpass.getpass('')
        return pwd

    @property
    def vpn(self):
        return self.__profile['vpn']

    @property
    def subnets(self):
        return [IPv4Subnet(k)
                for k, v in self.__profile['subnets'].items()
                if v is True]

    @classmethod
    def __default_settings_path(cls):
        return os.path.expanduser('~/.config/vpn-porthole/settings.conf')

    @classmethod
    def __default_settings_content(cls):
        return resource_stream("VPNPorthole", "resources/settings.conf.example").read()

    @classmethod
    def list_profiles(cls, config):
        config = config or cls.__default_settings_path()
        confobj = cls.__get_confobj(config)
        return {p: v for p, v in confobj['profile'].items()}

    @classmethod
    def __get_confobj(cls, config):
        spec_lines = resource_stream("VPNPorthole", "resources/settings.spec").readlines()

        confobj = ConfigObj(config, configspec=spec_lines, raise_errors=True)
        result = confobj.validate(Validator())
        if result is not True:
            #print(result)
            pass
        extra = get_extra_values(confobj)
        if extra:
            #print(extra)
            pass
        #print (confobj)
        return confobj
