from ircbot.prefix import Prefix


class Message(object):
    prefix = None
    command = None
    params = None

    def __init__(self, prefix=None, command=None, params=None):
        self.prefix, self.command, self.params = prefix, command, params

    @staticmethod
    def parse(msg):
        """
        Parses the message
        :param msg: The raw message
        :type msg str
        :return: The parsed message
        """
        prefix_str = ""
        # command = ""
        params = []

        parts = msg.split(" ")
        if parts[0].startswith(":"):
            prefix_str = parts[0][1:]
            command = parts[1]
            remaining = parts[2:]
        else:
            command = parts[0]
            remaining = parts[1:]

        prefix = Prefix.parse(prefix_str)

        for i, part in enumerate(remaining):
            if part.startswith(":"):
                param = " ".join(remaining[i:])[1:]  # skip the colon
                params.append(param)
                break
            else:
                params.append(part)
        return Message(prefix, command, params)

    def encode(self):
        msg = (self.prefix.encode() + b" ").decode() if self.prefix else ""
        msg += self.command
        for param in self.params:
            if not (" " in param):
                msg += " " + param
            else:
                msg += " " + ":" + param
        return msg.encode("utf-8") + b"\r\n"

    def __repr__(self):
        return "%s <prefix=%s, command=%s, params=%s>" % (self.__class__.__name__, self.prefix, self.command,
                                                          str(self.params))