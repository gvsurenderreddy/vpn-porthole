import os
from pkg_resources import resource_stream

from VPNPorthole.system import TmpDir, Docker, docker_host


Dockerfile_tmpl = resource_stream("VPNPorthole", "resources/Dockerfile.tmpl").read().decode("utf-8")
connect_sh_tmpl = resource_stream("VPNPorthole", "resources/connect.sh.tmpl").read().decode("utf-8")
post_connect_sh_tmpl = resource_stream("VPNPorthole", "resources/post_connect.sh.tmpl").read().decode("utf-8")


class Image(object):
    __container = None

    def __init__(self, settings):
        self.__settings = settings
        self.__docker = Docker()

    def _local_user(self):
        return os.environ['USER']

    def _tag(self):
        return "vpnp_%s_%s" % (self._local_user(), self.__settings.profile)

    def _prefix(self):
        return self._tag() + '_'

    def _ctx(self):
        ctx = {
            'gid': os.getgid(),
            'group': 'user',
            'uid': os.getuid(),
            'user': 'user',
        }
        return ctx

    def build(self):

        ctx = self._ctx()
        tag = self._tag()

        http_proxy = self.__settings.proxy

        if http_proxy:
            ctx['proxy'] = "RUN echo 'Acquire::http::proxy \"%(http_proxy)s\";' > /etc/apt/apt.conf" % \
                           {'http_proxy': http_proxy}
        else:
            ctx['proxy'] = ''

        ctx['vpn'] = self.__settings.vpn

        with TmpDir() as tmp:

            Dockerfile = os.path.join(tmp.path, 'Dockerfile')
            with open(Dockerfile, 'w') as fh:
                fh.write(Dockerfile_tmpl % ctx)

            def add_script(tmpl, name):
                script = os.path.join(tmp.path, name)
                with open(script, 'w') as fh:
                    fh.write(tmpl % ctx)

                os.chmod(script, 0o744)
                os.utime(script, (0, 0))

            add_script(vpn_script_tmpl, 'vpn')
            add_script(connect_sh_tmpl, 'connect')
            add_script(post_connect_sh_tmpl, 'post_connect')

            image = self.__docker.build('--tag', tag, '--rm=true', tmp.path)
            return image

    def start(self):

        if self.status():
            print("Already running")
            return 1

        if not self._images():
            self.build()

        ctx = self._ctx()
        image = self._tag()
        tag = self._tag()

        if tag:
            pass

        dnsmasqport = 53

        args = ['--rm', '-it', #'--name', tag,
                '--privileged']
        if docker_host():
            args.extend(['-p', '%d:53' % dnsmasqport])
        args.extend([image,
                    '/home/%(user)s/connect' % ctx, self.__settings.vpn])

        p = self.__docker.run_with_pexpect(*args)

        try:
            old_pwd = None
            while True:
                i = p.expect(['Username:', 'Password:', 'Established', 'Login failed.'])
                if i == 0:
                    p.sendline(self.__settings.username)
                if i == 1:
                    pwd = self.__settings.password
                    if old_pwd == pwd:  # Prevent lockout
                        print(" <password was same as previous attempt> ")
                        p.send(chr(3))
                        p.wait()
                        return 1
                    old_pwd = pwd
                    p.sendline('%s' % pwd)
                if i == 2:
                    break
                if i == 3:
                    pass
        except KeyboardInterrupt:
            p.send(chr(3))
            p.wait()
            raise

        fields = ['NetworkSettings.IPAddress']
        info = self.__docker.inspect(self._container(), fields)
        for k, v in info.items():
            print("- %s: %s" % (k, v))

        args = ['/home/%(user)s/post_connect' % ctx, '54']
        self.__docker.exec(self._container(), *args)

    def add_routes(self):
        pass

    def del_routes(self):
        pass

    def status(self):
        containers = self._containers()

        return any(containers.values())

    def _images(self):
        tag = self._tag()

        all_images = self.__docker.list_images()

        return [i for i in all_images if i == tag]

    def _containers(self):
        tag = self._tag()
        all_containers = self.__docker.list_containers()
        containers = {}
        for id, container in all_containers.items():
            if container['Image'] == tag:
                containers[id] = container['Running']
        return containers

    def _container(self):
        if self.__container:
            return self.__container
        containers = self._containers()
        running = [k for k, v in containers.items() if v is True]
        if not running:
            print("Not running")
            return None
        if len(running) > 1:
            print('WARNING: there are more than one containers: %s' % running)
        self.__container = running[0]
        return running[0]

    def stop(self):
        containers = self._containers()
        running = [k for k, v in containers.items() if v is True]
        self.__docker.stop(running)

        containers = self._containers()
        stopped = [k for k, v in containers.items() if v is False]
        self.__docker.rm(stopped)

    def purge(self):
        self.stop()
        images = self._images()
        self.__docker.rmi(images)

    def debug(self):
        self.__docker.shell(self._container())

    def info(self):
        fields = ['NetworkSettings.IPAddress']
        info = self.__docker.inspect(self._container(), fields)
        print(info)