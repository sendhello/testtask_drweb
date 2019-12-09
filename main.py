# /usr/bin/python

class Database(object):
    def __init__(self):
        self.db = {}

    def get(self, args):
        response = self.db.get(args[0])
        if not response:
            return 'NULL'
        return response

    def set(self, args):
        value_key = 'value:{}'.format(args[1])
        if value_key not in self.db:
            self.db[value_key] = set()
        self.db[value_key].add(args[0])
        self.db[args[0]] = args[1]
        return ''

    def unset(self, args):
        key = args[0]
        if key not in self.db:
            return None
        value_key = 'value:{}'.format(self.db.get(key))
        del(self.db, key)
        self.db.get(value_key).pop(key)
        return ''

    def counts(self, args):
        return len(self.db.get('value:{}'.format(args[0])))

    def find(self, args):
        return ', '.join(self.db.get('value:{}'.format(args[0])))

    def end(self, args):
        exit()
