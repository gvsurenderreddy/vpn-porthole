#!/usr/bin/env python3

from VPNPorthole.docker import Image
from VPNPorthole.settings import Settings
from VPNPorthole.argparsetree import ArgParseTree


class Main(ArgParseTree):
    def args(self, parser):
        parser.add_argument("--settings", default=None)
        parser.add_argument("--proxy", default=None)


class Action(ArgParseTree):
    def args(self, parser):
        parser.add_argument("profile", help="Profile name")

    def run(self, args):
        settings = Settings(args.profile, args.settings, args.proxy)
        image = Image(settings)
        return self.go(image, args)


class Build(Action):
    def go(self, image, args):
        return image.build()


class Start(Action):
    def go(self, image, args):
        try:
            return image.start()
        except KeyboardInterrupt:
            return 1


class Stop(Action):
    def go(self, image, args):
        return image.stop()


class Purge(Action):
    def go(self, image, args):
        image.purge()



class Status(Action):
    def go(self, image, args):
        if image.status():
            print('RUNNING')
            return 0
        else:
            print('STOPPED')
            return 1

class Debug(Action):
    def go(self, image, args):
        return image.debug()


class Info(Action):
    def go(self, image, args):
        return image.info()


class Rm(Action):
    def go(self, image, args):
        return image.purge()


class List(ArgParseTree):
    def run(self, args):
        profiles = Settings.list_profiles(args.settings)
        for name, profile in profiles.items():
            settings = Settings(name, args.settings, args.proxy)
            image = Image(settings)
            if image.status():
                status = "RUNNING"
            else:
                status = "STOPPED"
            print("%s: %s@%s %s" % (name, profile['username'], profile['vpn'], status))


def main():
    m = Main()
    Build(m)
    Start(m)
    Stop(m)
    Status(m)
    Info(m)
    Debug(m)
    Rm(m)
    List(m)

    return m.main()


if __name__ == "__main__":
    exit(main())
