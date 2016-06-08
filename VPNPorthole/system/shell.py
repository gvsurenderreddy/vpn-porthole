import sys
import subprocess

from pexpect import spawn as pe_spawn, TIMEOUT, EOF


def args_to_string(args):
    def q(s):
        if not isinstance(s, str):
            s = str(s)
        if '"' in s:
            s = s.replace('"', '\\"')
        if '"' in s or ' ' in s:
            s = '"%s"' % s
            return s
        return s

    return ' '.join([q(s) for s in args])


def popen(args, *vargs, **kwargs):

    print('$ %s' % args_to_string(args))
    try:
        return subprocess.Popen(args, *vargs, **kwargs)
    except IOError as e:
        print('Error running command: %s\n%s' % (str, e))
        raise


class Pexpect(pe_spawn):

    class Out(object):
        ignore = 0

        def write(self, b):
            st = b.decode("utf-8")
            for line in st.splitlines(True):
                if line.startswith(('Password', 'Username')):
                    self.ignore += 1
                elif self.ignore > 0:
                    self.ignore -= 1
                    return
                sys.stdout.write('%s' % line)

        def flush(self):
            sys.stdout.flush()

    def __init__(self, args):
        cmd = args_to_string(args)
        print('$ %s' % cmd)

        super(Pexpect, self).__init__(cmd)
        self.logfile = self.Out()

    def expect(self, pattern, **kwargs):
        pattern.insert(0, EOF)
        pattern.insert(1, TIMEOUT)

        i = super(Pexpect, self).expect(pattern, **kwargs)

        if i < 2:
            exit(1)
        return i - 2
