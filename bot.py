import socket
import sys
import pkgutil
from plugins import IrcModule

class IrcBot:
   network = 'irc.rizon.net'
   port = 6667
   irc = None
   nick = ""
   name = ""
   password = ""
   channels = []
   plugins = []

   def __init__(self, network, port):
      self.network = network
      self.port = port
      self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   def load_modules(self):
      modules = None
      for m in list(pkgutil.iter_modules(['modules'])):
         modules = __import__('modules.' + m[1])
         module = getattr(modules, m[1])
         for class_name in [x for x in dir(module) if not x.startswith("_")]:
            the_class = getattr(module, class_name)
            if issubclass(the_class, IrcModule) and the_class.__name__ != IrcModule.__name__:
               self.plugins.append(the_class(self))

   def connect(self, nick, name, password):
      self.nick = nick
      self.name = name
      self.password = password
      self.irc.connect(( self.network, self.port))
      self.debug(self.irc.recv(4096 ))
      self.irc.send("NICK %s\r\n" % self.nick )
      self.irc.send("USER %s %s %s :Python irc\r\n" % (self.name, self.name, self.name) )
      self.irc.send("PRIVMSG NickServ :GHOST Thing-kun %s\r\n" % self.password )
      self.irc.send("PRIVMSG NickServ :IDENTIFY %s\r\n" % self.password )

   def run(self, channels):
      self.channels = channels
      
      while True:
         data = self.irc.recv(4096 )
         for line in data.split('\r\n'):
            line = "%s\r\n" % line
            #self.debug(line)

            try:
               if len(line.split(':')) != 3:
                  continue

               meta = line.split(':')[1]
               channel = meta.split(' ')[2]

               if line.find("PRIVMSG") != -1:
                  message = line.split(':')[2]
                  user = meta.split(' ')[0].split('!')[0]
                  self.on_message(channel, user, message)
               if line.find("KICK") != -1:
                  self.irc.send("JOIN %s\r\n" % channel)
               if line.find("NOTICE") != -1 and line.find("Password accepted") != -1:
                  for c in self.channels:
                     self.irc.send("JOIN %s\r\n" % c)
                     self.send_message(c, "Greetings.")
            except Exception as e:
               print "=================== ERROR ==================="
               print e
               print "=================== ERROR ==================="

   def send_message(self, channel, message):
      self.irc.send("PRIVMSG %s :%s\r\n" %(channel, message) )

   def debug(self, data):
      sys.stdout.write(data)
      sys.stdout.flush()

   def on_message(self, channel, user, message):
      self.debug("%s: <%s> %s\r\n" % (channel, user, message))
      for p in self.plugins:
         if p.supports(channel, user, message):
            p.on_message(channel, user, message)
