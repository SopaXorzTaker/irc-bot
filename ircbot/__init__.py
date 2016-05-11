from .client import *

if __name__ == "__main__":
    import logging
    from .client import IRCClient
    from .message import Message


    def hook(self, source, target, args):
        command = args[0]
        if command == "!hello":
            self.send(Message(None, "PRIVMSG", [source, "Hello %s" % source]))


    logging.basicConfig(level=logging.DEBUG)

    irc = IRCClient(("chat.freenode.net", 6667), "TestBot12345", command_hook=hook)
    irc.start()