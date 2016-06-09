import sys
import subprocess

from vpnporthole.system.shell import popen
from vpnporthole.system.shell import Pexpect

docker_bin = subprocess.check_output('which docker', shell=True).decode('utf-8').rstrip()

class Docker(object):
    def __init__(self):
        # print(self.info())
        pass

    def info(self):
        args = [docker_bin, 'images']
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        info_lines = []
        for line in p.stdout:
            info_lines.append(line.decode('utf-8').rstrip())
        return info_lines

    def list_images(self):
        args = [docker_bin, 'images']
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        headers = None
        images = []
        for line in p.stdout:
            line = line.decode('utf-8')
            if not headers:
                headers = line.split()
            else:
                fields = line.split()
                entry = {h: f for h, f in zip(headers, fields)}
                images.append(entry['REPOSITORY'])

        p.wait()
        return images

    def list_containers(self):
        headers = ['ID', 'Image', 'Status']
        format = '{{.%s}}' % '}}:{{.'.join(headers)
        args = [docker_bin, 'ps', '--all', '--format', format]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        table = []
        for line in p.stdout:
            line = line.decode('utf-8').rstrip()
            fields = line.split(':')
            table.append({h: f for h, f in zip(headers, fields)})

        p.wait()
        ret = {}
        for entry in table:
            ret[entry['ID']] = {'Running': entry['Status'].startswith('Up '), 'Image': entry['Image']}
        return ret

    def rm(self, containers):
        if not containers:
            return
        args = [docker_bin, 'rm']
        args.extend(containers)
        p = popen(args, stdout=subprocess.PIPE)
        p.wait()

    def rmi(self, images):
        if not images:
            return
        args = [docker_bin, 'rmi']
        args.extend(images)
        p = popen(args, stdout=subprocess.PIPE)
        p.wait()

    def build(self, *vargs):
        args = [docker_bin, 'build']
        args.extend(vargs)
        p = popen(args, stdout=subprocess.PIPE)
        for line in p.stdout:
            line = line.decode('utf-8')
            sys.stdout.write(line)
        p.wait()

        if p.returncode == 0:
            image = line.split()[2]
            return image

    def stop(self, containers):
        if not containers:
            return
        args = [docker_bin, 'stop']
        args.extend(containers)
        p = popen(args, stdout=subprocess.PIPE)
        p.wait()

    def shell(self, container):
        if not container:
            return
        args = [docker_bin, 'exec', '-it', container, '/bin/bash']
        p = popen(args)
        p.wait()

    def inspect(self, container, values):
        if not container:
            return
        format = '{{.%s}}' % '}}:{{.'.join(values)

        args = [docker_bin, 'inspect', '--format', format, container]
        p = popen(args, stdout=subprocess.PIPE)
        table = []
        for line in p.stdout:
            line = line.decode('utf-8').rstrip()
            fields = line.split(':')
            table.append({h: f for h, f in zip(values, fields)})

        p.wait()
        return table[0]

    def run_with_pexpect(self, *vargs):
        args = [docker_bin, 'run']
        args.extend(vargs)

        pe = Pexpect(args)

        return pe

    def exec(self, container, *vargs):
        args = [docker_bin, 'exec', '-it', container]
        args.extend(vargs)
        p = popen(args)
        p.wait()

    def machine_ssh(self, args):
        args = ['/usr/local/bin/docker-machine', 'ssh', 'foo']
        args.extend(args)
        p = popen(args)
        p.wait()
