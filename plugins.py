class IrcModule(object):

    def supports(self, channel, user, message):
        raise NotImplementedError('Not implemented')

    def on_message(self, channel, user, message):
        raise NotImplementedError('Not implemented')

    def name(self):
        raise NotImplementedError('Not implemented')

    def version(self):
        raise NotImplementedError('Not implemented')