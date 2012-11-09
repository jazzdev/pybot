import socket, ssl

_irc = None

def connect(host, port=6667, nick='pybot', login='anonymous', password=None):
    global _irc
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    _irc = ssl.wrap_socket(s)
    _irc.connect(('irc', port))
    _irc.write('PASS %s\n' % password)
    _irc.write('NICK %s\n' % nick)
    _irc.write('USER %s 0 * :bot\n' % login)
    waitFor('You are connected')

def join(channel):
    global _irc
    _irc.write('JOIN %s\n' % channel)
    waitFor(':End')

def privmsg(channel, message):
    global _irc
    for line in message.split('\n'):
        _irc.write('PRIVMSG %s :%s\n' % (channel, line))

def quit():
    global _irc
    _irc.write('QUIT :bye\n')
    waitFor('Quit')
    _irc.close()
    _irc = None

def waitFor(string):
    global _irc
    buffer = ''
    while 1:
        data = _irc.read()
        if data == '':
            return
        print data,
        buffer += data
        if buffer.find(string) > -1:
            return
    raise Exception('Failed to find string: ' + string)

if __name__ == '__main__':
    main()
