# Chess-Bot By Davi0k
Chess-Bot is a [Discord](https://discordapp.com/) BOT used to play chess directly in text channels against other users. It includes also a graphical chess board and a simple statistics database for each player.

You can find it available here: [https://top.gg/bot/685895842430713913](https://top.gg/bot/685895842430713913)

## Starting the BOT
First, create a copy of `.env.example` and  install all of the needed PIP packages using the `requirements.txt` file:
```
cp .env.example .env
python -m pip install -r requirements.txt
```
Now, open the newly created `.env` file and set-up these environment variables:

`TOKEN`: The token of the BOT generated in [the developer portal](https://discordapp.com/developers/applications);

`DATABASE_HOST`: The hostname of the dedicated MongoDB database;
`DATABASE_PORT`: The port of the dedicated  MongoDB database;
`DATABASE_NAME`: The name that will be used for the database;

Finally, you can run the BOT very easy:
```
python bot.py
```

## Commands available within Chess-Bot
Several commands are available in Chess-Bot. They are divided into two categories: Main and Chess.

### Main Category:
The Main Category contains some useful and utility-based commands to simplify and extend  the user experience.
* `!rnd|random [minimum - optional] [maximum - optional]`: Draws a random number between `minimum` and `maximum`. If `minimum` is omitted, it will be set to 0. If `minimum` and `maximum` are omitted, a number from 0 to 100 will be drawn;
* `!coin|flip|coinflip`: Flips a coin and returns the result;
* `!whois|about|info [user - optional]`: Shows different kind of informations about a specified `user`. If `user` is omitted, the context user info will be shown.

### Chess Category:
The Chess Category contains all the main and unique commands of Chess-Bot to be able to play chess against your friends, or perhaps your enemies...
* `!chess new|create|invite [user]`: Sends an invite for a new match to a specified `user`;
* `!chess accept [user]`: Accepts an invite sent by a specified `user` and starts a new match;
* `!chess decline [user]`: Declines an invite sent by a specified `user` and deletes it;
* `!chess invites`: Shows every out-coming and in-coming invites for the context user;
* `!chess move|execute [initial] [final]`: Takes an `initial` and a `final` chess coordinate and executes a move in the current match;
* `!chess show|chessboard`: Shows the current match chessboard disposition;
* `!chess surrend`: Surrend and lost the current match;
* `!chess statistics|stats [user - optional]`: Shows the statistics of a Discord user who played at least one match. If `user` is omitted, the context user stats will be shown.

## Some screen-shots about the BOT
![](https://i.ibb.co/cNm5MBG/Help.png)

![](https://i.ibb.co/GQc35mw/Commands.png)

![](https://i.ibb.co/BB4Gp9K/Start.png)

![](https://i.ibb.co/gd1Q39H/Move.png)