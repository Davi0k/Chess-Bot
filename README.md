# Chess-Bot By Davi0k
Chess-Bot is a [Discord](https://discordapp.com/) BOT used to play chess directly in text channels against other users. It includes also a graphical chess board and a simple statistics database for each player. 

It makes use of the `python-chess` library as a chess engine. You can find it comfortably [here](https://python-chess.readthedocs.io/en/latest/).

## Starting the BOT
First, create a copy of `.env.example` and install all of the needed PIP packages using the `requirements.txt` file:
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

## Requirements for correct functioning
In order to function correctly, the BOT needs the following active privileges within the Server that will host it:
* `View Channels` permission: Necessary to allow the BOT to be able to view all text channels where users can play;
* `Send Messages` permission: Necessary to allow the BOT to send messages relating to invitations, games and statistics within the text channels;
* `Attach Files` permission: Necessary to allow the bot to send images containing the visual and current status of the chessboard within the text channels;

Also, to get the best possible experience, you can activate the following Intent:
* `Server Members Intent`: It allows the BOT to view the entire list of members connected to the Server that contains it, and not just that of users connected to any voice channel;

## Commands available within Chess-Bot
Several commands are available in Chess-Bot. They are divided into two categories: Main and Chess.

### Main Category:
The Main Category contains some useful and utility-based commands to simplify and extend  the user experience.
* `!rnd|random [minimum - optional] [maximum - optional]`: Draws a random number between `minimum` and `maximum`. If `minimum` and `maximum` are omitted, a number from 0 to 100 will be drawn;
* `!coin|flip|coinflip`: Flips a coin and returns the result;
* `!about|whois|info [user - optional]`: Shows different kind of informations about a specified `user`. If `user` is omitted, the context user info will be shown.

### Chess Category:
The Chess Category contains all the main and unique commands of Chess-Bot to be able to play chess against your friends, or perhaps your enemies...
* `!chess new|create|invite [user]`: Sends an invite for a new match to a specified `user`;
* `!chess accept [user]`: Accepts an invite sent by a specified `user` and starts a new match;
* `!chess invites`: Shows every out-coming and in-coming invites for the context user;
* `!chess move|execute [initial] [final]`: Takes an `initial` and a `final` chess coordinate and executes a move in the current match;
* `!chess show|chessboard`: Shows the current match chessboard disposition;
* `!chess surrend`: Surrend and lost the current match;
* `!chess statistics|stats [user - optional]`: Shows the statistics of a Discord user who played at least one match. If `user` is omitted, the context user stats will be shown.

## Some screen-shots about the BOT
![](https://i.ibb.co/BVcMNDj/Help.png)

![](https://i.ibb.co/hgks3Vp/Commands.png)

![](https://i.ibb.co/vv6RKHY/Start.png)

## License
This project is released under the `MIT License`. You can find the original license source here: [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).

```
MIT License

Copyright (c) 2020 Davide Casale

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```