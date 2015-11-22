import logging
import random
import socket
import time


logger = logging.getLogger(__name__)


class Connection(object):
    def __init__(self, settings):
        self.host, self.port = settings['host'], settings['port']
        self.connection = None
        self.channel, self.nick = settings['channel'], settings['nick']
        self.knocking = False

    def _write(self, text):
        self.connection.send(('%s\r\n' % text).encode())

    def connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.host, self.port))
        self._write('NICK %s' % self.nick)
        self._write('USER %s 8 * :%s' % (self.nick, self.nick))
        self.join()

    def join(self):
        self._write('JOIN %s' % self.channel)

    def pong(self, data):
        if data.find('PING') != -1:
            self._write('PONG %s' % data.split()[1])

    def quit(self, msg):
        self._write('QUIT :%s' % msg)
        self.connection.close()

    def message(self, text):
        self._write('PRIVMSG %s :%s' % (self.channel, text))

    def _knock(self):
        self._write('KNOCK %s' % self.channel)

    def knock(self, data):
        if data[-6:-2] == '(+i)' and self.knocking is False:
            self._knock()
            self.knocking = True
        if 'INVITE' in data:
            self.join()

    def read(self):
        data = self.receive().decode()
        # check for ping
        self.pong(data)
        user, message = None, None
        if data.find('PRIVMSG') != -1:
            user = data.split('!')[0].replace(':', '')
            message = data.split()[3:]
            message[0] = message[0][1:]
        return user, message

    def receive(self):
        return self.connection.recv(4096)


class ConnectionManager:
    def __init__(self, *args, **kwargs):
        assert len(args) > 0
        self.connection = args[0]

    def __enter__(self):
        self.connection.connect()
        self.connection.join()
        return self.connection

    def __exit__(self, *args, **kwargs):
        messages = [
            "Someone's stabbing me!!!",
            "I'm being murdered!",
            "Later, cunts.",
            "FFFFFUUUUUUCCCCCKKKKKK!!!!",
        ]
        self.connection.quit(random.choice(messages))
        return False
