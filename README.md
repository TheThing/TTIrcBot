TTIrcBot
========

TheThing's personal IRC bot

## How to install

 virtualenv --no-site-packages env
 source env/bin/activate

## How to run

### Direct

    # python
    >>> from bot import *
    >>> bot = IrcBot('irc.rizon.net', 6667)
    >>> bot.load_modules()
    >>> bot.connect('bot-name', 'MyBot', 'BotNickServPassword')
    >>> bot.run(["#my-channel"])

### Alternatively

Create a file called run.py and insert the above lines into it.

Then type:

 # python run.py

## License

All vode Licensed under the WTFPL 2.0
