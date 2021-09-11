import discord
from discord.ext import commands


class TicTacToeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.game_started = False
        self.player1 = None
        self.player2 = None
        self.board = [
                      "-", "-", "-",
                      "-", "-", "-",
                      "-", "-", "-"
                      ]
        self.turn = "player1"

    async def send_board(self, ctx):
        if self.game_started:
            message = ""
            for nr, value in enumerate(self.board):
                message += value + " "
                if nr in (2, 5, 8):
                    message += "\n"

            if self.turn == "player1":
                player = self.player1
            else:
                player = self.player2
            await ctx.send(f"{message}Turn of player: {player.mention}")

    async def check_win(self, ctx):
        won = False
        if self.board[0] == self.board[1] == self.board[2] and self.board[0] != "-":
            won = True
        if self.board[3] == self.board[4] == self.board[5] and self.board[3] != "-":
            won = True
        if self.board[6] == self.board[7] == self.board[8] and self.board[6] != "-":
            won = True
        if self.board[0] == self.board[3] == self.board[6] and self.board[0] != "-":
            won = True
        if self.board[1] == self.board[4] == self.board[7] and self.board[1] != "-":
            won = True
        if self.board[2] == self.board[5] == self.board[8] and self.board[2] != "-":
            won = True
        if self.board[0] == self.board[4] == self.board[8] and self.board[0] != "-":
            won = True
        if self.board[2] == self.board[4] == self.board[6] and self.board[2] != "-":
            won = True

        if won:
            if self.turn == "player1":
                winner = self.player1
            else:
                winner = self.player2

            await ctx.send(f"{winner.mention} wins!")
            self.game_started = False

    @commands.command(name="start")
    async def start(self, ctx):
        await ctx.send(f"Game starts for: {str(ctx.author)}")

        if not self.game_started:
            if self.player1 is None:
                self.player1 = ctx.author

            elif self.player2 is None:
                self.player2 = ctx.author
                self.game_started = True
                await ctx.send(f"Game starts for {str(self.player1)} i {str(self.player2)}")

        else:
            await ctx.send("Game already started.")

    @commands.command(name="set")
    async def set(self, ctx, *args):
        if self.game_started:
            nr = int("".join(args))
            if 0 < nr < 10 and self.board[nr - 1] == "-":
                if self.turn == "player1":
                    if str(self.player1) == str(ctx.author):
                        self.board[nr - 1] = "x"
                        await self.check_win(ctx)
                        self.turn = "player2"
                        await self.send_board(ctx)
                        if not ("-" in self.board):
                            await ctx.send("Game over")
                            self.game_started = False
                    else:
                        await ctx.send("Not your turn.")
                else:
                    if str(self.player2) == str(ctx.author):
                        self.board[nr - 1] = "o"
                        await self.check_win(ctx)
                        self.turn = "player1"
                        await self.send_board(ctx)
                        if not ("-" in self.board):
                            await ctx.send("Game over")
                            self.game_started = False
                    else:
                        await ctx.send("Not your turn.")
            else:
                await ctx.send("Invalid number or field already taken.")
        else:
            await ctx.send("Game is not started.")

