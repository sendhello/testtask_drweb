# /usr/bin/python


class Database(object):
    def __init__(self):
        self._db = {}
        self.transaction = 0

    def _set_values_collection(self, key, key_values_collection):
        if key_values_collection not in self._db:
            self._db[key_values_collection] = {}
        values_collection = self._db[key_values_collection]

        if self.transaction not in values_collection:
            if self.transaction - 1 in values_collection:
                values_collection[self.transaction] = values_collection[self.transaction - 1].copy()
            else:
                values_collection[self.transaction] = set()
        values_collection[self.transaction].add(key)

    def _delete_old_values(self, key):
        if key not in self._db:
            return None

        version = self.transaction
        element = 'val:{}'.format(self.get([key, ]))
        while version >= 0:
            if version not in self._db[element]:
                version -= 1
                continue
            if key in self._db[element][version]:
                self._db[element][version].remove(key)
                if not self._db[element][version] and not self.transaction:
                    del self._db[element][version]
                if not self._db[element]:
                    del self._db[element]
                return True
            version -= 1

    def get(self, args):
        key = args[0]
        response = self._db.get(key)
        if not response:
            return 'NULL'

        version = self.transaction
        while version:
            if version not in self._db[key]:
                version -= 1
                continue
            break
        return self._db[key][version]

    def set(self, args):
        key = args[0]
        if key[:4] == 'val:':
            return 'Cannot be user prefix "val:"'

        key_values_collection = 'val:{}'.format(args[1])

        self._delete_old_values(key)

        if key not in self._db:
            self._db[key] = {}
        self._db[key][self.transaction] = args[1]

        self._set_values_collection(key, key_values_collection)
        return ''

    def unset(self, args):
        key = args[0]
        if key not in self._db:
            return None

        self._delete_old_values(key)

        if self.transaction:
            self._db[key][self.transaction] = None
        else:
            del self._db[key]
        return ''

    def counts(self, args):
        key = 'val:{}'.format(args[0])
        element = self.get([key, ])
        return len(element)

    def find(self, args):
        key = 'val:{}'.format(args[0])
        element = self.get([key, ])
        if element == 'NULL':
            return ''
        return ', '.join(element)

    def begin(self, args):
        self.transaction += 1
        return ''

    def rollback(self, args):
        if not self.transaction:
            return 'Transactions not found'

        for element in self._db.keys():
            try:
                del self._db[element][self.transaction]
            except KeyError:
                pass

            if not self._db[element]:
                del self._db[element]

        self.transaction -= 1
        return ''

    def commit(self, args):
        if not self.transaction:
            return 'Transactions not found'

        for element in self._db.keys():
            version = self.transaction
            while version:
                if version not in self._db[element]:
                    version -= 1
                    continue

                value = self._db[element].get(version)
                if value:
                    self._db[element] = {0: value}
                else:
                    del self._db[element]
                break

        self.transaction = 0
        return ''

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

            except IndexError:
                print 'Few arguments'
            except AttributeError:
                print 'Command not found'
                continue
            except EOFError:
                exit()


if __name__ == "__main__":
    app = App()
    app.run()
