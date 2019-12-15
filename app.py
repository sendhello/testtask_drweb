# /usr/bin/python

from database import Database


class App(object):
    def __init__(self):
        self._db = Database()

    @staticmethod
    def analysis_line(line):
        args = line.strip(' ').split(' ')
        command = args.pop(0).lower()
        return command, args

    def run(self):
        while True:
            try:
                line = raw_input()
                if not line:
                    continue
                command, args = self.analysis_line(line)
                act = getattr(self._db, command)
                response = act(args)
                if response is not None:
                    print response

            except IndexError:
                print 'Few arguments'
            except AttributeError:
                print 'Command not found'
                continue
            except EOFError:
                exit()
