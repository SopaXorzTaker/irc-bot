import socket
import traceback
import logging

from threading import Thread
from ircbot.message import Message


class IRCClient(object):
    BUFFER_SIZE = 2048
    address = None
    nick = None
    realname = None
    command_hook = None
    command_prefix = None
    channels = None
    sock = None

    def _main_thread(self):
        logging.info("Connected")
        self.send(Message(None, "NICK", [self.nick]))
        self.send(Message(None, "USER", [self.nick, "0", "*", self.realname]))
        if self.channels:
            for channel in self.channels:
                self.send(Message(None, "JOIN", [channel]))
        while True:
            data = b""
            while True:
                recv = self.sock.recv(self.BUFFER_SIZE)
                if len(recv):
                    data += recv
                if len(recv) < self.BUFFER_SIZE:
                    break
            messages = data.split(b"\r\n")
            for msg in messages:
                if not len(msg):
                    continue
                try:
                    message = Message.parse(msg.decode("utf-8"))
                    logging.debug("Message received: %s", repr(message))
                except (IndexError, ValueError):
                    logging.warning("Unable to parse message: %s", traceback.format_exc())
                source = message.prefix.nickname
                if message.command in ["PRIVMSG", "NOTICE"]:
                    target = message.params[0]
                    text = message.params[1]
                    if text.startswith(self.command_prefix):
                        self.command_hook(self, source, target, text.split(" "))
                elif message.command == "PING":
                    self.send(Message(None, "PONG", message.params))

    def __init__(self, address, nick, realname="IRC Bot", command_hook=None, command_prefix="!", channels=None):
        self.address, self.nick, self.realname, self.command_hook, self.command_prefix, self.channels =\
            address, nick, realname, command_hook, command_prefix, channels

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        main_thread = Thread(target=self._main_thread)
        main_thread.start()
        # main_thread.join()

    def send(self, msg):
        logging.debug("Message sent: %s", repr(msg))
        tosend = msg.encode()
        self.sock.send(tosend)

    def privmsg(self, to, text):
        self.send(Message(None, "PRIVMSG", [to, text]))
