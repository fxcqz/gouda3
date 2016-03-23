import logging
import random
import socket
import time

from gouda.models import Message


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

        # keep alive
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 300)
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 30)
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

        # connect
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
        # include gouda messages in db
        Message.create(name=self.nick, message=text)
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
        data = self.receive().decode('latin1')
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
        self.db = args[1]

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
            "I didn't like it here anyway.",
            "The cheese of the day is...",
        ]
        self.connection.quit(random.choice(messages))
        self.db.close()
        return False
