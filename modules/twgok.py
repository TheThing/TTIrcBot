from plugins import IrcModule

class TWGOK(IrcModule):
    irc = None

    def __init__(self, irc):
        self.irc = irc

    def supports(self, channel, user, message):
        if (message.startswith("!twgok")):
            return True

    def on_message(self, channel, user, message):
        self.irc.send_message(channel, "%s: Please try again later." % user)

    def name(self):
        return "TWGOK"

    def version(self):
        return "0.0.2"