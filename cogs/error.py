import sys
import traceback

from discord.ext import commands


# Don't let any tools I get in the future complain about us catching
# exceptions too broadly here because that's kinda the whole point

# noinspection PyBroadException
class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except:  # noqa: E722
                pass

        elif isinstance(error, commands.errors.CommandOnCooldown):
            try:
                return await ctx.author.send(f'This command is on cooldown! Please try again in '
                                             f'{int(error.retry_after)} seconds.')
            except:  # noqa: E722
                pass

        elif isinstance(error, commands.BadArgument):
            return await ctx.send('Invalid arguments.')

        elif isinstance(error, commands.CheckFailure):
            return await ctx.send("Either you don't have permission to do that, or it can't be done here, baka!")

        await ctx.send(f"Sorry! An unexpected error has occurred. Please let <@84163178585391104> know ASAP, "
                       f"unless you just broke it for fun.\n```"
                       f"{''.join(traceback.format_exception(type(error), error, error.__traceback__))}```")
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
