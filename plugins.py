class IrcModule(object):

	def supports(channel, user, message):
		raise NotImplementedError('Not implemented')

	def on_message(channel, user, message):
		raise NotImplementedError('Not implemented')