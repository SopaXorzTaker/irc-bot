
class Prefix(object):
    servername = None
    nickname = None
    username = None
    host = None

    def __init__(self, servername=None, nickname=None, username=None, host=None):
        self.servername, self.nickname, self.username, self.host = servername, nickname, \
            username, host

    @staticmethod
    def parse(prefix):
        parts = prefix.split("!")
        if len(parts) == 1:
            return Prefix(parts[0])

        elif len(parts) == 2:
            nickname = parts[0]
            part_host = parts[1]
            user, host = part_host.split("@")
            return Prefix(None, nickname, user, host)

    def encode(self):
        if self.servername:
            return self.servername
        else:
            return "%s!%s@%s" % (self.nickname, self.username, self.host)

    def __repr__(self):
        return "%s <servername=%s, nickname=%s, username=%s, host=%s>" % (self.__class__.__name__, self.servername,
                                                                          self.nickname, self.username, self.host)