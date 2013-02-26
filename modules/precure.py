import json
import random
from datetime import datetime
from time import sleep
from plugins import IrcModule

class Precure(IrcModule):
    irc = None
    data = None
    last_run = None

    def __init__(self, irc):
        self.irc = irc
        self.load_json()

    def load_json(self):
        try:
            self.data = json.loads(open("modules/precure.json").read())
            for ending in self.data['endings']:
                print "Precure '%s': %s endings." % (ending['intro'], len(ending['endings']))
        except Exception as e:
            print "Error loading precure json: %s" % e
            raise

    def supports(self, channel, user, message):
        if (message.startswith("!precure")):
            return True
        if (message.startswith("!reload precure")):
            return True

    def on_message(self, channel, user, message):
        if (message.startswith("!reload precure")):
            self.load_json()
            return
        if self.last_run != None:
            if (datetime.now() - self.last_run).seconds // 60 < 2:
                return
        self.last_run = datetime.now()
        if message.startswith("!precure"):
            return self.send_ending(channel, user, message)
        self.irc.send_message(channel, "%s: Please try !precure again later." % user)

    def send_ending(self, channel, user, message):
        ending = self.data['endings'][random.randint(0, len(self.data['endings']) - 1))]
        print ending['intro']
        self.send_message(channel, ending['intro'], user)
        sleep(5)
        story = ending['endings'][random.randint(0, len(ending['endings']) - 1)]
        for line in story:
            self.send_message(channel, line, user)
            sleep(5)

    def send_message(self, channel, message, user):
        self.irc.send_message(channel, message.replace("{nick}", user))

    def name(self):
        return "Precure"

    def version(self):
        return "0.0.8"