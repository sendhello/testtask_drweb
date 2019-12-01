import redis


def GET(obj, args):
    response = obj.get(args[0])
    if not response:
        return 'NULL'
    return response


def SET(obj, args):
    obj.sadd('value:{}'.format(args[1]), args[0])
    obj.set(args[0], args[1])
    return ''


def UNSET(obj, args):
    value = 'value:{}'.format(obj.get(args[0]))
    obj.srem(value, args[0])
    obj.delete(args[0])
    return ''


def COUNTS(obj, args):
    return len(obj.smembers('value:{}'.format(args[0])))


def FIND(obj, args):
    return ', '.join(obj.smembers('value:{}'.format(args[0])))


def END(obj, args):
    exit()


functions = {
    'GET': GET,
    'SET': SET,
    'UNSET': UNSET,
    'COUNTS': COUNTS,
    'FIND': FIND,
    'END': END
}


def analysis_line(line):
    line_elements = line.strip(' ').split(' ')
    command = line_elements[0]
    args = line_elements[1:]
    return command, args


def transaction(db, transaction_lines):
    with db.pipeline() as pipe:
        pipe.multi()
        for command, args in transaction_lines:
            functions.get(command)(pipe, args)
        pipe.execute()


def run_transaction(db, transaction_lines):
    commands_level = []

    while transaction_lines:
        print transaction_lines
        line = transaction_lines.pop(0)
        command, args = analysis_line(line)

        if command == 'BEGIN':
            command = run_transaction(db, transaction_lines)
            if not command:
                continue
        if command == 'ROLLBACK':
            return None
        if command == 'COMMIT':
            transaction(db, commands_level)
            return command
        commands_level.append((command, args))


def run():
    db = redis.Redis()
    is_write_transaction = False
    transaction_lines = []
    level = 0
    while True:
        try:
            line = raw_input()
            command, args = analysis_line(line)

            if is_write_transaction:
                transaction_lines.append(line)
            if command == 'BEGIN' and not is_write_transaction:
                is_write_transaction = True
                continue
            if command == 'BEGIN':
                level += 1
            if command == 'COMMIT':
                is_write_transaction = False
                run_transaction(db, transaction_lines)
                transaction_lines = []
                print ''
                continue
            if command == 'ROLLBACK':
                if not level:
                    is_write_transaction = False
                    transaction_lines = []
                    print ''
                    continue
                level -= 1

            if not is_write_transaction:
                print functions.get(command)(db, args)
        except EOFError:
            exit()


if __name__ == "__main__":
    run()
