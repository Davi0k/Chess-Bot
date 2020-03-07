import os, io, random, shortuuid, datetime, discord
from chess import Match, Colors
from generator import Generator
from model import Statistics
from PIL import Image
from discord.ext import commands
from threading import Timer
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix = "!", case_insensitive = True)

@bot.event
async def on_ready():
    name, identifier = bot.user.name, str(bot.user.id)
    print("The BOT is currently online, connect to a server which contains it to start playing...")
    print("The name of the BOT is: " + name)
    print("The ID of the BOT is: " + identifier)

class Invite:
    def __init__(self, challenger: discord.Member, challenged: discord.Member, guild: discord.Guild):
        self.challenger, self.challenged = challenger, challenged
        self.guild = guild
        self.timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

class Game:
    def __init__(self, white: discord.Member, black: discord.Member, guild: discord.Guild):
        self.id = shortuuid.ShortUUID().random(length = 6)
        self.white, self.black = white, black
        self.guild = guild
        self.match = Match()

async def send_error(ctx, title: str = "Error", description: str = "General internal error") -> None:
    title, description = f"**{title}:**", f"__{description}__"
    embed = discord.Embed(color = 0xff0000)
    embed.add_field(name = title, value = description, inline = True)
    await ctx.send(embed = embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await send_error(ctx, description = "Unknown command, try !help to list every available command")

    if isinstance(error, commands.BadArgument):
        return await send_error(ctx, description = "The passed arguments are not valid for the invoked command")

    raise error

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "rnd", aliases = [ "random" ], help = "Draws a random number between `minimum` and `maximum`. If `minimum` is omitted, it will be set to 0. If `minimum` and `maximum` are omitted, a number from 0 to 100 will be drawn")
    async def rnd(self, ctx, minimum: int = None, maximum: int = None):
        min, max = minimum, maximum

        if min is None and max is None: min, max = 0, 100
        if max is None: max = min; min = 0

        if min < max: 
            result = random.randrange(min, max + 1)
            await ctx.send(f"{ctx.message.author.mention} draws a random number between `{min}` and `{max}` and gets: `{result}`")
        else: await send_error(ctx, description = "The minimum value must be less than the maximum one")

    @commands.command(name = "coin", aliases = [ "flip", "coinflip" ], help = "Flips a coin and returns the result")
    async def coin(self, ctx):
        author = ctx.message.author
        result = random.choice(["HEADS", "TAILS"])
        await ctx.send(f"{author.mention} flips a coin and gets: `{result}`")

    @commands.command(name = "whois", aliases = [ "about", "info" ], help = "Shows different kind of informations about a specified `user`. If `user` is omitted, the context user info will be shown.")
    async def whois(self, ctx, user = None):
        author, guild = ctx.message.author, ctx.message.author.guild

        member = Main.get_member_by_name(guild, user or author.name)

        if member is None: return await send_error(ctx, description = "No user found in the current server")

        embed = discord.Embed(color = 0xff8040)

        value = (f"Username: {member.name}\n"
                    f"Discriminator: {member.discriminator}\n"
                    f"Server nickname: {member.nick}\n"
                    f"GUID: {member.id}\n"
                    f"Status: {member.status}\n"
                    f"Avatar URL: {member.avatar_url}"
                )

        embed.add_field(name = f"Who is {member.name}#{member.discriminator}:", value = value)

        await ctx.send(embed = embed)

    @staticmethod
    def get_member_by_name(guild: discord.Guild, name: str) -> discord.Member:
        if name is None: return None

        for member in guild.members:
            if member.name.lower() == name.lower():
                return member
                
            if member.nick is not None:
                if member.nick.lower() == name.lower():
                    return member
        else: return None

class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites = list()
        self.games = list()

    @commands.group(name = "chess", help = "It contains all the main and unique commands of Chess-Bot to be able to play chess against your friends, or perhaps your enemies...")
    async def chess(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.CommandNotFound

    @chess.command(name = "new", aliases = [ "create", "invite" ], help = "Sends an invite for a new match to a specified `user`")
    async def new(self, ctx, user = None):
        author, guild = ctx.message.author, ctx.message.author.guild

        user = Main.get_member_by_name(guild, user)

        if self.get_game_from_user(author): return await send_error(ctx, description = "You cannot send other invitations while you are in the middle of a match")

        if self.get_game_from_user(user): return await send_error(ctx, description = "You cannot send invitations to a person who is already playing")

        if user is None: return await send_error(ctx, description = "Please, specify a valid user to challenge")

        if author == user: return await send_error(ctx, description = "You cannot challenge your-self")

        for invite in self.invites:
            if invite.challenger == author and invite.challenged == user and invite.guild == guild:
                return await send_error(ctx, description = "You have already invited this user")

        invite = Invite(author, user, guild)

        self.invites.append(invite)

        await ctx.send(f"Ehy {user.mention}, {author.name} wants to play a chess match against you! Use `!chess accept {author.name}` or `!chess decline {author.name}` to accept or decline the invite")

    @chess.command(name = "accept", help = "Accepts an invite sent by a specified `user` and starts a new match")
    async def accept(self, ctx, user = None):
        author, guild = ctx.message.author, ctx.message.author.guild

        user = Main.get_member_by_name(guild, user)

        if self.get_game_from_user(author): return await send_error(ctx, description = "You cannot accept other invitations while you are in the middle of a match")

        if self.get_game_from_user(user): return await send_error(ctx, description = "The selected player is already playing, wait until he is done")

        if user is None: return await send_error(ctx, description = "Please, specify a valid user to accept his invite")
        
        invite = None

        for index, element in enumerate(self.invites):
            if element.challenged == author and element.challenger == user and element.guild == guild:
                invite = element; del self.invites[index]; break

        if invite is None: return await send_error(ctx, description = "No invite has been sent by the selected user")

        white = random.choice([ author, user ])
        
        if white is author: black = user
        if white is user: black = author

        game = Game(white, black, guild); self.games.append(game)

        file = Chess.get_binary_chessboard(game.match.chessboard)

        await ctx.send((f"**Match ID: {game.id}**\n"
                        f"Well, let's start this chess match with {white.mention} as `White Player` against {black.mention} as `Black Player`!"
                       ), file = file)

    @chess.command(name = "decline", help = "Declines an invite sent by a specified `user` and deletes it")
    async def decline(self, ctx, user = None):
        author, guild = ctx.message.author, ctx.message.author.guild

        user = Main.get_member_by_name(guild, user)

        if user is None: return await send_error(ctx, description = "Please, specify a valid user to decline his invite")

        invite = None

        for index, element in enumerate(self.invites):
            if element.challenged == author and element.challenger == user and element.guild == guild:
                invite = element; del self.invites[index]; break

        if invite is None: return await send_error(ctx, description = "No invite has been sent by the selected user")

        await ctx.send(f"Oh, maybe the next time! {author.mention} declined the invite of {user.mention}")

    @chess.command(name = "invites", help = "Shows every out-coming and in-coming invites for the context user")
    async def invites(self, ctx):
        author, guild = ctx.message.author, ctx.message.author.guild

        embed = discord.Embed(title = f"Invitations for {author.name}", color = 0x00ff00)
        outcoming, incoming = str(), str()

        for invite in self.invites:
            if invite.challenger == author and invite.guild == guild:
                challenged = invite.challenged
                outcoming += f"You to {challenged.name} - {invite.timestamp}\n"; continue
            if invite.challenged == author and invite.guild == guild:
                challenger = invite.challenger
                incoming += f"{challenger.name} to you - {invite.timestamp}\n"; continue

        if not outcoming: outcoming = "No out-coming invitations for you"
        embed.add_field(name = ":arrow_right: Out-coming invites", value = outcoming, inline = False)

        if not incoming: incoming = "No in-coming invitations for you"
        embed.add_field(name = ":arrow_left: In-coming invites", value = incoming, inline = False)

        await ctx.send(embed = embed)

    @chess.command(name = "move", aliases = [ "execute" ], help = "Executes a move during a chess match")
    async def move(self, ctx, initial, final):
        author = ctx.message.author

        game = self.get_game_from_user(author)

        if game is None: return await send_error(ctx, description = "You are not playing any match in this server")

        color = None

        if game.white == author: color = Colors.WHITE
        if game.black == author: color = Colors.BLACK

        if color is not game.match.turn: return await send_error(ctx, description = "It is not your turn to make a move")

        try:
            message = f"{game.white.mention} VS {game.black.mention} - Actual turn: `{game.match.turn}`"

            if game.match.move(initial, final): 
                message = f"**Match Finished** - {game.white.mention} VS {game.black.mention} - `{author.name}` won the chess match, CONGRATULATIONS!"
                          
                self.games.remove(game)

                if color is Colors.WHITE: Chess.update_statitics(game.white, game.black)
                if color is Colors.BLACK: Chess.update_statitics(game.black, game.white)

            file = Chess.get_binary_chessboard(game.match.chessboard)

            await ctx.send(message, file = file)
        except Exception as exception:
            return await send_error(ctx, description = str(exception))

    @chess.command(name = "show", aliases = [ "chessboard" ], help = "Shows the current match chessboard disposition")
    async def show(self, ctx):
        author = ctx.message.author

        game = self.get_game_from_user(author)

        if game is None: return await send_error(ctx, description = "You are not playing any match in this server")

        file = Chess.get_binary_chessboard(game.match.chessboard)

        await ctx.send(f"{game.white.mention} VS {game.black.mention} - Actual turn: `{game.match.turn}`", file = file)

    @chess.command(name = "surrend", help = "Surrend and lost the current match")
    async def surrend(self, ctx):
        author = ctx.message.author

        game = self.get_game_from_user(author)

        if game is None: return await send_error(ctx, description = "You are not playing any match in this server")

        winner = None

        if game.white == author: winner = game.black
        if game.black == author: winner = game.white

        self.games.remove(game)

        if game.white == author: Chess.update_statitics(game.black, game.white)
        if game.black == author: Chess.update_statitics(game.white, game.black)

        await ctx.send(f"{game.white.mention} VS {game.black.mention} - `{author.name}` surrended, `{winner.name}` won the match, CONGRATULATIONS!")

    @chess.command(name = "statistics", aliases = [ "stats" ], help = "Shows the statistics of a Discord user who played at least one match. If `user` is omitted, the context user stats will be shown")
    async def statistics(self, ctx, user = None):
        author, guild = ctx.message.author, ctx.message.author.guild

        member = Main.get_member_by_name(guild, user or author.name)

        if member is None: return await send_error(ctx, description = "No user found in the current server")

        embed = discord.Embed(color = 0x0000ff)

        try: 
            statistics = Statistics.objects.get(player = member.id)
            
            value = (f":vs: Number of matches played: {statistics.totals}\n\n"
                     f":blue_circle: Number of matches won: {statistics.wins}\n"
                     f":red_circle: Server Number of matches lost: {statistics.losts}\n\n"
                     f":clock4: Last match date: {statistics.timestamp.strftime('%d-%m-%Y %H:%M')}"
                    )

            embed.add_field(name = f"Chess-Bot Statistics of {member.name}#{member.discriminator}", value = value)
        except: 
            embed.add_field(name = "Information:", value = "The selected player has never played a game, his stats are therefore not available")

        await ctx.send(embed = embed)

    def get_game_from_user(self, user: discord.Member) -> Match:
        for game in self.games:
            if (game.white == user or game.black == user) and game.guild == user.guild:
                return game
        else: return None

    @staticmethod
    def get_binary_chessboard(chessboard) -> discord.File:
        size = (500, 500)

        with io.BytesIO() as binary:
            chessboard = Generator.generate(chessboard).resize(size, Image.ANTIALIAS)
            chessboard.save(binary, "PNG"); binary.seek(0)
            return discord.File(fp = binary, filename = "chessboard.png")

    @staticmethod
    def update_statitics(winner: discord.Member, loser: discord.Member):
        winner, loser = winner.id, loser.id

        try: winner = Statistics.objects.get(player = winner)
        except: winner = Statistics(player = winner)

        try: loser = Statistics.objects.get(player = loser)
        except: loser = Statistics(player = loser)

        winner.totals += 1; loser.totals += 1
        winner.wins += 1; loser.losts += 1

        now = datetime.datetime.now()

        winner.timestamp = now; loser.timestamp = now

        winner.save(); loser.save()

bot.add_cog(Main(bot))

bot.add_cog(Chess(bot))

bot.run(TOKEN)