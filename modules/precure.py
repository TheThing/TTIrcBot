from plugins import IrcModule

class Precure(IrcModule):
	irc = None
	
	def __init__(self, irc):
		self.irc = irc

	def supports(self, channel, user, message):
		if (message.beginswith("!precure")):
			return True

	def on_message(self, channel, user, message):
		self.irc.send_message(channel, "%s: Please try !precure again later." % user)