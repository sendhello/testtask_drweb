# /usr/bin/python


class Database(object):
    def __init__(self):
        self._db = {}

    def get(self, args):
        response = self._db.get(args[0])
        if not response:
            return 'NULL'
        return response

    def set(self, args):
        value_key = 'val:{}'.format(args[1])
        if value_key not in self._db:
            self._db[value_key] = set()
        self._db[value_key].add(args[0])
        self._db[args[0]] = args[1]
        return ''

    def unset(self, args):
        key = args[0]
        if key not in self._db:
            return None
        value_key = 'val:{}'.format(self._db.get(key))
        self._db.get(value_key).remove(key)
        del self._db[key]
        return ''

    def counts(self, args):
        return len(self._db.get('val:{}'.format(args[0])))

    def find(self, args):
        return ', '.join(self._db.get('val:{}'.format(args[0])))

    def end(self, args):
        exit()


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
                print act(args)
            except EOFError:
                exit()


if __name__ == "__main__":
    app = App()
    app.run()
