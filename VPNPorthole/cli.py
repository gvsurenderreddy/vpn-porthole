#!/usr/bin/env python3
from vpnporthole.image import Image
from vpnporthole.settings import Settings
from vpnporthole.argparsetree import ArgParseTree


class Main(ArgParseTree):
    """

    """
    def args(self, parser):
        parser.add_argument("--settings", default=None, help='Alternative settings file')
        parser.add_argument("--proxy", default=None, help="Selected proxy profile")


class Action(ArgParseTree):
    def args(self, parser):
        parser.add_argument("profile", help='Selected profile in the settings "all" can be used')

    def run(self, args):
        if args.profile == 'all':
            profiles = Settings.list_profiles(args.settings)
            for name, profile in profiles.items():
                self.settings = Settings(name, args.settings, args.proxy)
                image = Image(self.settings)
                return self.go(image, args)
        else:
            self.settings = Settings(args.profile, args.settings, args.proxy)
            image = Image(self.settings)
            return self.go(image, args)


class Build(Action):
    """\
    Build profile

    Build the docker image for this profile
    """
    def go(self, image, args):
        return image.build()


class Start(Action):
    """\
    Start profile

    Start the docker container for this profile, requires user to enter password none configured
    """
    def go(self, image, args):
        try:
            return image.start()
        except KeyboardInterrupt:
            return 1


class Stop(Action):
    """\
    Stop profile

    Stop the docker container for this profile
    """
    def go(self, image, args):
        return image.stop()


class Status(Action):
    """\
    Purge profile

    Determine if the docker container fo this image is running
    """
    def go(self, image, args):
        if image.status():
            status = 'RUNNING'
        else:
            status = 'STOPPED'
        print("%s: %s@%s %s" % (self.settings.profile, self.settings.username, self.settings.vpn, status))


class Debug(Action):
    def go(self, image, args):
        return image.debug()


class Info(Action):
    def go(self, image, args):
        return image.info()


class Rm(Action):
    """\
    Purge profile

    Remove any running/stopped containers and images for this profile
    """
    def go(self, image, args):
        return image.purge()


class Restart(Action):
    """\
    Purge profile

    Remove any running/stopped containers and images for this profile
    """
    def go(self, image, args):
        if image.status():
            image.stop()
            image.start()


def main():
    m = Main()
    Build(m)
    Start(m)
    Status(m)
    Stop(m)
    Restart(m)
    Info(m)
    Debug(m)
    Rm(m)

    try:
        return m.main()
    except KeyboardInterrupt:
        print('^C')
        return 3


if __name__ == "__main__":
    exit(main())
