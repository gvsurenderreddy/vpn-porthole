import sys
from argparse import ArgumentParser


class ArgParseTree(object):
    """
    Facilitates building a CLI argument parser with sub commands and options.

    Example:
        $ script [--fish] foo <bar>
        $ script [--fish] spam [--eggs <EGGS>]

    >>> from argparsetree import ArgParseTree
    ...
    >>> class Main(ArgParseTree):
    ...     def args(self, parser):
    ...         parser.add_argument("--fish", default=False, action='store_true')
    ...
    >>> class Foo(ArgParseTree):
    ...     def args(self, parser):
    ...         parser.add_argument("bar")
    ...
    ...     def run(self, args):
    ...         print("FOO: %s (%s)" % (args.bar, args.fish))
    ...         return 3
    ...
    >>> class Spam(ArgParseTree):
    ...     def args(self, parser):
    ...         parser.add_argument("--eggs", default=None)
    ...
    ...     def run(self, args):
    ...         print("SPAM: %s (%s)" % (args.eggs, args.fish))
    ...         return 4
    ...
    >>> m = Main()
    >>> Foo(m)  # doctest: +ELLIPSIS
    <...>
    >>> Spam(m)  # doctest: +ELLIPSIS
    <...>
    >>> m.main(['foo', "BAR"])
    FOO: BAR (False)
    3
    >>> m.main(['--fish', 'spam', '--eggs', "green"])
    SPAM: green (True)
    4
    """
    usage = None
    name = None
    _parent = None
    _children = None
    _parser = None
    _subparser = None

    def __init__(self, parent=None):
        if parent:
            self._parent = parent
            if parent._children is None:
                parent._children = []
            parent._children.append(self)

    def _setup_args(self):
        if self._parent is None:
            self._parser = ArgumentParser(usage=self.usage)
            try:
                self.args(self._parser)
            except AttributeError:
                pass

        if self._children:
            self._subparser = self._parser.add_subparsers()

        if self._parent:
            self.name = self.name or self.__class__.__name__.lower()
            self._parser = self._parent._subparser.add_parser(self.name)
            try:
                self.args(self._parser)
            except AttributeError:
                pass

        if self._children:
            for child in self._children:
                child._setup_args()
        else:
            run = getattr(self, 'run', None)
            if run:
                self._parser.set_defaults(_run=run)

    def main(self, argv=None):
        self._setup_args()

        if argv is None:
            argv = sys.argv[1:]

        args = self._parser.parse_args(argv)
        return args._run(args)


if __name__ == "__main__":
    import doctest
    doctest.testmod()


