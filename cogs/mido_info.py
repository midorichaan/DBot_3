import discord
from discord.ext import commands

import re
import time
import datetime
import psutil
import platform

import util

class mido_info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.notify_channels = {464964949823848449: "RisuPu", 670557793010319362: "MCS", 695026857438871592: "VPN", 703556849710006353: "NTP",
                                718592791223074846: "RisuPu-rsvr", 789495012831920128: "MDBS", 718592871749517353: "Other", 698514180214489128: "RisuPu MusicBot"}

    #resolve_url
    def resolve_url(self, url):
        HTTP_URL_REGEX = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        URL_REGEX = "[\w/:%#\$&\?\(\)~\.=\+\-]+"

        if re.match(HTTP_URL_REGEX, str(url)):
            return str(url)
        elif re.match(URL_REGEX, str(url)):
            return f"http://" + str(url)
        else:
            return False

    #resolve_status
    def resolve_status(self, status):
        if str(status) == "online":
            return "ðãªã³ã©ã¤ã³"
        elif str(status) == "dnd":
            return "â¤åãè¾¼ã¿ä¸­"
        elif str(status) == "idle":
            return "ð§¡éå¸­ä¸­"
        elif str(status) == "offline":
            return "ð¤ãªãã©ã¤ã³"

    #debug
    @commands.command(name="debug", aliases=["dbg"], description="Botã®ãããã°æå ±ãè¡¨ç¤ºãã¾ãã", usage="rsp!debug | rsp!dbg")
    async def debug(self, ctx):
        e = discord.Embed(title="Debug Information", description="å¦çä¸­...", color=self.bot.color, timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=e)

        mem = psutil.virtual_memory()
        allmem = str(mem.total/1000000000)[0:3]
        used = str(mem.used/1000000000)[0:3]
        ava = str(mem.available/1000000000)[0:3]
        memparcent = mem.percent
        cpu = psutil.cpu_percent(interval=1)
        core_a = psutil.cpu_count()
        core_b = psutil.cpu_count(logical=False)
        f = 100-memparcent

        dsk = psutil.disk_usage("/")
        d_used = str(dsk.used/100000000)[0:3]
        d_free = str(dsk.free/1000000000)[0:3]

        e.description = None
        e.add_field(name="OS", value=f"{platform.platform(aliased=True)} ({platform.machine()})")
        e.add_field(name="OS Version", value=platform.release())
        e.add_field(name="CPU Information", value=f"Usage: {cpu}% \nCore: {core_a}/{core_b}")
        e.add_field(name="Memory Information", value=f"Total: {allmem}GB \nUsed: {used}GB ({memparcent}%) \nFree: {ava}GB ({f}%)")
        e.add_field(name="Disk Information", value=f"Total: {d_used}GB \nFree: {d_free}GB \nUsage: {dsk.percent}%")
        e.add_field(name="Shard Information", value=f"Total: {self.bot.shard_count}")
        e.add_field(name="Last Started Date", value=self.bot.uptime.strftime('%Y/%m/%d %H:%M:%S'))
        e.add_field(name="Bot Information", value=f"discord.py v{discord.__version__} \nPython v{platform.python_version()}")

        await msg.edit(embed=e)

    #about
    @commands.group(name="about", description="Botã«ã¤ãã¦ã®æå ±ãè¡¨ç¤ºãã¾ãã", usage="rsp!about [args]", invoke_without_command=True)
    async def about(self, ctx):
        e = discord.Embed(title="Info - about", description="å¦çä¸­...", color=self.bot.color, timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=e)

        e.description = """
        > 1. ãã®Botã«ã¤ãã¦
         ãã®Botã¯RisuPu (https://risupunet.jp/) Discordãµã¼ãã¼ç¨ã«ä½ãããå°å±Botã§ãã
         Botã®å°å¥ç­ã¯ã§ãã¾ããã®ã§ãæ³¨æãã ããã

        > 2. RisuPu Discordãµã¼ãã¼
         æ¬ãµã¼ãã¼: https://discord.gg/2JkvG2JwuC
         ãµãã¼ããµã¼ãã¼: https://discord.gg/zaQnvmrp76

        > 3. Botã®ä¸å·åç­ã«ã¤ãã¦
         ã»Midorichan#3451 (ID: 546682137240403984)ã«DM
         ã»ãµãã¼ããµã¼ãã¼ã«ã¦ãã±ãããçºè¡
         ã»Twitter: https://twitter.com/Midorichaan2525
         ã»Mail: midorichan@adm.rspnet.jp

        > 4. ãã®ä»
         éçºèã¯ Midorichan#3451 (ID: 546682137240403984) ã§ãããæææ¨©ã¯RisuPuã«ãããã®ã¨ãã¾ãã
        """

        await msg.edit(embed=e)

    #about notice
    @about.command(name="notice", description="Botã®ãç¥ãããè¡¨ç¤ºãã¾ãã", usage="rsp!about notice")
    async def notice(self, ctx):
        e = discord.Embed(title="About - notice", description="å¦çä¸­...", color=self.bot.color, timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=e)
        e.description = self.bot.notice or "ãªã"

        return await msg.edit(embed=e)

    #about support
    @about.command(name="support", description="ãµãã¼ããµã¼ãã¼ã®URLç­ãè¡¨ç¤ºãã¾ãã", usage="rsp!about support")
    async def support(self, ctx):
        e = discord.Embed(title="About - support", description="å¦çä¸­...", color=self.bot.color, timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=e)

        e.description = "> RisuPuãåãåããã»ãµãã¼ã \nDiscordãµã¼ãã¼: https://discord.gg/zaQnvmrp76 \nWeb: https://www.risupunet.jp/contact \nãµãã¼ã(ã¡ã¼ã«): support@rspeml.jp \nAbuse: abuse@rspeml.jp \nåäººæå ±æå½çªå£: ãã©ã¤ãã·ã¼ããªã·ã¼ã«æè¨ãã¦ããæå½é¨ç½²"

        await msg.edit(embed=e)

    #ping
    @commands.command(name="ping", description="Pingãè¡¨ç¤ºãã¾ããURLãæå®ããã¨ãã®ãµã¤ãã®ã¹ãã¼ã¿ã¹ã³ã¼ããåå¾ãã¾ãã", usage="rsp!ping [url] [noproxy]")
    async def ping(self, ctx, link=None, option:str=None):
        st = time.time()
        e = discord.Embed(title="Ping pong!!", description="Pinging...Please Wait....", color=self.bot.color, timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=e)

        if link == None:
            e.description = "ã½ããã£ï¼ð"
            e.add_field(name="Ping", value=str(round(time.time()-st, 3) * 1000)+"ms")
            e.add_field(name="WebSocket", value=f"{round(self.bot.latency * 1000, 2)}ms")
            [e.add_field(name=f"Shard{s}", value=f"{round(self.bot.get_shard(s).latency * 1000, 2)}ms") for s in self.bot.shards]
            return await msg.edit(embed=e)
        else:
            url = self.resolve_url(link)

            if url is False:
                e.description = None
                e.add_field(name="ã¨ã©ã¼", value="URLãä¸æ­£ã§ãã")
                return await msg.edit(embed=e)

            latency = time.time()

            if option == "noproxy" and ctx.author.id in self.bot.owner_ids:
                async with ctx.bot.session.get(url) as ret:
                    e.description = f"Latency: {round(time.time() - latency, 3) * 1000}ms"
                    e.add_field(name="Result", value=f"ã¹ãã¼ã¿ã¹ã³ã¼ã: {ret.status}")
                    return await msg.edit(embed=e)
            else:
                async with ctx.bot.session.get(url, proxy=f"{ctx.bot.config.PROXY_URL}:{ctx.bot.config.PROXY_PORT}") as ret:
                    e.description = f"Latency: {round(time.time() - latency, 3) * 1000}ms"
                    e.add_field(name="Result", value=f"ã¹ãã¼ã¿ã¹ã³ã¼ã: {ret.status}")
                    return await msg.edit(embed=e)

    #on_member_join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 461153681971216384:
            e = discord.Embed(color=0x36b8fa, timestamp=datetime.datetime.now())
            e.set_author(name=f"{member} ãããåå ãã¾ããï¼ï¼", icon_url=member.avatar_url_as(static_format="png"))
            e.add_field(name="ID", value=str(member.id))
            e.add_field(name="Botã", value="ã¯ã" if member.bot else "ããã")
            e.add_field(name="ã¹ãã¼ã¿ã¹", value=self.resolve_status(member.status))
            e.add_field(name="ã¢ã«ã¦ã³ãä½ææ¥", value=str(member.created_at.strftime('%Y/%m/%d %H:%M:%S')))

            dm = discord.Embed(title=f"{member.guild} ã¸ããããï¼", description="", color=0x36b8fa, timestamp=member.joined_at)
            dm.description = f"""
            {member.guild}å¬å¼Discordãµã¼ãã¼ã¸ãåå ããã ããã¾ãã¨ã«ãããã¨ããããã¾ãã
            å½ãµã¼ãã¼ã§ã¯Botãä»ããèªè¨¼ãè¡ããªãã¨ãã£ããã«åå ã§ããªãä»çµã¿ã¨ãªã£ã¦ããã¾ãã

            ã¾ãåãã«ãã®ä»¥ä¸å½çµç¹ã°ã«ã¼ãä¼å¡è¦ç´ã»ã³ãã¥ããã£ãµã¼ãå©ç¨è¦ç´ããèª­ã¿ãã ããã
            > **https://www.risupunet.jp/agreement/dcd-srvtos/**
            ä¸è¨è¦ç´ã«åæããã ããå ´åã¯ãèªè¨¼ã«ã¤ãã¦ã®æ¡ç´ã«è¨è¼ããã¦ããæ¹æ³ã§èªè¨¼ãã¦ä¸ããã
            â»èªè¨¼ã¯ <#621387537608605716> ã§è¡ã£ã¦ãã ããã

            > **------------------------------------------------------------------------------------------**
            rspnet.jpã°ã«ã¼ã
            RisuPu by RSPnet.jp

            ãã¼ã ãã¼ã¸ãã**https://suoc.me/rspnet**
ãããããããã            **https://www.risupunet.jp/**

            ãåãåãããããµãã¼ããã¹ã¯ç­
ãããããããã            **https://www.risupunet.jp/contact/**

ãããããããã            ãµãã¼ããµã¼ãã¼
ãããããããã            **https://discord.gg/phvBHXh5DT**
            > **------------------------------------------------------------------------------------------**
            """

            try:
                await member.send(embed=dm)
                await member.guild.get_channel(621387537608605716).send(embed=dm)
            except:
                await member.guild.get_channel(621387537608605716).send(embed=dm)

            await member.guild.get_channel(685034563747184650).send(content="> ã¡ã³ãã¼ã®æå ±", embed=e)
            await member.guild.get_channel(461153681971216388).send(content="> ã¡ã³ãã¼ã®æå ±", embed=e)

    #on_member_left
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 461153681971216384:
            e = discord.Embed(color=0x36b8fa, timestamp=datetime.datetime.now())
            e.set_author(name=f"{member} ãããéåºãã¾ãã...", icon_url=member.avatar_url_as(static_format="png"))
            e.add_field(name="ID", value=str(member.id))
            e.add_field(name="Botã", value="ã¯ã" if member.bot else "ããã")
            e.add_field(name="ã¹ãã¼ã¿ã¹", value=self.resolve_status(member.status))
            e.add_field(name="ãµã¼ãã¼åå æ¥", value=str(member.joined_at.strftime('%Y/%m/%d %H:%M:%S')))
            e.add_field(name="ã¢ã«ã¦ã³ãä½ææ¥", value=str(member.created_at.strftime('%Y/%m/%d %H:%M:%S')))

            await member.guild.get_channel(685034563747184650).send(embed=e)
            await member.guild.get_channel(461153681971216388).send(embed=e)

    #on_message
    @commands.Cog.listener()
    async def on_message(self, msg):
        if isinstance(msg.channel, discord.DMChannel):
            return

        if msg.guild.id == 461153681971216384 and msg.channel.id in self.notify_channels:
            e = discord.Embed(title=f"ð¢ {self.notify_channels[msg.channel.id]} Notification", description=f"{msg.channel.mention}ã§æ°ãããç¥ãããããã¾ãï¼ï¼ \n[ãããã¯ãªãã¯]({msg.jump_url})", color=0x36b8fa, timestamp=msg.created_at)
            await msg.guild.get_channel(685034563747184650).send(embed=e)

    #userinfo
    @commands.command(name="userinfo", aliases=["ui", "user"], description="ã¦ã¼ã¶ã¼ã®æå ±ãè¡¨ç¤ºãã¾ãã", usage="rsp!userinfo [user/member]")
    async def userinfo(self, ctx, user:util.FetchUserConverter=None):
        e = discord.Embed(title="User Information", description="å¦çä¸­...", color=self.bot.color, timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=e)

        if not user:
            user = ctx.author

        e.set_thumbnail(url=user.avatar_url_as(static_format="png"))
        e.description = None
        e.add_field(name="ã¦ã¼ã¶ã¼å", value=f"{user} \n({user.id})")

        if ctx.guild and isinstance(user, discord.Member):
            e.add_field(name="ããã¯ãã¼ã ", value=user.display_name)

        e.add_field(name="Botã", value="ã¯ã" if user.bot else "ããã")

        if isinstance(user, discord.Member):
            e.add_field(name="Nitroãã¼ã¹ã¿ã¼", value=f"{user.premium_since.strftime('%Y/%m/%d %H:%M:%S')}ãã" if user.premium_since is not None else "ãªã")

        e.add_field(name="ã¢ã«ã¦ã³ãä½ææ¥æ", value=user.created_at.strftime('%Y/%m/%d %H:%M:%S'))

        if isinstance(user, discord.Member):
            e.add_field(name="ãµã¼ãã¼åå æ¥æ", value=user.joined_at.strftime('%Y/%m/%d %H:%M:%S'))
            e.add_field(name="ã¹ãã¼ã¿ã¹", value=self.resolve_status(user.status))
            if not user.activity:
                try:
                    if user.activity.type == discord.ActivityType.custom:
                        e.add_field(name="ã«ã¹ã¿ã ã¹ãã¼ã¿ã¹", value=user.activity)
                    else:
                        e.add_field(name="ã«ã¹ã¿ã ã¹ãã¼ã¿ã¹", value=f"{user.activity.name}")
                except:
                    e.add_field(name="ã«ã¹ã¿ã ã¹ãã¼ã¿ã¹", value=user.activity)

            roles = ", ".join(c.mention for c in list(reversed(user.roles)))
            if len(user.roles) <= 1000:
                e.add_field(name="å½¹è·", value=roles, inline=False)
            else:
                e.add_field(name="å½¹è·", value="å¤ããã¦è¡¨ç¤ºã§ããªããï¼", inline=False)
            e.add_field(name=f"æ¨©é ({user.guild_permissions.value})", value=", ".join("`{}`".format(self.bot.json_config["roles"].get(c, str(c))) for c,b in dict(user.guild_permissions).items() if b is True), inline=False)

        await msg.edit(embed=e)

def setup(bot):
    bot.add_cog(mido_info(bot))
