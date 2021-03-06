import discord
from discord.ext import commands

import threads
import asyncio
import util

class mido_thread(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.threadutil = threads.ThreadHTTP(bot)

    #reactions
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        if str(payload.emoji) == "ð":
            try:
                await self.threadutil.create_thread_with_message(payload.channel_id, payload.message_id, f"thread-{payload.user_id}", 1440)
            except Exception as exc:
                print(f"[Error] {exc}")
            else:
                await self.bot.get_channel(payload.channel_id).send(f"> ã¹ã¬ãããä½æãã¾ããï¼\nâ <#{payload.message_id}>")

    #threads
    @commands.group(name="threads", aliases=["thread"], description="threadé¢é£ã®ã³ãã³ãã§ãã", usage="rsp!threads <args> [args]", invoke_without_command=True)
    async def threads(self, ctx):
        pass

    #threads help
    @threads.command(name="help", description="threadsã®ãã«ãã§ãã", usage="rsp!threads help [command]")
    async def help(self, ctx, cmd=None):
        e = discord.Embed(title="Threads help", description="å¦çä¸­...", color=self.bot.color, timestamp=ctx.message.created_at)
        m = await ctx.send(embed=e)

        e.description = None

        if cmd:
            c = self.bot.get_command("threads").get_command(cmd)

            if c:
                e.title = f"Threads - {c.name}"
                e.add_field(name="èª¬æ", value=c.description or "èª¬æãªã")
                e.add_field(name="ä½¿ç¨æ³", value=c.usage or "ä¸æ")
                e.add_field(name="ã¨ã¤ãªã¢ã¹", value=", ".join([f"`{row}`" for row in c.aliases]))
                return await m.edit(embed=e)
            else:
                for c in self.bot.get_command("threads").commands:
                    e.add_field(name=c.name, value=c.description or "èª¬æãªã")

                return await m.edit(embed=e)
        else:
            for c in self.bot.get_command("threads").commands:
                e.add_field(name=c.name, value=c.description or "èª¬æãªã")

            return await m.edit(embed=e)

    #addmember
    @threads.command(name="addmember", description="ã¡ã³ãã¼ãã¹ã¬ããã«è¿½å ãã¾ãã", usage="rsp!threads addmember <thread_id> <members>", brief="éå¶ãã¼ã ã®ã¿")
    @commands.check(util.is_risupu_staff)
    async def addmember(self, ctx, thread_id: int=None, members:commands.Greedy[discord.Member]=None):
        m = await ctx.send("> å¦çä¸­...")

        if not thread_id:
            return await m.edit(content="> ã¹ã¬ããIDãæå®ãã¦ã­ï¼")

        if not members:
            return await m.edit(content="> ã¡ã³ãã¼ãæå®ãã¦ã­ï¼")


        tasks = []
        for i in members:
            tasks.append(self.threadutil.add_member(thread_id, i.id))

        try:
            await asyncio.gather(*tasks)
        except Exception as exc:
            return await m.edit(content=f"> ã¨ã©ã¼ \n```py\n{exc}\n```")
        else:
            return await m.edit(content=f"> {len(members)}äººã®ã¡ã³ãã¼ãã¹ã¬ããã«è¿½å ãã¾ããï¼")

    #removemember
    @threads.command(name="removemember", aliases=["rmmember"], description="ã¡ã³ãã¼ãã¹ã¬ããããåé¤ãã¾ãã", usage="rsp!threads removemember <thread_id> <members>", brief="éå¶ãã¼ã ã®ã¿")
    @commands.check(util.is_risupu_staff)
    async def removemember(self, ctx, thread_id: int=None, members:commands.Greedy[discord.Member]=None):
        m = await ctx.send("> å¦çä¸­...")

        if not thread_id:
            return await m.edit(content="> ã¹ã¬ããIDãæå®ãã¦ã­ï¼")

        if not members:
            return await m.edit(content="> ã¡ã³ãã¼ãæå®ãã¦ã­ï¼")

        tasks = []
        for i in members:
            tasks.append(self.threadutil.remove_member(thread_id, i.id))

        try:
            await asyncio.gather(*tasks)
        except Exception as exc:
            return await m.edit(content=f"> ã¨ã©ã¼ \n```py\n{exc}\n```")
        else:
            return await m.edit(content=f"> {len(members)}äººã®ã¡ã³ãã¼ãã¹ã¬ããããåé¤ãã¾ããï¼")

    #create
    @threads.command(name="create", description="ã¹ã¬ãããä½æãã¾ãã", usage="rsp!threads create <name> [channel] [message] [archive]")
    async def create(self, ctx, name: str=None, channel: commands.TextChannelConverter=None, message: commands.MessageConverter=None, archive: int=1440):
        m = await ctx.send("> å¦çä¸­...")

        if not name:
            return await m.edit(content="> ã¹ã¬ããåãæå®ãã¦ãã ããã")

        if not channel:
            channel = ctx.channel

        if message:
            try:
                pl = await self.threadutil.create_thread_with_message(channel.id, message.id, name, archive)
            except Exception as exc:
                return await m.edit(content=f"> ã¨ã©ã¼ \n```py\n{exc}\n```")
            else:
                return await m.edit(content=f"> ã¹ã¬ãããä½æãã¾ããï¼ \n â <#{pl['id']}>")
        else:
            try:
                pl = await self.threadutil.create_thread(channel.id, name, archive)
            except Exception as exc:
                return await m.edit(content=f"> ã¨ã©ã¼ \n```py\n{exc}\n```")
            else:
                return await m.edit(content=f"> ã¹ã¬ãããä½æãã¾ããï¼ \n â <#{pl['id']}>")

    #archive
    @threads.command(name="archive", description="ã¹ã¬ãããã¢ã¼ã«ã¤ããã¾ãã", usage="rsp!threads archive <thread_id>", brief="éå¶ãã¼ã ã®ã¿")
    @commands.check(util.is_risupu_staff)
    async def archive(self, ctx, thread: int=None):
        m = await ctx.send("> å¦çä¸­...")

        if not thread:
            return await m.edit(content="> ã¹ã¬ããã®IDãæå®ãã¦ãã ããã")

        try:
            await self.threadutil.archive_thread(thread)
        except Exception as exc:
            return await m.edit(content=f"> ã¨ã©ã¼ \n```py\n{exc}\n```")
        else:
            return await m.edit(content="> ã¹ã¬ãããã¢ã¼ã«ã¤ããã¾ããï¼")

    #delete
    @threads.command(name="delete", description="ã¹ã¬ãããåé¤ãã¾ãã", usage="rsp!threads delete <thread_id>", brief="éå¶ãã¼ã ã®ã¿")
    @commands.check(util.is_risupu_staff)
    async def delete(self, ctx, thread_id: int=None):
        m = await ctx.send("> å¦çä¸­...")

        if not thread_id:
            return await m.edit(content="> ã¹ã¬ããã®IDãæå®ãã¦ãã ããã")

        try:
            await self.bot.http.delete_channel(thread_id)
        except Exception as exc:
            return await m.edit(content=f"> ã¨ã©ã¼ \n```py\n{exc}\n```")
        else:
            return await m.edit(content="> ã¹ã¬ãããåé¤ãã¾ããï¼")

def setup(bot):
    bot.add_cog(mido_thread(bot))
