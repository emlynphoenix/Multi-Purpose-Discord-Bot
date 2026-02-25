import discord
import discord.ui
import asyncio
from discord import NotFound, Forbidden
from discord.ext.commands.errors import CommandNotFound
from discord.ext import commands
from discord.ext import tasks
from rbxapiyes.exceptions import PlayerNotFound, Unauthorized
from rbxapiyes.Client import Client as Client1
from ro_py import Client as Client2
import time
import chat_exporter
import io
from io import *
import requests
import csv
import arrow
import math
import humanfriendly
from discord.ui import InputText, Modal
from operator import itemgetter
from datetime import datetime, timedelta, timezone
import ast
from roblox import Client
from typing import List
import mysql.connector


maincolor = 0xFFFFFF
grey = 0x99AAB5
redcolor = 0xed4245
nocolour = 0x2b2d31

class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        if user.id == 722113748088782899 or user.id == 1037772222145765406:
            return True
        return await super().is_owner(user)
    
invites = {}
overwrites = {}

def openCON():
  con = mysql.connector.connect(user='root', password='3Hci2W1G!^L3', host='localhost', database='sparkles_mm_bot')
  cur = con.cursor(dictionary=True)
  return con, cur

def closeCON(cur,con):
  cur.close()
  con.close()


TOKEN = ""
PREFIX = "$"
DB_SERVERID = 997526266171371601
MAIN_INFOID = 997527838565597268
LOGSINFO_ID = 997527868722663535
TICKETLOGS_ID = 1147315076274073610
MMROLE_ID = 1147238049231683735 
GUILD_ID = 1147232317983707246
CLOSED_CATEGORY_ID = 1147831767005401159
STATS_UPDATES_CHANNELID = 1147241690311163918
FIRST_TICKETS_CAT = 1147241185937727669
BLACKLIST_ROLE = 1147270835527233547
IGNORE_THESE = [997526266859241515, 997527838565597268, 997527868722663535]
SUPPORT_ID = 1147234818195718165

STARTER_TICKETS = 1147241274508845178 
NOVICE_TICKETS = 1147241317987000451 
MIDDLEMAN_TICKETS = 1147241385712431175 
SENIOR_TICKETS = 1147241423691857981 
ADV_TICKETS = 1147241467169996810
HEAD_TICKETS = 1147241510039978025
ADMIN_TICKETS = 1147323324943306752

STARTER_ROLE = 1147238000418369707
NOVICE_ROLE = 1147237907388715048
MIDDLEMAN_ROLE = 1147237851948388553
SENIOR_ROLE = 1147237795983786094
ADV_ROLE = 1147237739461353543
HEAD_ROLE = 1147237678031577279
cates = [STARTER_TICKETS, NOVICE_TICKETS, MIDDLEMAN_TICKETS, SENIOR_TICKETS, ADV_TICKETS, HEAD_TICKETS, ADMIN_TICKETS, FIRST_TICKETS_CAT, CLOSED_CATEGORY_ID, 1103657193531781200, 995691309601914910]


intents = discord.Intents.all()
intents.members = True
intents.voice_states = True


bot = MyBot(command_prefix=PREFIX, intents=intents, case_insensitive=True, help_command=None)
MyBot.last_channel = None

bot.load_extension("jishaku")

ROBLOSECURITY = "" # put your cookie here
session = requests.Session()
session.cookies[".ROBLOSECURITY"] = ROBLOSECURITY
req = session.get(url="https://users.roblox.com/v1/users/authenticated")
req = session.post(url="https://auth.roblox.com/")
if "X-CSRF-Token" in req.headers:
  session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
req2 = session.post(url="https://auth.roblox.com/")

client = Client()


async def updatedb_logs(data, logsdata_msg, dbchannel):
  buffer = io.StringIO()
  buffer.name = "output.py"
  buffer.write(str(data))
  buffer.seek(0)
  await logsdata_msg.delete()
  await dbchannel.send(file=discord.File(buffer, 'output.py'))

async def loa_logs(data, messages, dbchannel):
  buffer = io.StringIO()
  buffer.name = "loa.py"
  buffer.write(str(data))
  buffer.seek(0)
  await messages.delete()
  await dbchannel.send(file=discord.File(buffer, 'loa.py'))

@bot.command()
async def a(ctx):
  c = bot.get_channel(1155888521840693359)
  buffer = io.StringIO()
  await c.send(file=discord.File(buffer, 'loa.py'))


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X
        elif diag == 3:
            return self.O

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None



@tasks.loop(seconds=10)
async def time_status():
    # my_date = datetime.now(pytz.timezone('Asia/Qatar'))
    # time = my_date.strftime('%I:%M %p')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Middleman Tickets"), status=discord.Status.dnd)


@tasks.loop(hours=1)
async def purger1():
  try:
    category = bot.get_channel(1147234780375678996)
    general = discord.utils.get(category.channels, name="🌷・chat") 
    commands = discord.utils.get(category.channels, name="🌷・cmds") 
    new_channel = await general.clone(reason="Channel was purged")
    await new_channel.edit(position=general.position)
    await general.delete()
    await new_channel.send("This channel has been **purged**. Every **hour** this channel will be deleted. We do this to ensure the server's **safety**")
    bot.last_channel = new_channel

    new_channel2 = await commands.clone(reason="Channel was purged")
    await new_channel2.edit(position=commands.position)
    await commands.delete()
    await new_channel2.send("This channel has been **purged**. Every **hour** this channel will be deleted. We do this to ensure the server's **safety**")
    bot.last_channel = new_channel2
  except Exception:
    pass

@purger1.before_loop
async def before_msg1():
  for _ in range(60*60*24): # loop the whole day
    if datetime.now().minute == 0: # 24 hour format
      return
    await asyncio.sleep(1)

@tasks.loop(seconds=90)
async def warn():
  try:
    category = bot.get_channel(1103759996468080752)
    embed = discord.Embed(title="WARNING", description=f"⚠️・To **avoid** getting the **TRADEBAN** role, do **not** use these words\n- Account\n- Nitro\n- Discord\n- Server\n- Beam\n- Method\n- Free", color=discord.Colour.red())
    await category.send(embed=embed)
  except Exception:
    pass

@tasks.loop(minutes=30)
async def check_logs():
    category = bot.get_channel(CLOSED_CATEGORY_ID)
    transcript_channel = bot.get_channel(TICKETLOGS_ID)
    ticketlogs = bot.get_channel(TICKETLOGS_ID)
    
    try:
      if len(category.channels) == 0:
        return
    except Exception:
      return

    users_1 = {}
    
    dbchannel = bot.get_channel(LOGSINFO_ID)
    logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
    while len(logsdata_msg) == 0:
      logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
      time.sleep(0.5)
    logsdata_msg=logsdata_msg[0]
    file = logsdata_msg.attachments[0]
    cont = await file.read()
    alldata = ast.literal_eval(cont.decode('utf-8'))
    users_list = []
    for i in alldata:
      users_list.append(str(i['username']))
    
    for i in category.channels:
      name = i.name.split("-")[0]
      name2 = i.name.split(" ")[0]
      
      toggle = False
      if name in users_list:
        name = name
        toggle = True
      elif name2 in users_list:
        name = name2
        toggle = True
      
      if toggle == True:
        if i.name == f"{name}-done" or i.name == f"{name} done":
            if name in users_1.keys():
              users_1[name]+=1
              users = {}
              transcript = await chat_exporter.export(channel=i, limit=None, tz_info="Asia/Qatar")
              logembed = discord.Embed(description=f"Author: **Auto Deletion**\nTicket: **{i.name}** | ID: {i.id}\nAction: **Deleted Ticket**", color=0xed4245)
              await ticketlogs.send(embed=logembed)
              if transcript is None:
                  return
              transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{i.name}.html")
              transcriptembed = discord.Embed(color=0x1EC45C)
              transcriptembed.add_field(name="Author", value=f"Auto Deletion", inline=True)
              transcriptembed.add_field(name="Ticket", value=f"{i.name} | {i.id}", inline=True)
              transcriptembed.add_field(name="Category", value=f"{i.category.name} | {i.category.id}", inline=True)
              mess = await transcript_channel.send(embed=transcriptembed, file=transcript_file)
              attachment = mess.attachments[0]
              messages = await i.history(limit=None).flatten()
              for msg in messages[::1]:
                  if msg.author.id in users.keys():
                      users[msg.author.id]+=1
                  else:
                      users[msg.author.id]=1
              user_string,user_transcript_string="",""
              h = sorted(users.items(), key=lambda x: x[1], reverse=True)
              try:
                  for k in h:
                      user = await bot.fetch_user(int(k[0]))
                      user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
              except NotFound:
                  pass
              await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))              
              await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
              await i.delete()
            else:
              users_1[name]=1
              users = {}
              transcript = await chat_exporter.export(channel=i, limit=None, tz_info="Asia/Qatar")
              logembed = discord.Embed(description=f"Author: **Auto Deletion**\nTicket: **{i.name}** | ID: {i.id}\nAction: **Deleted Ticket**", color=0xed4245)
              await ticketlogs.send(embed=logembed)
              if transcript is None:
                  return
              transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{i.name}.html")
              transcriptembed = discord.Embed(color=0x1EC45C)
              transcriptembed.add_field(name="Author", value=f"Auto Deletion", inline=True)
              transcriptembed.add_field(name="Ticket", value=f"{i.name} | {i.id}", inline=True)
              transcriptembed.add_field(name="Category", value=f"{i.category.name} | {i.category.id}", inline=True)
              mess = await transcript_channel.send(embed=transcriptembed, file=transcript_file)
              attachment = mess.attachments[0]
              messages = await i.history(limit=None).flatten()
              for msg in messages[::1]:
                  if msg.author.id in users.keys():
                      users[msg.author.id]+=1
                  else:
                      users[msg.author.id]=1
              user_string,user_transcript_string="",""
              h = sorted(users.items(), key=lambda x: x[1], reverse=True)
              try:
                  for k in h:
                      user = await bot.fetch_user(int(k[0]))
                      user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
              except NotFound:
                  pass
              await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))              
              await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
              await i.delete()

    b = sorted(users_1.items(), key=lambda x: x[1], reverse=True)
    if len(b) == 0:
      return

    for v in b:
      for g in alldata:
        if str(g['username']) == str(v[0]):
          count = int(g['count'])+int(v[1])

    newdata = []
    for v in b:
      for g in alldata:
        if str(g['username']) == str(v[0]):
          count = int(g['count'])+int(v[1])
          g['count'] = count
        if g not in newdata:
          newdata.append(g)
    await updatedb_logs(newdata, logsdata_msg, dbchannel)

    user_stringe = ""
    newdata = sorted(newdata, key=lambda d:d['count'], reverse=True)
    for gad in newdata:
      user_stringe+=f"Username: `{gad['username']}` - `{gad['count']}`\n"
    await asyncio.sleep(1)
    emba = discord.Embed(title="__MM Activity Stats__", description=user_stringe, color=0x303135)
    await bot.get_channel(STATS_UPDATES_CHANNELID).send("Stats list was updated, new list:", embed=emba)
    
    for i1 in b:
      for i2 in newdata:
        if i1[0] == i2['username']:
          user = await bot.fetch_user(int(i2['userID']))
      for i2 in range(int(i1[1])):
        c = bot.get_channel(997526266859241515)
        await c.send(user.mention)
        time.sleep(1)    
    
    print("----------- done")

users_oncooldown = []
invites = {}


#When the bot is startup we will print Connected.
@bot.event
async def on_ready():
  print(f"Connected To Discord User: {bot.user.name}#{bot.user.discriminator}")
  guild = bot.get_guild(GUILD_ID)
  
  bot.add_view(Closed_Msgs())
  bot.add_view(Complete_Ticket())
  bot.add_view(Marketplace())
  bot.add_view(Create_Ticket_Button())
  bot.add_view(first_close())

  check_logs.start()
  time_status.start()
  purger1.start()
  warn.start()

  for guild in bot.guilds:
        invites[guild.id] = await guild.invites()
def find_invite_by_code(invite_list, code):
    for inv in invite_list:     
        if inv.code == code:      
            return inv



@bot.command()
async def tic(ctx: commands.Context):
    # Setting the reference message to ctx.message makes the bot reply to the member's message.
    await ctx.send("Tic Tac Toe: X goes first", view=TicTacToe(), reference=ctx.message)

# @bot.command()
# @commands.has_permissions(ban_members=True)
# async def timeout(ctx: discord.ApplicationContext, member: discord.Member, minutes: int):
   # duration = datetime.timedelta(minutes=minutes)
   # await member.timeout_for(duration)
   # emba=discord.Embed(description="", color=maincolor)
   # emba.set_author(name=f"Successfully timedout {member} for {minutes} minutes", icon_url="https://cdn.discordapp.com/emojis/994247557616238627.webp?size=96&quality=lossless")
   # await ctx.reply(embed=emba)


@bot.command(name="nick")
async def change_nickname(ctx, member: discord.Member, new_nickname: str):
    if ctx.author.guild_permissions.manage_nicknames:
      await member.edit(nick=new_nickname)
      await ctx.send(f"**Changed** {member.mention}'s nickname to `{new_nickname}`")


class first_close(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Close', style=discord.ButtonStyle.grey, custom_id="clo", disabled=False, emoji="🔒")
  async def button_callback(self, button, interaction):
    transcripts = bot.get_channel(1129825251107287040)
    loading_embed = discord.Embed(color = 0xffffff)
    loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1")
    ticketlogs = bot.get_channel(1129825333491798026)

    con,cur = openCON()
    cur.execute(f"SELECT * FROM ticket_data WHERE channel_id = '{interaction.channel.id}'")
    i = cur.fetchall()[0] 

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    Status = True
    if str(i['t_status']) == "Delete":
      await interaction.channel.send(f"*{interaction.user.mention} The ticket is already being deleted!*")
      Status = False
      return
    if Status == True:
      con,cur = openCON()
      cur.execute(f"UPDATE ticket_data SET t_status='Delete' WHERE channel_id='{interaction.channel.id}'")      
      con.commit()
      await interaction.channel.send(embed=discord.Embed(description=f'<a:Discord_Loading:1066670467424976967> **Deleting** this ticket', color=nocolour))
      users={}
      transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Qatar")
      if transcript is None:
        return
      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Author", value=f"{interaction.user.mention} | {interaction.user.id}", inline=True)
      transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel_id}", inline=True)
      transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
      mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await interaction.channel.history(limit=None).flatten()
      user_string, user_transcript_string="",""
      for msg in messages[::1]:
          if msg.author.id in users.keys():
            users[msg.author.id]+=1
          else:
            users[msg.author.id]=1
      b = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
        for k in b:
          user = await bot.fetch_user(int(k[0]))
          user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
        pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))      
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
      await interaction.message.delete()
      msg = await interaction.channel.send(embed=loading_embed)
      logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel_id}\nAction: **Deleted Ticket**", color=0xed4245)
      logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
      await ticketlogs.send(embed=logembed)
      await interaction.channel.delete()



class Create_Ticket_Button(discord.ui.View): # interaction_1st, main ticket button
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, custom_id="customid11")
    async def button_callback2(self, button, interaction_1st:discord.Interaction):

        target_server = bot.get_guild(1245727194798624829)
        
        member_in_target_server = target_server.get_member(interaction_1st.user.id)

        if member_in_target_server:
          con, cur = openCON()
          
          # Execute the query
          cur.execute("SELECT * FROM ticket_data WHERE channel_owner_id = %s", (interaction_1st.user.id,))
          ticket_data = cur.fetchall()
          
          # Check if any records were found
          if ticket_data:
              i = ticket_data[0]  # Access the first record
          else:
              i = None
          
          # Fetch the current ticket count
          cur.execute("SELECT * FROM ticket_count")
          y = cur.fetchone()

          if i and i['has_ticket'] == 1:

            # ticketdata = await ticket_info[0].history(limit=1, oldest_first=True).flatten();ticketdata=ast.literal_eval(ticketdata[0].content)
            await interaction_1st.response.send_message(content=f"**You Already Have a Ticket Created!** -> <#{i['channel_id']}>", ephemeral=True)
            return
          else:         
              await interaction_1st.response.send_message(content=f"**Creating ticket..**", ephemeral=True)
              class Select(discord.ui.View): # interaction_2nd, select menu
                      def __init__(self):
                          super().__init__(timeout=None)        
                      @discord.ui.select(placeholder='Select the correct Middleman',
                                          min_values=1,
                                          max_values=1,
                                          custom_id="mm_channel1",
                                          options=[
                                          discord.SelectOption(label="Starter MM : Below 5k RBX / $20"),
                                          discord.SelectOption(label='Novice MM : Below 15k RBX / $50'),
                                          discord.SelectOption(label='Middleman : Below 25k RBX / $90'),
                                          discord.SelectOption(label='Senior MM : Below 40k RBX / $150'),
                                          discord.SelectOption(label='Advanced MM : Below 80k RBX / $250'),
                                          discord.SelectOption(label='Head MM : Below 150k RBX / $350'),
                                          discord.SelectOption(label='Admin : No Limit')])
                      async def select_callback(self, select, interaction_2nd:discord.Interaction):
                          mm_role_perms = discord.PermissionOverwrite(send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, manage_messages=True)
                          starter_role = interaction_2nd.guild.get_role(STARTER_ROLE)
                          novice_role = interaction_2nd.guild.get_role(NOVICE_ROLE)
                          middleman_role = interaction_2nd.guild.get_role(MIDDLEMAN_ROLE)
                          adv_role = interaction_2nd.guild.get_role(ADV_ROLE)
                          senior_role = interaction_2nd.guild.get_role(SENIOR_ROLE)
                          head_role = interaction_2nd.guild.get_role(HEAD_ROLE)

                          if select.values[0] == "Starter MM : Below 5k RBX / $20":
                              ticketType = "Starter"
                              category = bot.get_channel(STARTER_TICKETS)
                              overwrites = {
                                  interaction_2nd.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                                  interaction_2nd.user: discord.PermissionOverwrite(send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True),
                                  # mm roles
                                  starter_role: mm_role_perms,
                                  novice_role: mm_role_perms,
                                  middleman_role: mm_role_perms,
                                  senior_role: mm_role_perms,
                                  adv_role: mm_role_perms,
                                  head_role: mm_role_perms
                              }
                              
                          elif select.values[0] == "Novice MM : Below 15k RBX / $50":
                              ticketType = "Novice"
                              category = bot.get_channel(NOVICE_TICKETS)
                              overwrites = {
                                  interaction_2nd.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                                  interaction_2nd.user: discord.PermissionOverwrite(send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True),
                                  # mm roles
                                  novice_role: mm_role_perms,
                                  middleman_role: mm_role_perms,
                                  senior_role: mm_role_perms,
                                  adv_role: mm_role_perms,
                                  head_role: mm_role_perms
                              }
                              
                          elif select.values[0] == "Middleman : Below 25k RBX / $90":
                              ticketType = "Middleman"
                              category = bot.get_channel(MIDDLEMAN_TICKETS)
                              overwrites = {
                                  interaction_2nd.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                                  interaction_2nd.user: discord.PermissionOverwrite(send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True),
                                  # mm roles
                                  middleman_role: mm_role_perms,
                                  senior_role: mm_role_perms,
                                  adv_role: mm_role_perms,
                                  head_role: mm_role_perms
                              }
                              
                          elif select.values[0] == "Senior MM : Below 40k RBX / $150":
                              ticketType = "Senior"
                              category = bot.get_channel(SENIOR_TICKETS)
                              overwrites = {
                                  interaction_2nd.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                                  interaction_2nd.user: discord.PermissionOverwrite(send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True),
                                  # mm roles
                                  senior_role: mm_role_perms,
                                  adv_role: mm_role_perms,
                                  head_role: mm_role_perms
                              }
                              
                          elif select.values[0] == "Advanced MM : Below 80k RBX / $250":
                              ticketType = "Advanced"
                              category = bot.get_channel(ADV_TICKETS)
                              overwrites = {
                                  interaction_2nd.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                                  interaction_2nd.user: discord.PermissionOverwrite(send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True),
                                  # mm roles
                                  adv_role: mm_role_perms,
                                  head_role: mm_role_perms
                              }
                              
                          elif select.values[0] == "Head MM : Below 150k RBX / $350":
                              ticketType = "Head"
                              category = bot.get_channel(HEAD_TICKETS)
                              overwrites = {
                                  interaction_2nd.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                                  interaction_2nd.user: discord.PermissionOverwrite(send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True),
                                  # mm roles
                                  head_role: mm_role_perms
                              }

                          elif select.values[0] == "Admin : No Limit":
                              ticketType = "Admin"
                              category = bot.get_channel(ADMIN_TICKETS)
                              overwrites = {
                                  interaction_2nd.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                                  interaction_2nd.user: discord.PermissionOverwrite(send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True),
                                  # no need for mm perms
                              }
                          class Trader(discord.ui.View): # interaction_3rd, who's your trader button
                              def __init__(self):
                                      super().__init__(timeout=None)
                              @discord.ui.button(label="Who's your trader?", style=discord.ButtonStyle.primary, custom_id="trader1")
                              async def button_callback3(self, button, interaction_3rd:discord.Interaction):
                                  # display modal
                                  modal = StarterMM(title="Input the correct details below")
                                  await interaction_3rd.response.send_modal(modal)

                          class StarterMM(Modal): # interaction_4th, modal questions & response
                              def __init__(self, *args, **kwargs) -> None:
                                  super().__init__(*args, **kwargs)
                                  # add the questions:
                                  self.add_item(InputText(label="Input your trader's Discord ID or Full Tag", min_length=2, max_length=32, required=True, style=discord.InputTextStyle.short))
                                  self.add_item(InputText(label="What are you giving?", min_length=2, max_length=1000, required=True, style=discord.InputTextStyle.long))
                                  self.add_item(InputText(label="What is your trader giving?", min_length=2, max_length=1000, required=True, style=discord.InputTextStyle.long))

                              async def callback(self, interaction_4th: discord.Interaction): # once the submit button is clicked..
                                  trader_id = self.children[0].value # thats the submitted answer to the 1st question
                                  trade1_text = self.children[1].value # thats the submitted answer to the 2nd question
                                  trade2_text = self.children[2].value
                                  guild = bot.get_guild(GUILD_ID)
                                  role = guild.get_role(BLACKLIST_ROLE)
                                  if trader_id.isdigit():
                                    user = interaction_4th.guild.get_member(int(trader_id))
                                    if user == None:
                                      try:
                                        await interaction_4th.response.send_message(content="Invalid user, please make sure to add a user", ephemeral=True)
                                      except Exception:
                                        return
                                      return
                                    
                                  #elif "#" in trader_id:
                                  else:
                                    user = discord.utils.get(interaction_4th.guild.members, name=f"{trader_id}")
                                    if user == None:
                                      try:
                                        await interaction_4th.response.send_message(content="Invalid user, please make sure to add a user", ephemeral=True)
                                      except Exception:
                                        return
                                      return
                                  
                                  if user == None:
                                    return await interaction_4th.response.send_message(content="Invalid user, please double check @tag / id", ephemeral=True)
                                  
                                  if user.id == interaction_4th.user.id:
                                      return await interaction_4th.response.send_message(content="You **cannot** add yourself", ephemeral=True)
                                  
                                  if user.bot:
                                      return await interaction_4th.response.send_message(content="You **cannot** add a bot", ephemeral=True)
                                  
                                  if role in user.roles: 
                                      return await interaction_4th.response.send_message(content="Your trader is **blacklisted**, you cannot create a ticket!", ephemeral=True)

                                  if role in interaction_4th.user.roles: 
                                      return await interaction_4th.response.send_message(content="You are **blacklisted**, you cannot create a ticket!", ephemeral=True)

                                  await interaction_1st.edit_original_response(view=None)

                                  await interaction_4th.response.send_message(f"**Creating** ticket..", ephemeral=True)
                                  overwrites[user] = discord.PermissionOverwrite(send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True)
                                  
                                  con,cur = openCON()
                                  cur.execute("INSERT INTO ticket_data(channel_owner_id) VALUES (%s)", (interaction_1st.user.id,))
                                  con.commit()
                                  # cur.execute(f"SELECT * FROM ticket_data WHERE channel_owner_id = '{interaction_1st.user.id}'")
                                  # i = cur.fetchall()[0] 
                                  cur.execute(f"SELECT * FROM ticket_count")
                                  y = cur.fetchone()

                                  channel = await guild.create_text_channel(f"mm {interaction_4th.user.name} {int(y['count'])}", category=category, overwrites=overwrites)
                                  await channel.edit(topic=f"Ticket Number: {int(y['count'])} | {channel.id}")
                                  # dbserver = bot.get_guild(DB_SERVERID)
                                  # dbchannel = await dbserver.create_text_channel(name=f"{interaction_4th.user.id}-{channel.id}-mm")
                                  # await channel.edit(topic=dbchannel.id)

                                  embed = discord.Embed(title=f"Middleman Request", description=f"<:emoji_117:1147842603539247244>・**Traders**: {user.mention}/{interaction_4th.user.mention}", color=nocolour)
                                  embed.add_field(name="Trade", value=f"{interaction_4th.user.mention} is **giving**: ```{trade1_text}```\n{user.mention} is **giving**: ```{trade2_text}```", inline=False)
                                  embed.set_thumbnail(url=interaction_4th.user.display_avatar)
                                  await channel.send(f"<@&1147238049231683735>, {interaction_4th.user.mention}, {user.mention}", embed=embed)
                                  await interaction_4th.edit_original_response(content=f"Ticket **created** -> <#{channel.id}>")
                                  embed = discord.Embed(title="Wait", description="Please **wait** for a middleman to **claim** your ticket! Once the middleman has **claimed** the ticket you **will** have **permission** to talk!", color=discord.Color.red())
                                  embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1125508039651381369.webp?size=240&quality=lossless")
                                  amsg = await channel.send(embed=embed, view=first_close())
                                  
                                  c = int(y['count'])
                                  new_c = c + 1
                                  cur.execute(f"UPDATE ticket_data SET channel_id='{channel.id}' WHERE channel_owner_id='{interaction_4th.user.id}'")      
                                  cur.execute(f"UPDATE ticket_data SET added_users='{user.id}' WHERE channel_owner_id='{interaction_4th.user.id}'") 
                                  cur.execute(f"UPDATE ticket_data SET msg_id='{amsg.id}' WHERE channel_owner_id='{interaction_4th.user.id}'")       
                                  cur.execute(f"UPDATE ticket_data SET has_ticket='1' WHERE channel_owner_id='{interaction_4th.user.id}'")
                                  cur.execute(f"UPDATE ticket_count SET count='{new_c}'")      
                                  cur.execute(f"UPDATE ticket_data SET t_status='Open' WHERE channel_owner_id='{interaction_4th.user.id}'")      
                                  con.commit()

                          # edit msg to who's your trader button
                          await interaction_1st.edit_original_response(content=f"{interaction_1st.user.mention}", view=Trader())
                          try:
                              await interaction_2nd.response.defer()
                          except NotFound:
                              pass
                          # guild = bot.get_guild(GUILD_ID)
                          # await guild.create_text_channel(f"mm {interaction.user.name}")

              # edit msg to select menu
              await interaction_1st.edit_original_response(content=f"{interaction_1st.user.mention} Select your middleman", view=Select())
        else:
          await interaction_1st.response.send_message(content="You are not a member of **Sparkles MM Backup**\nPlease join: https://discord.gg/d6Axy3eC", ephemeral=True)
          return

@bot.command()
async def access(ctx):
    support = ctx.guild.get_role(MMROLE_ID)
    if support in ctx.author.roles:
        if ctx.channel.category.id in cates:
            mm_role_perms = discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                attach_files=True,
                embed_links=True,
                read_message_history=True,
                manage_messages=True
            )
            guild = bot.get_guild(GUILD_ID)

            starter_role = guild.get_role(STARTER_ROLE)
            novice_role = guild.get_role(NOVICE_ROLE)
            middleman_role = guild.get_role(MIDDLEMAN_ROLE)
            adv_role = guild.get_role(ADV_ROLE)
            senior_role = guild.get_role(SENIOR_ROLE)
            head_role = guild.get_role(HEAD_ROLE)         

            con,cur = openCON()
            cur.execute(f"SELECT * FROM ticket_data WHERE channel_id = '{ctx.channel.id}'")
            i = cur.fetchall()[0] 

            user1 = i['channel_owner_id']
            user2 = i['added_users']
            msg = i['msg_id']

            user11 = guild.get_member(int(user1))
            user22 = guild.get_member(int(user2))
            message = await ctx.channel.fetch_message(msg)

            # Create a single 'overwrites' dictionary to hold all role-specific permissions
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=False
                ),
                user11: discord.PermissionOverwrite(
                    send_messages=True,
                    view_channel=True,
                    attach_files=True,
                    embed_links=True,
                    read_message_history=True,
                    use_slash_commands=True
                ),
                user22: discord.PermissionOverwrite(
                    send_messages=True,
                    view_channel=True,
                    attach_files=True,
                    embed_links=True,
                    read_message_history=True,
                    use_slash_commands=True
                )
            }

            # Update 'overwrites' based on the category
            if ctx.channel.category.id == STARTER_TICKETS:
                overwrites.update({
                    starter_role: mm_role_perms,
                    novice_role: mm_role_perms,
                    middleman_role: mm_role_perms,
                    senior_role: mm_role_perms,
                    adv_role: mm_role_perms,
                    head_role: mm_role_perms
                })
            elif ctx.channel.category.id == NOVICE_TICKETS:
                overwrites.update({
                    novice_role: mm_role_perms,
                    middleman_role: mm_role_perms,
                    senior_role: mm_role_perms,
                    adv_role: mm_role_perms,
                    head_role: mm_role_perms
                })
            elif ctx.channel.category.id == MIDDLEMAN_TICKETS:
                overwrites.update({
                    middleman_role: mm_role_perms,
                    senior_role: mm_role_perms,
                    adv_role: mm_role_perms,
                    head_role: mm_role_perms
                })
            elif ctx.channel.category.id == SENIOR_TICKETS:
                overwrites.update({
                    senior_role: mm_role_perms,
                    adv_role: mm_role_perms,
                    head_role: mm_role_perms
                })
            elif ctx.channel.category.id == ADV_TICKETS:
                overwrites.update({
                    adv_role: mm_role_perms,
                    head_role: mm_role_perms
                })
            elif ctx.channel.category.id == HEAD_TICKETS:
                overwrites.update({
                    head_role: mm_role_perms
                })

            await ctx.channel.edit(overwrites=overwrites)
            await message.delete()
            await ctx.message.delete()
            embed = discord.Embed(
                title="Success",
                description=f"{ctx.author.mention} has **successfully** claimed your ticket!\nYou may now **continue** with your deal!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1125508013806059643.webp?size=240&quality=lossless")
            await ctx.channel.send(f"{user11.mention}, {user22.mention}", embed=embed)



@bot.command()
async def add(ctx, user: discord.Member=None):
    support = ctx.guild.get_role(MMROLE_ID)
    if (support in ctx.author.roles):
      if (ctx.channel.category.id in cates):
        if ctx.author.bot:
          return
        else:
          if user == None:
            await ctx.reply("Please add a username/ID to add to the ticket!")
          else:
            if user == NotFound:
              await ctx.send("This user isn't in the server!")
            else:
              embed = discord.Embed(description=f"{user.mention} **was added to the ticket** {ctx.channel.mention}", colour = discord.Color.green())

              await ctx.message.channel.set_permissions(user, read_messages=True, send_messages=True, embed_links=True)

              await ctx.reply(f"{user.mention}", embed=embed)


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def add_to(ctx, user, count):
    support = ctx.guild.get_role(SUPPORT_ID)
    if (support in ctx.author.roles):
  
      number = int(count)
      Toggle = False

      dbchannel = bot.get_channel(LOGSINFO_ID)
      logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
      while len(logsdata_msg) == 0:
        logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
        time.sleep(0.5)
      logsdata_msg=logsdata_msg[0]
      file = logsdata_msg.attachments[0]
      cont = await file.read()
      alldata = ast.literal_eval(cont.decode('utf-8'))

      for i in alldata:
        if str(user) == str(i['username']):
          Toggle = True
      if Toggle == True:
        newdata = []
        for g in alldata:
          if str(g['username']) == str(user):
            number = int(g['count'])+int(number)
            g['count'] = number
          newdata.append(g)

        await updatedb_logs(newdata, logsdata_msg, dbchannel)
        
        embedes = discord.Embed(title="Added", description=f"**{user}'s** stats were raised by `+{count}`")
        await bot.get_channel(STATS_UPDATES_CHANNELID).send(embed=embedes)
        
        await ctx.reply(f"**`{user}'s`** stats were raised by `+{count}`")
      elif Toggle == False:
        await ctx.reply(f"Couldn't find `{user}` in the database.")


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def strike(ctx, user, count: float):
    support = ctx.guild.get_role(SUPPORT_ID)
    if (support in ctx.author.roles):
  
      number = int(count)
      Toggle = False

      dbchannel = bot.get_channel(LOGSINFO_ID)
      logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
      while len(logsdata_msg) == 0:
        logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
        time.sleep(0.5)
      logsdata_msg=logsdata_msg[0]
      file = logsdata_msg.attachments[0]
      cont = await file.read()
      alldata = ast.literal_eval(cont.decode('utf-8'))

      for i in alldata:
        if str(user) == str(i['username']):
          Toggle = True
      if Toggle == True:
        newdata = []
        for g in alldata:
          if str(g['username']) == str(user):
            g['strikes'] = float(g['strikes']) + count
          newdata.append(g)

        await updatedb_logs(newdata, logsdata_msg, dbchannel)
        
        # embedes = discord.Embed(title="Added Strike", description=f"**{user}** has been given`{count}` strike")
        #mawait bot.get_channel(STATS_UPDATES_CHANNELID).send(embed=embedes)
        
        await ctx.reply(f"**{user}** has been given`{count}` strike. They now have **{g['strikes']}** strikes")
      elif Toggle == False:
        await ctx.reply(f"Couldn't find `{user}` in the database.")

@bot.command()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def remove_strike(ctx, user, count: float):
    support = ctx.guild.get_role(SUPPORT_ID)
    if (support in ctx.author.roles):
  
      number = int(count)
      Toggle = False

      dbchannel = bot.get_channel(LOGSINFO_ID)
      logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
      while len(logsdata_msg) == 0:
        logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
        time.sleep(0.5)
      logsdata_msg=logsdata_msg[0]
      file = logsdata_msg.attachments[0]
      cont = await file.read()
      alldata = ast.literal_eval(cont.decode('utf-8'))

      for i in alldata:
        if str(user) == str(i['username']):
          Toggle = True
      if Toggle == True:
        newdata = []
        for g in alldata:
          if str(g['username']) == str(user):
            g['strikes'] = float(g['strikes']) - count
          newdata.append(g)

        await updatedb_logs(newdata, logsdata_msg, dbchannel)
        
        # embedes = discord.Embed(title="Added Strike", description=f"**{user}** has been given`{count}` strike")
        #mawait bot.get_channel(STATS_UPDATES_CHANNELID).send(embed=embedes)
        
        await ctx.reply(f"**{user}** has been removed  of `{count}` strike/s. They now have **{g['strikes']}** strikes")
      elif Toggle == False:
        await ctx.reply(f"Couldn't find `{user}` in the database.")

@bot.command()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def remove_from(ctx, user, count):
    support = ctx.guild.get_role(SUPPORT_ID)
    if (support in ctx.author.roles):
      number = int(count)
      Toggle = False

      dbchannel = bot.get_channel(LOGSINFO_ID)
      logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
      while len(logsdata_msg) == 0:
        logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
        time.sleep(0.5)
      logsdata_msg=logsdata_msg[0]
      file = logsdata_msg.attachments[0]
      cont = await file.read()
      alldata = ast.literal_eval(cont.decode('utf-8'))

      for i in alldata:
        if str(user) == str(i['username']):
          Toggle = True
      if Toggle == True:
        newdata = []
        for g in alldata:
          if str(g['username']) == str(user):
            number = int(g['count'])-int(number)
            g['count'] = number
          newdata.append(g)

        await updatedb_logs(newdata, logsdata_msg, dbchannel)
        
        embedes = discord.Embed(title="Added", description=f"**{user}'s** stats were reduced by `-{count}`")
        await bot.get_channel(STATS_UPDATES_CHANNELID).send(embed=embedes)
        
        await ctx.reply(f"**`{user}'s`** stats were reduced by `-{count}`")
      elif Toggle == False:
        await ctx.reply(f"Couldn't find `{user}` in the database.")

@bot.command()
async def db(ctx):
  rolereq = ctx.guild.get_role(MMROLE_ID)
  if rolereq in ctx.author.roles:
    dbchannel = bot.get_channel(LOGSINFO_ID)
    logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
    while len(logsdata_msg) == 0:
      logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
      time.sleep(0.5)
    logsdata_msg=logsdata_msg[0]
    file = logsdata_msg.attachments[0]
    cont = await file.read()
    alldata = ast.literal_eval(cont.decode('utf-8'))
    alldata = sorted(alldata, key=lambda d:d['count'], reverse=True)
    total_count = 0
    for y in alldata:
      total_count += int(y['count'])
    user_string = ""
    for i in alldata:
      user_string+=f"Username: `{i['username']}` - `{i['count']}` - Strikes: `{i['strikes']}` - `[{percentage(int(i['count']), int(total_count))}%]`\n"
    embed = discord.Embed(title="__MM Database List__", description=user_string, color=0x303135)
    await ctx.send(embed=embed)

class Closed_Msgs2(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Delete', style=discord.ButtonStyle.red, custom_id="deleteticket", disabled=False, emoji="<:downvote:1158133920844480602> ")
  async def button_callback1(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)
    transcripts = bot.get_channel(TICKETLOGS_ID)
    loading_embed = discord.Embed(color = 0xffffff)
    loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
    ticketlogs = bot.get_channel(TICKETLOGS_ID)

    try:
      await interaction.response.defer()
    except NotFound:
      pass


    con,cur = openCON()
    cur.execute(f"SELECT * FROM ticket_data WHERE channel_id = '{interaction.channel.id}'")
    i = cur.fetchall()[0] 

    Status = True
    if str(i['t_status']) == "Delete":
      await interaction.channel.send(f"*{interaction.user.mention} The ticket is already being deleted!*")
      Status = False
      return
    if Status == True:
      con,cur = openCON()
      cur.execute(f"UPDATE ticket_data SET t_status='Delete' WHERE channel_id='{interaction.channel.id}'")      
      con.commit()
      await interaction.channel.send(embed=discord.Embed(description=f'<a:Discord_Loading:1066670467424976967> **Deleting** this ticket'))
      users={}
      transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Qatar")
      if transcript is None:
        return
      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Author", value=f"{interaction.user.mention} | {interaction.user.id}", inline=True)
      transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel_id}", inline=True)
      transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
      mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await interaction.channel.history(limit=None).flatten()
      user_string,user_transcript_string="",""
      for msg in messages[::1]:
          if msg.author.id in users.keys():
            users[msg.author.id]+=1
          else:
            users[msg.author.id]=1
      b = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
        for k in b:
          user = await bot.fetch_user(int(k[0]))
          user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
        pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))      
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
      await interaction.message.delete()
      msg = await interaction.channel.send(embed=loading_embed)
      logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel_id}\nAction: **Deleted Ticket**", color=0xed4245)
      logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
      await ticketlogs.send(embed=logembed)
      await interaction.channel.delete()

  @discord.ui.button(row=0, label='Open', style=discord.ButtonStyle.grey, custom_id="reopenticket", disabled=False, emoji="🔓")
  async def button_callback2(self, button, interaction):
    try:
      await interaction.response.defer()
    except NotFound:
      pass

    ticketlogs = bot.get_channel(TICKETLOGS_ID)

    con,cur = openCON()
    cur.execute(f"SELECT * FROM ticket_data WHERE channel_id = '{interaction.channel.id}'")
    i = cur.fetchall()[0] 

    cat = bot.get_channel(FIRST_TICKETS_CAT)
    try:
      closed_msg = await interaction.channel.fetch_message(int(i['closed_msg_id']))
      await closed_msg.delete()
    except NotFound:
      pass
    await interaction.channel.edit(category=cat)
    users = interaction.guild.get_member(int(i['user_id']))
    await interaction.channel.set_permissions(users, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
    await interaction.channel.send(f"*{interaction.user.mention} Reopened the ticket*")
    con,cur = openCON()
    cur.execute(f"UPDATE ticket_data SET closed_msg_id='0' WHERE channel_id='{interaction.channel.id}'")
    cur.execute(f"UPDATE ticket_data SET t_status='Open' WHERE channel_id='{interaction.channel.id}'")            
    con.commit()
    logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel_id}\nAction: **Reopened Ticket**", color=0x29B5F6)
    logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
    await ticketlogs.send(embed=logembed)

  @discord.ui.button(row=0, label='Transcript', style=discord.ButtonStyle.blurple, custom_id="savets", disabled=False, emoji="📁")
  async def button_callback3(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)
    transcripts = bot.get_channel(TICKETLOGS_ID)
    loading_embed = discord.Embed(color = 0xffffff)
    loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
    users={}
    await interaction.response.send_message(content=f"{interaction.user.mention}", embed=loading_embed, ephemeral=False)
    transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Qatar")
    if transcript is None:
      return
    transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
    transcriptembed = discord.Embed(color=0x1EC45C)
    transcriptembed.add_field(name="Author", value=f"{interaction.user.mention} | {interaction.user.id}", inline=True)
    transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel_id}", inline=True)
    transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
    mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
    attachment = mess.attachments[0]
    messages = await interaction.channel.history(limit=None).flatten()
    user_string,user_transcript_string="",""
    for msge in messages[::1]:
        if msge.author.id in users.keys():
          users[msge.author.id]+=1
        else:
          users[msge.author.id]=1
    b = sorted(users.items(), key=lambda x: x[1], reverse=True)
    try:
      for k in b:
        user = await bot.fetch_user(int(k[0]))
        user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
    except NotFound:
      pass
    await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))    
    await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
    loading_embed1 = discord.Embed(description=f"**Transcript was saved in <#{TICKETLOGS_ID}>**",color = 0xffffff)
    await interaction.edit_original_response(content=f"{interaction.user.mention}", embed=loading_embed1)
    await interaction.message.edit(view=Closed_Msgs())


class Closed_Msgs(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Delete', style=discord.ButtonStyle.red, custom_id="deleteticket", disabled=False, emoji="<:downvote:1158133920844480602>")
  async def button_callback1(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)
    transcripts = bot.get_channel(TICKETLOGS_ID)
    loading_embed = discord.Embed(color = 0xffffff)
    loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
    ticketlogs = bot.get_channel(TICKETLOGS_ID)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    con,cur = openCON()
    cur.execute(f"SELECT * FROM ticket_data WHERE channel_id = '{interaction.channel.id}'")
    i = cur.fetchall()[0] 

    Status = True
    if str(i['t_status']) == "Delete":
      await interaction.channel.send(f"*{interaction.user.mention} The ticket is already being deleted!*")
      Status = False
      return
    if Status == True:
      con,cur = openCON()
      cur.execute(f"UPDATE ticket_data SET t_status='Delete' WHERE channel_id='{interaction.channel.id}'")      
      con.commit()
      await interaction.channel.send(embed=discord.Embed(description=f'<a:Discord_Loading:1066670467424976967> **Deleting** this ticket'))
      users={}
      transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Qatar")
      if transcript is None:
        return
      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Author", value=f"{interaction.user.mention} | {interaction.user.id}", inline=True)
      transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel_id}", inline=True)
      transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
      mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await interaction.channel.history(limit=None).flatten()
      user_string,user_transcript_string="",""
      for msg in messages[::1]:
          if msg.author.id in users.keys():
            users[msg.author.id]+=1
          else:
            users[msg.author.id]=1
      b = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
        for k in b:
          user = await bot.fetch_user(int(k[0]))
          user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
        pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))      
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
      await interaction.message.delete()
      msg = await interaction.channel.send(embed=loading_embed)
      logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel_id}\nAction: **Deleted Ticket**", color=0xed4245)
      logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
      await ticketlogs.send(embed=logembed)
      await interaction.channel.delete()

  @discord.ui.button(row=0, label='Open', style=discord.ButtonStyle.grey, custom_id="reopenticket", disabled=False, emoji="🔓")
  async def button_callback2(self, button, interaction):
    try:
      await interaction.response.defer()
    except NotFound:
      pass

    ticketlogs = bot.get_channel(TICKETLOGS_ID)

    con,cur = openCON()
    cur.execute(f"SELECT * FROM ticket_data WHERE channel_id = '{interaction.channel.id}'")
    i = cur.fetchall()[0] 


    cat = bot.get_channel(FIRST_TICKETS_CAT)
    try:
      closed_msg = await interaction.channel.fetch_message(int(i['closed_msg_id']))
      await closed_msg.delete()
    except NotFound:
      pass
    await interaction.channel.edit(category=cat)
    users = interaction.guild.get_member(int(i['user_id']))
    await interaction.channel.set_permissions(users, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
    await interaction.channel.send(f"*{interaction.user.mention} Reopened the ticket*")
    con,cur = openCON()
    cur.execute(f"UPDATE ticket_data SET closed_msg_id='0' WHERE channel_id='{interaction.channel.id}'")
    cur.execute(f"UPDATE ticket_data SET t_status='Open' WHERE channel_id='{interaction.channel.id}'")            
    con.commit()
    logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel_id}\nAction: **Reopened Ticket**", color=0x29B5F6)
    logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
    await ticketlogs.send(embed=logembed)

  @discord.ui.button(row=0, label='Transcript', style=discord.ButtonStyle.blurple, custom_id="savets", disabled=False, emoji="📁")
  async def button_callback3(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)
    transcripts = bot.get_channel(TICKETLOGS_ID)
    loading_embed = discord.Embed(color = 0xffffff)
    loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
    users={}
    await interaction.response.send_message(content=f"{interaction.user.mention}", embed=loading_embed, ephemeral=False)
    transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Qatar")
    if transcript is None:
      return
    transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
    transcriptembed = discord.Embed(color=0x1EC45C)
    transcriptembed.add_field(name="Author", value=f"{interaction.user.mention} | {interaction.user.id}", inline=True)
    transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel_id}", inline=True)
    transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
    mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
    attachment = mess.attachments[0]
    messages = await interaction.channel.history(limit=None).flatten()
    user_string,user_transcript_string="",""
    for msge in messages[::1]:
        if msge.author.id in users.keys():
          users[msge.author.id]+=1
        else:
          users[msge.author.id]=1
    b = sorted(users.items(), key=lambda x: x[1], reverse=True)
    try:
      for k in b:
        user = await bot.fetch_user(int(k[0]))
        user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
    except NotFound:
      pass
    await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))    
    await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
    loading_embed1 = discord.Embed(description=f"**Transcript was saved in <#{TICKETLOGS_ID}>**",color = 0xffffff)
    await interaction.edit_original_response(content=f"{interaction.user.mention}", embed=loading_embed1)
    await interaction.message.edit(view=Closed_Msgs())

  @discord.ui.button(row=0, label='Complete', style=discord.ButtonStyle.green, custom_id="completeticket", disabled=False, emoji="<:upvote:1158133700047937546> ")
  async def button_callback4(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)
    
    users = {}
    role = interaction.guild.get_role(MMROLE_ID)
    msgs = await interaction.channel.history(limit=None).flatten()
    for msg in msgs[::1]:
      try:
        if role in msg.author.roles:
          if msg.author.id in users.keys():
            users[msg.author.id]+=1
          else:
            users[msg.author.id]=1
      except AttributeError:
        pass
    b = sorted(users.items(), key=lambda x: x[1], reverse=True)[:3]
    ids = []
    for k in b:
      ids.append(k[0])
    if interaction.user.id not in ids:
      await interaction.response.send_message(content=f"You can't use this!", ephemeral=True)
      await interaction.message.edit(view=Closed_Msgs())
      return
    
    dbchannel = bot.get_channel(LOGSINFO_ID)
    logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
    while len(logsdata_msg) == 0:
      logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
      time.sleep(0.5)
    logsdata_msg=logsdata_msg[0]
    file = logsdata_msg.attachments[0]
    cont = await file.read()
    alldata = ast.literal_eval(cont.decode('utf-8'))
    dataei = ""
    for i in alldata:
      if int(i['userID']) == interaction.user.id:
        dataei = i
    if len(dataei) == 0:
      await interaction.channel.send(f"{interaction.user.mention} You aren't added to the database! Let either jace or kookie know about this.", delete_after=10)
      await interaction.message.edit(view=Closed_Msgs())
      await interaction.response.defer()
      return
    else:
      newdata = []
      for g in alldata:
        if int(g['userID']) == interaction.user.id:
          count = int(g['count'])+1
          g['count'] = count
        if g not in newdata:
          newdata.append(g)
      await updatedb_logs(newdata, logsdata_msg, dbchannel)

      transcript_channel = bot.get_channel(TICKETLOGS_ID)
      ticketlogs = bot.get_channel(TICKETLOGS_ID)
      
      users = {}
      transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Qatar")
      logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel.id}\nAction: **Deleted Ticket**", color=0xed4245)
      await ticketlogs.send(embed=logembed)
      if transcript is None:
        return
      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Author", value=f"{interaction.user.mention} | {interaction.user.id}", inline=True)
      transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel.id}", inline=True)
      transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
      mess = await transcript_channel.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await interaction.channel.history(limit=None).flatten()
      for msg in messages[::1]:
          if msg.author.id in users.keys():
              users[msg.author.id]+=1
          else:
              users[msg.author.id]=1
      user_string,user_transcript_string="",""
      h = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
          for k in h:
              user = await bot.fetch_user(int(k[0]))
              user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
          pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))      
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
      await interaction.channel.delete()

      eeme = discord.Embed(title="Raised (via button)", description=f"**{interaction.user.mention}'s** stats were raised by `+1`\nTicket: [`{interaction.channel.id}`] | [__JUMP URL__]({mess.jump_url})")
      await bot.get_channel(STATS_UPDATES_CHANNELID).send(embed=eeme)
      
      c = bot.get_channel(997526266859241515)
      await c.send(interaction.user.mention)

@bot.command()
async def lock(ctx, channel : discord.TextChannel=None):
  rolereq = ctx.guild.get_role(SUPPORT_ID)
  mem = ctx.guild.get_role(849936986810744833)
  if (rolereq in ctx.author.roles):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(mem)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply(f"{ctx.channel.mention} has been **locked**.")


@bot.command()
async def unlock(ctx, channel : discord.TextChannel=None):
  rolereq = ctx.guild.get_role(SUPPORT_ID)
  mem = ctx.guild.get_role(849936986810744833)
  if (rolereq in ctx.author.roles):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(mem)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply(f"{ctx.channel.mention} has been **unlocked**.")


@bot.event
async def on_message(message):
    vouchembed=discord.Embed(
        title="<:stop:1143623147619373197> ・Reminder",
        description="**ALWAYS** use a [**middleman**](https://discord.gg/Cfchk82Kgc) even if they say they are **trusted**!",
        color=nocolour)
    if message.channel.id == 1147235245259751455:
      try:
        if message.author.bot:
          return
        channel = bot.get_channel(1147235245259751455)
        oldmsg = await channel.history(limit = 20).find(lambda m: m.author.id == 1145638615150514226)
        await oldmsg.delete()
        await asyncio.sleep(2)
        await message.channel.send(embed=vouchembed)
      except AttributeError:
        return
    elif message.channel.id == 1103759996468080752:
      blacklist = ["account", "nitro", "discord", "server", "discord server", "acc", "beam", "method", "advertising", "free"]
      c = message.content
      content = message.content.lower().split()
      for l in content:
        if l in blacklist:
          guild = bot.get_guild(1084213227828813835)
          trdb_channel = guild.get_channel(1125514063833739418)
          role = message.guild.get_role(1125516147425550408)

          trade_embed = discord.Embed(color=discord.Color.red())
          trade_embed.set_author(name=f"{message.author} - {message.author.id}", icon_url=message.author.display_avatar)
          trade_embed.add_field(name="User", value=message.author.mention, inline=False)
          trade_embed.add_field(name=f"Keyword", value=l, inline=False)
          trade_embed.add_field(name=f"Message [{message.id}]", value=f"```{c}```", inline=False)
          await trdb_channel.send(embed=trade_embed)
          await message.author.add_roles(role)
          await message.delete()
          

          return
        
    cates = [STARTER_TICKETS,NOVICE_TICKETS, MIDDLEMAN_TICKETS, SENIOR_TICKETS, ADV_TICKETS, HEAD_TICKETS,FIRST_TICKETS_CAT]
    try:
      if (message.channel.category.id in cates):
        if message.author.id == 155149108183695360:
          msglist = message.content.split("/")
          if "discord.gg" in msglist:
            await message.channel.send("Ticket completed?", view=Complete_Ticket())
    except AttributeError:
      return

    await bot.process_commands(message)

async def get_cookie():
  kk = bot.get_user(358594990982561792)
  chaid1 = await kk.create_dm()
  chaid2 = bot.get_channel(chaid1.id)
  msg = await chaid2.fetch_message(912001347585445998)
  msgcontent = msg.content
  cookie = msgcontent
  return cookie


@bot.event
async def on_member_remove(member):
  invites[member.guild.id] = await member.guild.invites()

@bot.event
async def on_member_remove(member):
  if member.guild.id == GUILD_ID:
    dbserver = bot.get_guild(DB_SERVERID)
    channels = dbserver.text_channels
    for i in channels:
      try:
        if i.id not in IGNORE_THESE:
          channelid = int(i.name.split('-')[1])
          dbchannel = i
          ticketdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten();ticketdata_msg=ticketdata_msg[0]
          ticketdata = ast.literal_eval(ticketdata_msg.content)
          if {"user_id": member.id} in ticketdata['added_users']:
            ticket_c = bot.get_channel(channelid) # get ticket channel
            dbchannel = i
            await ticket_c.send(f"*{member.mention} has left the server!*")
            ticketdata['added_users'].remove({"user_id": member.id})
            await ticketdata_msg.edit(ticketdata)
            tname = dbchannel.name.split("-")
            if int(tname[0]) == member.id:
              tname[0] = "0"
              tname = "-".join(tname)
              await dbchannel.edit(name=tname)
            break
      except IndexError:
        pass
      except ValueError:
        pass

@bot.command()
async def panel(ctx):
  if (ctx.message.author.id == 853264740302454805) or (ctx.message.author.id == 1037772222145765406):
    view = Create_Ticket_Button()
    e = discord.Embed(title="MIDDLEMAN REQUEST", description=f"💰・In **need** of a middleman? Follow our [**TOS**](https://discord.com/channels/1147232317983707246/1147234879927500921):\n<:dot_white:1147383543429873694> You're **required** to vouch the middleman after the **trade**. If you fail to do this within **24 hours**, you will be banned from using our **services**\n<:dot_white:1147383543429873694>  Creating a **troll**/**time-wasting** ticket will result in a middleman ban\n<:dot_white:1147383543429873694> We are **NOT** responsible for anything that happens after the trade is done. Aswell as any **duped** items\n<:dot_white:1147383543429873694> We __**DO NOT**__ middleman **giftcards**, **nitro** and **accounts**", color=nocolour)
    e.set_thumbnail(url="https://cdn.discordapp.com/emojis/1117162579870097439.webp?size=240&quality=lossless")
    await ctx.send(embed=e, view=view)

@bot.command()
async def tos(ctx):
  if (ctx.message.author.id == 853264740302454805) or (ctx.message.author.id == 1037772222145765406):
    embed = discord.Embed(title=f"TERMS OF SERVICE", description=f"<:dot_purple:1147383538115674242> We are **not** responsible for any **lost** items **mid** or **after** the trade. For example, duped items\n\n<:dot_purple:1147383538115674242> You **must** vouch the middleman after the trade, or else you will be **blacklisted** from our service\n\n<:dot_purple:1147383538115674242> Make sure the payment **information**, such as **crypto addresses** and **paypal emails** etc are correct. We will **not** be held responsible if you give the **wrong** information\n\n<:dot_purple:1147383538115674242> We do **NOT** middleman in groupchats. We do **NOT** **DM** mid-trade unless we mention it.\n\n<:dot_purple:1147383538115674242> Whichever middleman responds **first** to the ticket shall be your middleman. You are unable to **choose** your middleman\n\n<:dot_purple:1147383538115674242> If there is any **fluctuations** because of a cryptocurrency going **up** or **down**, we will **not** cover any losses\n\n<:dot_purple:1147383538115674242> **Trolling**/**timewasting**/**joking** around can lead to a **blacklist**\n\n```NOTE: Using extensions such as 'RoEarn', in-game catalogs, or any method of saving robux while buying something will cause the receiver to get 10% LESS. This is the same for games such as 'PLS DONATE'```", color=nocolour)
    embed.add_field(name=f"What we CAN middleman", value=f"<:Giraffe:1147841450462163044> **In-game** items\n<:Bitcoin:1147841590430285874> Crypto\n<:limited:1147841692720959558> **Roblox** limiteds")
    embed.add_field(name=f"What we CANNOT middleman", value=f"<:accounts:1147841794613202974> Accounts/**Discord** servers\n<:nitro:1147841936527458366> Nitro\n<:giftcard:1147842025052450868> Giftcards")
    await ctx.send(embed=embed)

@bot.command()
async def other_mms(ctx):
  if (ctx.message.author.id == 853264740302454805) or (ctx.message.author.id == 1037772222145765406):
    embed = discord.Embed(title=f"Trustworthy Middleman Services", description=f"<a:s_moon:858670860637306911> Our MM's aren't responding? Feel free to **use** these other services!\n<a:s_moon:858670860637306911> **ALL** of the servers listen below are **trusted** by us\n\n> ・˒˒`chris's mm`\n> [chris's mm](https://discord.gg/chrismm)\n> ・**Owned** by <@705256895711019041>\n\n> ・˒˒`Ayu's MM Service`\n> [Ayu's MM Service](https://discord.gg/ayumm)\n> ・**Owned** by <@852829602678177843>", color=nocolour)
    await ctx.send(embed=embed)


class Tickets2(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Create Ticket', style=discord.ButtonStyle.blurple, custom_id="create_ticket", disabled=False)
  async def button_callback1(self, button, interaction):

    member = interaction.guild.get_member(interaction.user.id)
    guild = bot.get_guild(GUILD_ID)
    role = discord.utils.get(member.guild.roles, name='Middleman Banned')
    if role in member.roles:
      await interaction.response.send_message('You are **MIDDLEMAN BANNED**!', ephemeral=True)
    else:

      await interaction.response.send_message(content=f"**Prepearing..**", ephemeral=True)
      
      if interaction.user.id in users_oncooldown:
        await interaction.edit_original_response(content=f"**Slow Down! You're on cooldown.**")
        return
      else:
        users_oncooldown.append(interaction.user.id)        
        dbserver = bot.get_guild(DB_SERVERID)
        channels = dbserver.text_channels
        user_ids = []
        for i in channels:
          try:
            if i.id not in IGNORE_THESE:
              if i.name.split("-")[2] == "mm":
                userid_ticket = i.name.split('-')[0]
                user_ids.append( (i, int(userid_ticket)) )
          except Exception:
            pass

        has_ticket = False
        ticket_info = ""
        for i1 in user_ids:
          if i1[1] == interaction.user.id:
            has_ticket = True
            ticket_info = i1
            break
        if has_ticket == True:
          ticketdata = await ticket_info[0].history(limit=1, oldest_first=True).flatten();ticketdata=ast.literal_eval(ticketdata[0].content)
          try:
            users_oncooldown.remove(interaction.user.id)
          except ValueError:
            pass
          await interaction.edit_original_response(content=f"**You Already Have a Ticket Created!** -> <#{ticketdata['channel_id']}>")
          return

        if has_ticket == False:          
          await interaction.edit_original_response(content=f"**Creating ticket..**")
                
          category = bot.get_channel(FIRST_TICKETS_CAT)
          ticketlogs = bot.get_channel(TICKETLOGS_ID)
          mmrole = interaction.guild.get_role(MMROLE_ID)
          #starter_role = interaction.guild.get_role(856694433712701460)

          dbchannel = bot.get_channel(MAIN_INFOID)
          maindata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten();maindata_msg=maindata_msg[0]
          maindata = ast.literal_eval(maindata_msg.content)

          new_count = int(maindata['t_count'])+1
          maindata['t_count'] = new_count
          await maindata_msg.edit(maindata)

          newvar = str(new_count)
          overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True),
            mmrole: discord.PermissionOverwrite(send_messages=False, view_channel=False, attach_files=True, embed_links=True, read_message_history=True, manage_messages=True)
          }
          channel = await interaction.guild.create_text_channel(f"mm {interaction.user.name} {newvar}", category=category, overwrites=overwrites)
          await interaction.edit_original_response(content=f"**Ticket Created!** -> {channel.mention}")

          dbchannel = await dbserver.create_text_channel(name=f"{interaction.user.id}-{channel.id}-mm")
          await channel.edit(topic=dbchannel.id)
          dbdata = {
            "channel_id": channel.id,
            "channel_owner_id": interaction.user.id,
            "closed_msg_id": 0,
            "t_status": "Open",
            "user_added": "No",
            "added_users": [ {"user_id": interaction.user.id} ]
          }
          await dbchannel.send(f"{dbdata}")
          try:
            users_oncooldown.remove(interaction.user.id)
          except ValueError:
            pass
          logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{channel.name}** | ID: {channel.id}\nAction: **Created Ticket**", color=0x57f287)
          logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
          await ticketlogs.send(embed=logembed)
          msgembed = discord.Embed(title=f"Middleman Request", description=f"・Please respond with the **ID**/**username** of your trader!\n For **example**:\n・`1037772222145765406`\n・`sparkles#1286`", color=nocolour)
          msgembed.set_footer(text=f"{guild.name} | {guild.id}")
          msgembed.set_thumbnail(url=interaction.user.display_avatar)
          await channel.send(f"{interaction.user.mention}", embed=msgembed)






@bot.command()
async def dec_trades(ctx):
  if (ctx.message.author.id == 722113748088782899):
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      tradeslist = session.get(f"https://trades.roblox.com/v1/trades/Inbound?sortOrder=Asc&limit=100").json()["data"]
      for i in tradeslist:
        tradeid = i['id']
        Request = session.post(f"https://trades.roblox.com/v1/trades/{tradeid}/decline")
      if len(tradeslist) == 0:
        await ctx.reply("No inbound trades were found!")
        return
      else:
        if (Request.status_code == 200):
          await ctx.reply(embed=discord.Embed(description=f"***Successfully declined all inbound trades***", color=0x57F288))
        elif (Request.status_code == 400):
          await ctx.reply(embed=discord.Embed(description=f"*Unknown error has occurred*", color=0xED4245))
        elif (Request.status_code == 401):
          await ctx.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
        elif (Request.status_code == 403):
          await ctx.reply(embed=discord.Embed(description=f"*Token Validation Failed*", color=0xED4245))
        elif (Request.status_code == 429):
          await ctx.reply(embed=discord.Embed(description=f"*The flood limit has been exceeded*", color=0xED4245))

@bot.command()
async def mm(ctx):
  if (ctx.message.author.id == 722113748088782899) or (ctx.message.author.id == 358594990982561792):
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      authData = session.get(f"https://users.roblox.com/v1/users/authenticated").json()
      rbx_userID = authData['id']
      rbx_name = authData['name']  

      get_avatar_0 = session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={rbx_userID}&size=720x720&format=Png&isCircular=false")
      avatar_0 = get_avatar_0.json()["data"][0]["imageUrl"]

      embed = discord.Embed(title="**Middleman Account Information**", description="This is the only account associated with **Sparkles / <@722113748088782899>**.\nAny other accounts you are given are fakes and they may be trying to scam you.", color=maincolor)
      embed.add_field(name="Account Username & ID", value=f"User: [**`{rbx_name}`**](https://www.roblox.com/users/{rbx_userID}/profile)\nID: **`{rbx_userID}`**", inline=False)
      embed.add_field(name="Profile Link", value=f"https://www.roblox.com/users/{rbx_userID}/profile", inline=False)
      embed.add_field(name="Trade Link", value=f"https://roblox.com/users/{rbx_userID}/trade", inline=False)
      embed.set_thumbnail(url=avatar_0)
      await ctx.reply(embed=embed)

@bot.command()
async def get_f(ctx):
  if (ctx.message.author.id == 722113748088782899) or (ctx.message.author.id == 358594990982561792):
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      requests_data = session.get(f"https://friends.roblox.com/v1/my/friends/requests?sortOrder=Desc&limit=10").json()["data"]
      embed = discord.Embed(title="__Latest Friend Requests__", color=0x303135)
      for i in requests_data:
        sentAt = i["friendRequest"]["sentAt"]
        a = arrow.get(sentAt)
        sentAtDate = math.trunc(a.timestamp())
        #sentAtDate = a.humanize(granularity=["hour", "minute"])

        createdAt = i["created"]
        b = arrow.get(createdAt)
        createdAtDate = math.trunc(b.timestamp())
        #createdAtDate = b.humanize(granularity=["day", "hour", "minute"])
        
        senderId = i["friendRequest"]["senderId"]
        username = i["name"]
        displayName = i["displayName"]
        embed.add_field(name=f"Sent since <t:{sentAtDate}:R>", value=f"> ID: `{senderId}`\n> Username: `{username}`\n> Display Name `{displayName}`\n> Created since <t:{createdAtDate}:R>\n> [Direct Link](https://www.roblox.com/users/{senderId})\n〃───────────〃〃───────────〃〃───────────〃", inline=False)
      if len(requests_data) == 0:
        await ctx.reply("No recent friend requests were found!")
      else:
        await ctx.reply(embed=embed)

@bot.command()
async def acc_f(ctx, arg1=None):
  if (ctx.message.author.id == 722113748088782899):
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      if arg1==None:
        await ctx.reply("Username is missing!")
      else:
        data = {"usernames": arg1}
        get_user = session.post(f"https://users.roblox.com/v1/usernames/users", data=data).json()
        usernamu = get_user["data"][0]["id"]
        usernamua = get_user["data"][0]["name"]
        Request = session.post(f"https://friends.roblox.com/v1/users/{usernamu}/accept-friend-request")
        if (Request.status_code == 200):
          await ctx.reply(embed=discord.Embed(description=f"***Successfully accepted the friend request from `{usernamua}`***", color=0x57F288))
        elif (Request.status_code == 400):
          await ctx.reply(embed=discord.Embed(description=f"*Unknown error has occurred*", color=0xED4245))
        elif (Request.status_code == 401):
          await ctx.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
        elif (Request.status_code == 403):
          await ctx.reply(embed=discord.Embed(description=f"*Token Validation Failed*", color=0xED4245))
        elif (Request.status_code == 429):
          await ctx.reply(embed=discord.Embed(description=f"*The flood limit has been exceeded*", color=0xED4245))

@bot.command()
async def dec_f(ctx, arg1=None):
  if (ctx.message.author.id == 722113748088782899):
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")

      if arg1==None:
        await ctx.reply("Username is missing!")
      else:
        data = {"usernames": arg1}
        get_user = session.post(f"https://users.roblox.com/v1/usernames/users", data=data).json()
        usernamu = get_user["data"][0]["id"]
        usernamua = get_user["data"][0]["name"]
        Request = session.post(f"https://friends.roblox.com/v1/users/{usernamu}/decline-friend-request")
        if (Request.status_code == 200):
          await ctx.reply(embed=discord.Embed(description=f"***Successfully declined the friend request from `{usernamua}`***", color=0x57F288))
        elif (Request.status_code == 400):
          await ctx.reply(embed=discord.Embed(description=f"*Unknown error has occurred*", color=0xED4245))
        elif (Request.status_code == 401):
          await ctx.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
        elif (Request.status_code == 403):
          await ctx.reply(embed=discord.Embed(description=f"*Token Validation Failed*", color=0xED4245))
        elif (Request.status_code == 429):
          await ctx.reply(embed=discord.Embed(description=f"*The flood limit has been exceeded*", color=0xED4245))

@bot.command()
async def dec_all(ctx):
  if (ctx.message.author.id == 722113748088782899):
    cookie = await get_cookie()
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.get(url="https://users.roblox.com/v1/users/authenticated")
    if req.status_code != 200:
      await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")
      return
    else:
      req = session.post(url="https://auth.roblox.com/")
      if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
      req2 = session.post(url="https://auth.roblox.com/")
      
      Request = session.post(f"https://friends.roblox.com/v1/user/friend-requests/decline-all")
      if (Request.status_code == 200):
        await ctx.reply(embed=discord.Embed(description=f"***Successfully declined all the friend requests***", color=0x57F288))
      elif (Request.status_code == 400):
        await ctx.reply(embed=discord.Embed(description=f"*Unknown error has occurred*", color=0xED4245))
      elif (Request.status_code == 401):
        await ctx.reply(embed=discord.Embed(description=f"*Authorization has been denied for this request. (aka. invalid cookie is set)*", color=0xED4245))
      elif (Request.status_code == 403):
        await ctx.reply(embed=discord.Embed(description=f"*Token Validation Failed*", color=0xED4245))
      elif (Request.status_code == 429):
        await ctx.reply(embed=discord.Embed(description=f"*The flood limit has been exceeded*", color=0xED4245))


@bot.listen()
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
    pass
  elif isinstance(error, commands.CommandOnCooldown):
    hours = int(time.time() + error.retry_after)
    await ctx.reply(f"> You're doing that too quickly, try again **<t:{hours}:R>**")

@bot.command()
async def lim(ctx):
  price = 1234567890
  #https://catalog.roblox.com/v1/search/items/details?category=Collectibles&limit=30&sortType=4&subcategory=Collectibles
  res = requests.get('https://catalog.roblox.com/v1/search/items/details?'
                            f'category=Accessories&'
                            f'limit=30&'
                            f'sortType=4&'
                            #f'minPrice=1&'
                            f'creatorName=Roblox&'
                            f'salesTypeFilter=2')

  for limited in res.json()['data']:
    if "lowestPrice" not in limited:
      continue
    if "totalQuantity" in limited:
      continue
    if int(limited['lowestPrice']) < price:
      price = int(limited['lowestPrice'])
      info = limited
  embed = discord.Embed(title=f"`₍ ᐢ..ᐢ ₎ ﹒cheapest limited`", description=f"・ *__`name`__ **`:`*** ***`{info['name']}`***\n・ *__`price`__ **`:`*** ***`{price}`*** <:Robux:1127315514256011376>\n・ *__`link`__ **`:`*** ***https://www.roblox.com/catalog/{info['id']}***", color=nocolour)
  res = requests.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={info['id']}&size=420x420&format=Png&isCircular=true")
  embed.set_thumbnail(url=res.json()['data'][0]['imageUrl'])
  await ctx.reply(embed=embed)

@bot.command()
async def a_t(ctx, arg1=None):
  if arg1==None:
    await ctx.reply(f"Argument is missing!\n*`usuage: {PREFIX}a_t 123`*")
  else:
    try:
      getint = int(arg1)
      if type(getint) == int:
        c = round(getint/0.7)
        await ctx.reply(f"After tax of {getint} is **__{c}__**")
    except ValueError:
      await ctx.reply("Argument must be a number!")

@bot.command()
async def b_t(ctx, arg1=None):
  if arg1==None:
    await ctx.reply(f"Argument is missing!\n*`usuage: {PREFIX}b_t 123`*")
  else:
    try:
      getint = int(arg1)
      if type(getint) == int:
        b = round(getint*0.7)
        await ctx.reply(f"Before tax of {getint} is **__{b}__**")
    except ValueError:
      await ctx.reply("Argument must be a number!")

@bot.command()
async def mmban(ctx, member : discord.Member = None, *, reason = None):
  role = ctx.guild.get_role(BLACKLIST_ROLE)
  rolereq = ctx.guild.get_role(MMROLE_ID)
  blc = bot.get_channel(1147836224015450192)
  if rolereq in ctx.author.roles:
      if member == None:
        return await ctx.reply("Please mention a user to blacklist/unblacklist.")
      
      if role in member.roles:
        await member.remove_roles(role)
        await ctx.reply(f"**{member.name}#{member.discriminator}** has been removed from the blacklist.")
        await blc.send(embed=discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nUsed in: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: Unblacklisted **{member.name}#{member.discriminator}** | ID: {member.id} | {member.mention}", color=0xed4245))
      else: 
        
        if reason == None:
          return await ctx.reply("Please specify a reason.")
        
        await member.add_roles(role)
        await ctx.reply(f"**{member.name}#{member.discriminator}** has been blacklisted.")
        await blc.send(embed=discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nUsed in: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: Blacklisted **{member.name}#{member.discriminator}** | ID: {member.id} | {member.mention}\nReason: {reason}", color=0x57f287))

@bot.command()
async def dwc(ctx, member : discord.Member = None, *, reason = None):
  role = ctx.guild.get_role(1147836326889144360)
  rolereq = ctx.guild.get_role(MMROLE_ID)
  blc = bot.get_channel(1147836224015450192)
  if rolereq in ctx.author.roles:
      if member == None:
        return await ctx.reply("Please mention a user to give dwc role.")
      
      if role in member.roles:
        await member.remove_roles(role)
        await ctx.reply(f"**{member.name}#{member.discriminator}** has been removed from dwc.")
        await blc.send(embed=discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nUsed in: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: Removed From DWC **{member.name}#{member.discriminator}** | ID: {member.id} | {member.mention}", color=0xed4245))
      else: 
        
        if reason == None:
          return await ctx.reply("Please specify a reason.")
        
        await member.add_roles(role)
        await ctx.reply(f"**{member.name}#{member.discriminator}** has been given dwc role.")
        await blc.send(embed=discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nUsed in: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: Has been DWC'ed **{member.name}#{member.discriminator}** | ID: {member.id} | {member.mention}\nReason: {reason}", color=0x57f287))

@bot.command()
async def v(ctx):
   guild = bot.get_guild(DB_SERVERID)
   await guild.channel.delete()

@bot.event
async def on_guild_channel_delete(channel):
    if channel.guild.id == GUILD_ID:
        try:
            if (channel.category.id == FIRST_TICKETS_CAT) or (channel.category.id == CLOSED_CATEGORY_ID) or (channel.category.id == 1147836710793773126) or channel.category.id in cates:
                con,cur = openCON()
                cur.execute(f"DELETE FROM ticket_data WHERE channel_id='{channel.id}'")
                con.commit()
                closeCON(cur,con)
        except AttributeError:
            pass


allowed_content_types = [
    "image/jpeg",
    "image/png",
]

@bot.command()
async def add_emoji(ctx, name, url):
    guild = bot.get_guild(GUILD_ID)
    if ctx.author.guild_permissions.manage_emojis:
        try:
            async with ctx.typing():
                async with bot.session.get(url) as response:
                    emoji_image = await response.read()
            
            emoji = await guild.create_custom_emoji(name=name, image=emoji_image)
            await ctx.send(f'Emoji {emoji} added successfully!')
        except discord.HTTPException as e:
            await ctx.send(f'Failed to add emoji: {e}')
    else:
        await ctx.send("You don't have permission to manage emojis.")




@bot.command()
async def whois(ctx, user : discord.User=None):
  guild = bot.get_guild(GUILD_ID)
  publicFlags = []
  rolelist = []
  
  
  if user == None: # If no user was provided
        
    member1 = guild.get_member(ctx.author.id)
    memberfetch = await bot.fetch_user(ctx.author.id)
    
    banner = memberfetch.banner
    
    highestrole_color = member1.roles[-1].color


    
    embed = discord.Embed(description=f"**{member1.mention}** | **ID: `{member1.id}`**")
    embed.set_author(name=f"{member1.name}#{member1.discriminator}", icon_url=member1.display_avatar.url)
    embed.set_thumbnail(url=member1.display_avatar.url)

    if member1.colour.value:
      embed.colour = member1.colour

    if member1.public_flags.staff:
      publicFlags.append("<:Discord_Staff:1083411067599859722> Discord Staff")
    if member1.public_flags.discord_certified_moderator:
      publicFlags.append("<:Discord_certified_moderator:908773478138794044> Discord Certified Moderator")
    if member1.public_flags.bug_hunter:
      publicFlags.append("<:Bug_Hunter:1083415473263226982> Bug Hunter")
    if member1.public_flags.bug_hunter_level_2:
      publicFlags.append("<:Bug_Hunter_level_2:1083412145552752711> Bug Hunter Lvl.2")
    if member1.public_flags.partner:
      publicFlags.append("<:Discord_Partner:1083416673735950386>  Discord Partner")
    if member1.public_flags.verified_bot_developer:
      publicFlags.append("<:Verified_Bot_Developer:1083416957761626146> Verified Bot Developer")
    if member1.public_flags.early_supporter:
      publicFlags.append("<:Early_Supporter:1083418251826044978> Early Supporter")
    if member1.public_flags.hypesquad:
      publicFlags.append("<:HypeSquad_Event:908773478260428810> Hypesquad Event")
    if member1.public_flags.hypesquad_balance:
      publicFlags.append("<:HypeSquad_Balance:1066677556851519530> Hypesquad Balance")
    if member1.public_flags.hypesquad_bravery:
      publicFlags.append("<:HypeSquad_Bravery:1066677280652398633> Hypesquad Bravery")
    if member1.public_flags.hypesquad_brilliance:
      publicFlags.append("<:HypeSquad_Brilliance:1066677440652517427> Hypesquad Brilliance")
    if member1.public_flags.verified_bot:
      publicFlags.append("<:verified_bot:908774786778402836> Verified Bot")
    var1 = "\n".join(publicFlags)
        
    createddate = member1.created_at
    a1 = arrow.get(member1.created_at)
    b1 = a1.humanize(granularity=["second"]).split()[0]
    c1 = humanfriendly.format_timespan(int(b1))
    created_date = createddate.strftime(f"%a, %b %d, %Y %I:%M %p\n({c1} ago)")
    
    joineddate = member1.joined_at
    a2 = arrow.get(member1.joined_at)
    b2 = a2.humanize(granularity=["second"]).split()[0]
    c2 = humanfriendly.format_timespan(int(b2))
    joined_date = joineddate.strftime(f"%a, %b %d, %Y %I:%M %p\n({c2} ago)")
    
    
    roles = member1.roles[1:]
    for i in roles:
      #if i.id == 810934999703355402 or i.id == 810935095589863474:
      #  pass
      #else:
      rolelist.append(i.mention)
    rolelist.reverse()
    var2 = f"\n".join(rolelist)
    
    
    embed.add_field(name=f"**Joined**", value=f"{joined_date}", inline=True)
    embed.add_field(name=f"**Created**", value=f"{created_date}", inline=True)

    if member1.public_flags.value != 0:
      embed.add_field(name=f"**Badges [{len(publicFlags)}]**", value=f"{var1}", inline=False)
      
    embed.add_field(name=f"**Roles [{len(rolelist)}]**", value=f"{var2}", inline=False)
    
    
    fetchauthor = await bot.fetch_user(ctx.author.id)
    
    embed.set_footer(text=f"Author: {member1.name}#{member1.discriminator} | {member1.id}", icon_url=fetchauthor.display_avatar.url)
        
    if banner != None:
      class Google(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)
          self.add_item(discord.ui.Button(label="View User's Banner", url=banner.url, emoji="<:user:1177983443859165307>"))
      await ctx.reply(embed=embed, view=Google())
    elif banner == None:
      await ctx.reply(embed=embed)
  elif user != None: # If user was provided
    
    if user.bot == True: # If user is bot
      member1 = guild.get_member(user.id)
      author = guild.get_member(ctx.author.id)
            
      highestrole_color = member1.roles[-1].color
      
      embed = discord.Embed(description=f"**{member1.mention}** | **ID: `{member1.id}`**", color=member1.color)
      embed.set_author(name=f"{member1.name}#{member1.discriminator}", icon_url=member1.display_avatar.url)
      embed.set_thumbnail(url=member1.display_avatar.url)

      if member1.public_flags.staff:
        publicFlags.append("<:Discord_Staff:1083411067599859722> Discord Staff")
      if member1.public_flags.discord_certified_moderator:
        publicFlags.append("<:Discord_certified_moderator:908773478138794044> Discord Certified Moderator")
      if member1.public_flags.bug_hunter:
        publicFlags.append("<:Bug_Hunter:1083415473263226982> Bug Hunter")
      if member1.public_flags.bug_hunter_level_2:
        publicFlags.append("<:Bug_Hunter_level_2:1083412145552752711> Bug Hunter Lvl.2")
      if member1.public_flags.partner:
        publicFlags.append("<:Discord_Partner:1083416673735950386>  Discord Partner")
      if member1.public_flags.verified_bot_developer:
        publicFlags.append("<:Verified_Bot_Developer:1083416957761626146> Verified Bot Developer")
      if member1.public_flags.early_supporter:
        publicFlags.append("<:Early_Supporter:1083418251826044978> Early Supporter")
      if member1.public_flags.hypesquad:
        publicFlags.append("<:HypeSquad_Event:908773478260428810> Hypesquad Event")
      if member1.public_flags.hypesquad_balance:
        publicFlags.append("<:HypeSquad_Balance:1066677556851519530> Hypesquad Balance")
      if member1.public_flags.hypesquad_bravery:
        publicFlags.append("<:HypeSquad_Bravery:1066677280652398633> Hypesquad Bravery")
      if member1.public_flags.hypesquad_brilliance:
        publicFlags.append("<:HypeSquad_Brilliance:1066677440652517427> Hypesquad Brilliance")
      if member1.public_flags.verified_bot:
        publicFlags.append("<:verified_bot:908774786778402836> Verified Bot")
      var1 = "\n".join(publicFlags)
      
      createddate = member1.created_at
      a1 = arrow.get(member1.created_at)
      b1 = a1.humanize(granularity=["second"]).split()[0]
      c1 = humanfriendly.format_timespan(int(b1))
      created_date = createddate.strftime(f"%a, %b %d, %Y %I:%M %p\n({c1} ago)")
      
      joineddate = member1.joined_at
      a2 = arrow.get(member1.joined_at)
      b2 = a2.humanize(granularity=["second"]).split()[0]
      c2 = humanfriendly.format_timespan(int(b2))
      joined_date = joineddate.strftime(f"%a, %b %d, %Y %I:%M %p\n({c2} ago)")
      
      
      roles = member1.roles[1:]
      for i in roles:
        #if i.id == 810934999703355402 or i.id == 810935095589863474:
        #  pass
        #else:
        rolelist.append(i.mention)
      rolelist.reverse()
      var2 = f"\n".join(rolelist)
      
      
      embed.add_field(name=f"**Joined**", value=f"{joined_date}", inline=True)
      embed.add_field(name=f"**Created**", value=f"{created_date}", inline=True)

      if member1.public_flags.value != 0:
        embed.add_field(name=f"**Badges [{len(publicFlags)}]**", value=f"{var1}", inline=False)
      
      embed.add_field(name=f"**Roles [{len(rolelist)}]**", value=f"{var2}", inline=False)
      
      
      fetchauthor = await bot.fetch_user(ctx.author.id)
      
      embed.set_footer(text=f"Author: {author.name}#{author.discriminator} | {author.id}", icon_url=fetchauthor.display_avatar.url)
          
      await ctx.reply(embed=embed)
    elif user.bot == False: # If user is not a bot
      
      checkmember = guild.get_member(user.id)
      if checkmember != None: # If member is in the server
        member2 = guild.get_member(user.id)
        memberfetch2 = await bot.fetch_user(user.id)
        author2 = guild.get_member(ctx.author.id)
        
        banner2 = memberfetch2.banner
        
        highestrole_color = member2.roles[-1].color

        embed1 = discord.Embed(description=f"**{member2.mention}** | **ID: `{member2.id}`**", color=highestrole_color)
        embed1.set_author(name=f"{member2.name}#{member2.discriminator}", icon_url=memberfetch2.display_avatar.url)
        embed1.set_thumbnail(url=memberfetch2.display_avatar.url)

        if member2.public_flags.staff:
          publicFlags.append("<:Discord_Staff:1083411067599859722> Discord Staff")
        if member2.public_flags.discord_certified_moderator:
          publicFlags.append("<:Discord_certified_moderator:908773478138794044> Discord Certified Moderator")
        if member2.public_flags.bug_hunter:
          publicFlags.append("<:Bug_Hunter:1083415473263226982> Bug Hunter")
        if member2.public_flags.bug_hunter_level_2:
          publicFlags.append("<:Bug_Hunter_level_2:1083412145552752711> Bug Hunter Lvl.2")
        if member2.public_flags.partner:
          publicFlags.append("<:Discord_Partner:1083416673735950386>  Discord Partner")
        if member2.public_flags.verified_bot_developer:
          publicFlags.append("<:Verified_Bot_Developer:1083416957761626146> Verified Bot Developer")
        if member2.public_flags.early_supporter:
          publicFlags.append("<:Early_Supporter:1083418251826044978> Early Supporter")
        if member2.public_flags.hypesquad:
          publicFlags.append("<:HypeSquad_Event:908773478260428810> Hypesquad Event")
        if member2.public_flags.hypesquad_balance:
          publicFlags.append("<:HypeSquad_Balance:1066677556851519530> Hypesquad Balance")
        if member2.public_flags.hypesquad_bravery:
          publicFlags.append("<:HypeSquad_Bravery:1066677280652398633> Hypesquad Bravery")
        if member2.public_flags.hypesquad_brilliance:
          publicFlags.append("<:HypeSquad_Brilliance:1066677440652517427> Hypesquad Brilliance")
        if member2.public_flags.verified_bot:
          publicFlags.append("<:verified_bot:908774786778402836> Verified Bot")
        var1 = "\n".join(publicFlags)
            
        createddate = member2.created_at
        a1 = arrow.get(member2.created_at)
        b1 = a1.humanize(granularity=["second"]).split()[0]
        c1 = humanfriendly.format_timespan(int(b1))
        created_date1 = createddate.strftime(f"%a, %b %d, %Y %I:%M %p\n({c1} ago)")
        
        joineddate = member2.joined_at
        a2 = arrow.get(member2.joined_at)
        b2 = a2.humanize(granularity=["second"]).split()[0]
        c2 = humanfriendly.format_timespan(int(b2))
        joined_date1 = joineddate.strftime(f"%a, %b %d, %Y %I:%M %p\n({c2} ago)")
        
        
        roles = member2.roles[1:]
        for i in roles:
          #if i.id == 810934999703355402 or i.id == 810935095589863474:
          #  pass
          #else:
          rolelist.append(i.mention)
        rolelist.reverse()
        var2 = f"\n".join(rolelist)
        
        
        embed1.add_field(name=f"**Joined**", value=f"{joined_date1}", inline=True)
        embed1.add_field(name=f"**Created**", value=f"{created_date1}", inline=True)

        if member2.public_flags.value != 0:
          embed1.add_field(name=f"**Badges [{len(publicFlags)}]**", value=f"{var1}", inline=False)
        
        embed1.add_field(name=f"**Roles [{len(rolelist)}]**", value=f"{var2}", inline=False)
        
        
        fetchauthor = await bot.fetch_user(ctx.author.id)
                
        embed1.set_footer(text=f"Author: {author2.name}#{author2.discriminator} | {author2.id}", icon_url=fetchauthor.display_avatar.url)
        if banner2 != None:
          class Google1(discord.ui.View):
            def __init__(self):
              super().__init__(timeout=None)
              self.add_item(discord.ui.Button(label="View User's Banner", url=banner2.url, emoji="<:user:1177983443859165307>"))
          await ctx.reply(embed=embed1, view=Google1())
        elif banner2 == None:
          await ctx.reply(embed=embed1)
      elif checkmember == None: # If member is not in the server
        
        memberfetch2 = await bot.fetch_user(user.id)
        author2 = guild.get_member(ctx.author.id)
        
        banner2 = memberfetch2.banner
        
        embed1 = discord.Embed(description=f"**{memberfetch2.mention}** | **ID: `{memberfetch2.id}`**", color=memberfetch2.color)
        embed1.set_author(name=f"{memberfetch2.name}#{memberfetch2.discriminator}", icon_url=memberfetch2.display_avatar.url)
        embed1.set_thumbnail(url=memberfetch2.display_avatar.url)

        if memberfetch2.public_flags.staff:
          publicFlags.append("<:Discord_Staff:1083411067599859722> Discord Staff")
        if memberfetch2.public_flags.discord_certified_moderator:
          publicFlags.append("<:Discord_certified_moderator:908773478138794044> Discord Certified Moderator")
        if memberfetch2.public_flags.bug_hunter:
          publicFlags.append("<:Bug_Hunter:1083415473263226982> Bug Hunter")
        if memberfetch2.public_flags.bug_hunter_level_2:
          publicFlags.append("<:Bug_Hunter_level_2:1083412145552752711> Bug Hunter Lvl.2")
        if memberfetch2.public_flags.partner:
          publicFlags.append("<:Discord_Partner:1083416673735950386>  Discord Partner")
        if memberfetch2.public_flags.verified_bot_developer:
          publicFlags.append("<:Verified_Bot_Developer:1083416957761626146> Verified Bot Developer")
        if memberfetch2.public_flags.early_supporter:
          publicFlags.append("<:Early_Supporter:1083418251826044978> Early Supporter")
        if memberfetch2.public_flags.hypesquad:
          publicFlags.append("<:HypeSquad_Event:908773478260428810> Hypesquad Event")
        if memberfetch2.public_flags.hypesquad_balance:
          publicFlags.append("<:HypeSquad_Balance:1066677556851519530> Hypesquad Balance")
        if memberfetch2.public_flags.hypesquad_bravery:
          publicFlags.append("<:HypeSquad_Bravery:1066677280652398633> Hypesquad Bravery")
        if memberfetch2.public_flags.hypesquad_brilliance:
          publicFlags.append("<:HypeSquad_Brilliance:1066677440652517427> Hypesquad Brilliance")
        if memberfetch2.public_flags.verified_bot:
          publicFlags.append("<:verified_bot:908774786778402836> Verified Bot")
        var1 = "\n".join(publicFlags)
            
        createddate = memberfetch2.created_at
        a1 = arrow.get(memberfetch2.created_at)
        b1 = a1.humanize(granularity=["second"]).split()[0]
        c1 = humanfriendly.format_timespan(int(b1))
        created_date1 = createddate.strftime(f"%a, %b %d, %Y %I:%M %p\n({c1} ago)")
                        
        
        embed1.add_field(name=f"**Created**", value=f"{created_date1}", inline=True)

        if memberfetch2.public_flags.value != 0:
          embed1.add_field(name=f"**Badges [{len(publicFlags)}]**", value=f"{var1}", inline=False)        
        
        fetchauthor = await bot.fetch_user(ctx.author.id)
                
        embed1.set_footer(text=f"Author: {author2.name}#{author2.discriminator} | {author2.id}", icon_url=fetchauthor.display_avatar.url)
        if banner2 != None:
          class Google1(discord.ui.View):
            def __init__(self):
              super().__init__(timeout=None)
              self.add_item(discord.ui.Button(label="View User's Banner", url=banner2.url, emoji="<:user:1177983443859165307>"))
          await ctx.reply(embed=embed1, view=Google1())
        elif banner2 == None:
          await ctx.reply(embed=embed1)




def get_prefix():
  prefix = PREFIX
  return prefix

@bot.command()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def loa(ctx, userID=None, amt_time=None):
    con,cur = openCON()
    cur.execute(f"SELECT * FROM loa_logs")
    guild = bot.get_guild(GUILD_ID)
    alldata = cur.fetchall()
    support = guild.get_role(SUPPORT_ID)
    role = guild.get_role(1205130805479739402)
    if support in ctx.author.roles:
        if userID is None or amt_time is None:
            await ctx.reply(f"Invalid usage.\n*`usage: {PREFIX} userID time in days`*")
            return
        
        user_exists = False
        for row in alldata:
            if str(row["userID"]) == str(userID):
                user_exists = True
                break
        
        if user_exists:
            user = guild.get_member(userID)
            cur.execute("DELETE FROM loa_logs WHERE userID = %s", (userID,))
            con.commit()  # Commit the transaction
            await ctx.reply(f"**Successfully** removed <@{str(userID)}> from the **database**.")
            await user.remove_roles(role)
        else:
            user = guild.get_member(userID)
            cur.execute("INSERT INTO loa_logs (userID, timeD) VALUES (%s, %s)", (userID, amt_time))
            con.commit()
            await ctx.reply(f"**Successfully** added <@{str(userID)}> to the **LOA database**.")
            await user.add_roles(role)



@bot.command()
async def loa_logs(ctx):
    rolereq = ctx.guild.get_role(SUPPORT_ID)
    if rolereq in ctx.author.roles:
        guild = bot.get_guild(GUILD_ID)
        con, cur = openCON()
        cur.execute(f"SELECT * FROM loa_logs")
        alldata = cur.fetchall()

        user_string = ""

        for i in alldata:
            user_id = int(i['userID'])
            user = guild.get_member(user_id)
            time_duration = i['timeD']
            
            current_date = datetime.datetime.now()
            expiration_date = current_date + datetime.timedelta(days=time_duration)
            expiration_date_str = expiration_date.strftime('%Y-%m-%d')

            remaining_time = expiration_date - current_date
            
            # Calculate remaining days and remaining hours
            remaining_days = remaining_time.days
            remaining_hours = remaining_time.seconds // 3600  # Convert remaining seconds to hours

            user_string += f"User: {user.mention} - Remaining: **{remaining_days} Days, {remaining_hours} Hours** - Expires: **{expiration_date_str}**\n"

            if remaining_days == 0 and remaining_hours == 0:
                role = discord.utils.get(ctx.guild.roles, id=1205130805479739402) 
                cur.execute("DELETE FROM loa_logs WHERE userID = %s", (user_id,))
                con.commit()  # Commit the transaction

                embed = discord.Embed(title="LOA ENDED", description=f"The LOA for <@{str(user_id)}> has ended! They have been removed of the <@&1205130805479739402> role.", color=discord.Color.green())
                await ctx.send("<@&1147320320089407538>", embed=embed)
                await user.remove_roles(role)

        embed = discord.Embed(title="__MM LOA List__", description=user_string, color=0x303135)
        await ctx.send(embed=embed)

        await asyncio.sleep(3600)  # Sleep for 1 hour (3600 seconds)
        await loa_logs(ctx)






@bot.command()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def add_db(ctx, userID=None, username=None):
    support = ctx.guild.get_role(SUPPORT_ID)
    if (support in ctx.author.roles):
      if userID == None or username==None:
        await ctx.reply(f"Invalid usuage.\n*`usuage: {PREFIX} userID username`*")
        return
      else:
        dbchannel = bot.get_channel(LOGSINFO_ID)
        logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
        while len(logsdata_msg) == 0:
          logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
          time.sleep(0.5)
        logsdata_msg=logsdata_msg[0]
        file = logsdata_msg.attachments[0]
        cont = await file.read()
        alldata = ast.literal_eval(cont.decode('utf-8'))
        alldata.append({"userID": userID, "username": username, "count": 0, "strikes": 0, "role_id": "1"})
        await updatedb_logs(alldata, logsdata_msg, dbchannel)
        await ctx.reply(f"Successfully added <@{str(userID)}> to the database.")

@bot.command()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def remove_db(ctx, userID=None):
    support = ctx.guild.get_role(SUPPORT_ID)
    if (support in ctx.author.roles):
      if userID == None:
        await ctx.reply(f"Invalid usuage.\n*`usuage: {PREFIX}remove_db userID`*")
        return
      else:
        dbchannel = bot.get_channel(LOGSINFO_ID)
        logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
        while len(logsdata_msg) == 0:
          logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
          time.sleep(0.5)
        logsdata_msg=logsdata_msg[0]
        file = logsdata_msg.attachments[0]
        cont = await file.read()
        alldata = ast.literal_eval(cont.decode('utf-8'))
        for i in alldata:
          if int(i['userID']) == int(userID):
            alldata.remove(i)
            await updatedb_logs(alldata, logsdata_msg, dbchannel)
            await ctx.reply(f"Successfully removed <@{str(userID)}> from the database.")
            break


@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, user:discord.User=None, *, reason=None):
  guild = bot.get_guild(GUILD_ID)
  #rolereq = guild.get_role(898697518454550529)
  Toggle = True
  #if rolereq in ctx.author.roles:
  if reason == None:
    reason = "No reason given."
  if user == None:
    await ctx.reply("Please **specify** a user to ban.")
    return
  else:
    try:
      ban = await guild.fetch_ban(user)
      ban = True
    except NotFound:
      ban = False
    if ban == True:
      await ctx.reply(f"{user.mention} is **already** banned!")
      return
    else:
      checkmember = guild.get_member(user.id)
      if checkmember != None: # If member is in the server
        if checkmember.guild_permissions.administrator == True:
          await ctx.reply("You **can't** ban an administrator!")
          return
      try:
        dmchannel = await user.create_dm()
        emee = discord.Embed(title=f"BANNED", description=f"You've been **banned** from {guild.name} by {ctx.author.mention}", color=redcolor)
        emee.add_field(name=f"Reason", value=reason)
        await dmchannel.send(embed=emee)
      except Forbidden:
        pass
      await guild.ban(user, reason=reason, delete_message_seconds=0)
      success = bot.get_emoji(931633507971764318)
      emba=discord.Embed(description="", color=maincolor)
      emba.set_author(name=f"Successfully banned {user}", icon_url="https://cdn.discordapp.com/emojis/994247557616238627.webp?size=96&quality=lossless")
      await ctx.reply(embed=emba)
                
      logs_c = bot.get_channel(1147241361351905391)
      embed = discord.Embed(color=0xed4245)
      embed.set_author(name=f"Banned {user.name}#{user.discriminator} - {user.id}", icon_url=f"{user.display_avatar.url}")
      embed.add_field(name="User", value=user.mention, inline=True)
      embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
      embed.add_field(name="Reason", value=reason, inline=True)
      await logs_c.send(embed=embed)

@bot.command()
async def pend(ctx):
  rolereq = ctx.guild.get_role(MMROLE_ID)
  if rolereq in ctx.author.roles:
    cates = [STARTER_TICKETS, NOVICE_TICKETS, MIDDLEMAN_TICKETS, SENIOR_TICKETS, ADV_TICKETS, HEAD_TICKETS, ADMIN_TICKETS, FIRST_TICKETS_CAT, CLOSED_CATEGORY_ID, 1103657193531781200, 995691309601914910]
    if (ctx.channel.category.id in cates):
      pendingcat = bot.get_channel(1147836710793773126)
      await ctx.channel.edit(category=pendingcat)
      await ctx.send("Ticket has been moved to <#1147836710793773126>.")

@bot.command()
async def unpend(ctx):
  rolereq = ctx.guild.get_role(MMROLE_ID)
  if rolereq in ctx.author.roles:
    if (ctx.channel.category.id == 1147836710793773126):
      unpend = bot.get_channel(STARTER_TICKETS)
      await ctx.channel.edit(category=unpend)
      await ctx.send("Ticket has been moved to <#FIRST_TICKETS_CAT>.")

@bot.command()
async def setam(ctx, *,args=None):
  if (ctx.author.id == 1037772222145765406) or (ctx.author.id == 853264740302454805) or (ctx.author.id == 352643853590855681):
    if args == None:
      return await ctx.reply("Specify the vip server link.")
    user = bot.get_user(1037772222145765406)
    channel = await user.create_dm()
    msg = await channel.fetch_message(1180541292443349114)
    await msg.edit(args)
    await ctx.reply("Vip server **updated**")

@bot.command()
async def setmm2(ctx, *,args=None):
  if (ctx.author.id == 1037772222145765406) or (ctx.author.id == 853264740302454805) or (ctx.author.id == 352643853590855681):
    if args == None:
      return await ctx.reply("Specify the vip server link.")
    user = bot.get_user(1037772222145765406)
    channel = await user.create_dm()
    msg = await channel.fetch_message(1180542502399389819)
    await msg.edit(args)
    await ctx.reply("Vip server **updated**")

@bot.command()
async def setpsx(ctx, *,args=None):
  if (ctx.author.id == 1037772222145765406) or (ctx.author.id == 853264740302454805) or (ctx.author.id == 352643853590855681):
    if args == None:
      return await ctx.reply("Specify the vip server link.")
    user = bot.get_user(1037772222145765406)
    channel = await user.create_dm()
    msg = await channel.fetch_message(1180542051922743438)
    await msg.edit(args)
    await ctx.reply("Vip server **updated**")

@bot.command()
async def setms2(ctx, *,args=None):
  if (ctx.author.id == 1037772222145765406) or (ctx.author.id == 853264740302454805) or (ctx.author.id == 352643853590855681):
    if args == None:
      return await ctx.reply("Specify the vip server link.")
    user = bot.get_user(358594990982561792)
    channel = await user.create_dm()
    msg = await channel.fetch_message(998269948889677874)
    await msg.edit(args)
    await ctx.reply("Vip server updated.")

@bot.command()
async def ms2(ctx):
  mmrole = ctx.guild.get_role(MMROLE_ID)
  if (mmrole in ctx.author.roles):
    user = bot.get_user(358594990982561792)
    channel = await user.create_dm()
    msg = await channel.fetch_message(998269948889677874)
    await ctx.send(msg.content)

@bot.command()
async def am(ctx):
  mmrole = ctx.guild.get_role(MMROLE_ID)
  if (mmrole in ctx.author.roles):
    user = bot.get_user(1037772222145765406)
    channel = await user.create_dm()
    msg = await channel.fetch_message(1180541292443349114)
    await ctx.reply(msg.content)

@bot.command()
async def mm2(ctx):
  mmrole = ctx.guild.get_role(MMROLE_ID)
  if (mmrole in ctx.author.roles):
    user = bot.get_user(1037772222145765406)
    channel = await user.create_dm()
    msg = await channel.fetch_message(1180542502399389819)
    await ctx.reply(msg.content)

@bot.command()
async def psx(ctx):
  mmrole = ctx.guild.get_role(MMROLE_ID)
  if (mmrole in ctx.author.roles):
    user = bot.get_user(1037772222145765406)
    channel = await user.create_dm()
    msg = await channel.fetch_message(1180542051922743438)
    await ctx.reply(msg.content)

@bot.command()
async def help(ctx):
  embed = discord.Embed(color=maincolor)
  embed.add_field(name=f"<:global:1147838104959455352>・__Global__", value=f"───────────〃\n> ៹ 〃[`a_t` \"number\"] **-** Calculate roblox merch after tax.\n> ៹ 〃[`b_t` \"number\"] **-** Calculate roblox merch before tax.\n> ៹ 〃[`lim`] **-** Get cheapest limited on roblox.\n> ៹ 〃[`whois` \"@user/userID\"] **-** Get user info.\nㅤ", inline=False)
  embed.add_field(name=f"<:Discord_Certified_Moderator:1083411149757874286>・__Staff__", value=f"───────────〃\n> ៹ 〃[`ban`/`b` \"@user/userID\" \"reason\"] **-** Ban a user.\nㅤ", inline=False)
  embed.add_field(name=f"<:Discord_Staff:1083411067599859722>・__Middleman__", value=f"───────────〃\n> ៹ 〃[`add` \"@user/userID\"] **-** Add user to a ticket.\n> ៹ 〃[`remove` \"@user/userID\"] **-** Remove user from a ticket.\n> ៹ 〃[`rename` \"name\"] **-** Rename a ticket.\n> ៹ 〃[`delete`/`del`] **-** Delete a ticket.\n> ៹ 〃[`reopen`] **-** Reopen a ticket.\n> ៹ 〃[`mmban` \"@user/userID\" \"reason\"] **-** Blacklist a user.\n> ៹ 〃[`am`] **-** Sends adopt me vip server link.\n> ៹ 〃[`mm2`] **-** Sends mm2 vip server link.\n> ៹ 〃[`psx`] **-** Sends psx vip server link.\n> ៹ 〃[`pend` & `unpend`] **-** Move ticket to/out the pending category.\nㅤ", inline=False)
  embed.set_footer(text=f"Prefix: {PREFIX}")
  await ctx.reply(embed=embed)

@bot.command()
async def remove(ctx, user : discord.Member):
  rolereq = ctx.guild.get_role(MMROLE_ID)
  ticketlogs = bot.get_channel(TICKETLOGS_ID)
  if rolereq in ctx.author.roles:
    cates = [STARTER_TICKETS, NOVICE_TICKETS, MIDDLEMAN_TICKETS, SENIOR_TICKETS, ADV_TICKETS, HEAD_TICKETS, ADMIN_TICKETS, FIRST_TICKETS_CAT, CLOSED_CATEGORY_ID, 1103657193531781200, 995691309601914910]
    if ctx.channel.category.id in cates:

      try:
        dbchannel_id = int(ctx.channel.topic)
      except Exception:
        return await ctx.reply("This channel isn't a ticket.")
      dbchannel = bot.get_channel(dbchannel_id)
      ticketdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten();ticketdata_msg=ticketdata_msg[0]
      ticketdata = ast.literal_eval(ticketdata_msg.content)
      if len(ticketdata) == 0:
        return await ctx.reply("This channel isn't a ticket.")

      if rolereq in user.roles:
        return await ctx.reply("BRO! Why are you trying to remove your crew mate 😭")

      Toggle = True
      if str(ticketdata['t_status']) == "Closed" or str(ticketdata['t_status']) == "Delete":
        await ctx.reply("*You can't use this while the ticket is closed!*")
        Toggle = False
        return
      if Toggle == True:
        await ctx.message.channel.set_permissions(user, send_messages=False, view_channel=False, attach_files=False, embed_links=False, read_message_history=False)
        await ctx.send(f"{user.mention}", embed=discord.Embed(description=f'***{user.mention} was removed from the ticket {ctx.channel.mention}***', color=0xed4245))
        logembed = discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nTicket: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: **Removed {user.name}#{user.discriminator} | ID: {user.id}**", color=0xed4245)
        logembed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
        await ticketlogs.send(embed=logembed)
        ticketdata['added_users'].remove({"user_id": user.id})
        await ticketdata_msg.edit(ticketdata)
        tname = dbchannel.name.split("-")
        if int(tname[0]) == user.id:
          tname[0] = "0"
          tname = "-".join(tname)
          await dbchannel.edit(name=tname)

@bot.command(aliases=['del'])
@commands.cooldown(1, 10, commands.BucketType.channel)
async def delete(ctx):
  cates = [STARTER_TICKETS, NOVICE_TICKETS, MIDDLEMAN_TICKETS, SENIOR_TICKETS, ADV_TICKETS, HEAD_TICKETS, ADMIN_TICKETS, FIRST_TICKETS_CAT, CLOSED_CATEGORY_ID, 1103657193531781200, 995691309601914910]
  if ctx.channel.category.id in cates:
    rolereq = ctx.guild.get_role(MMROLE_ID)
    if (rolereq in ctx.author.roles):
      users={}
      ticketlogs = bot.get_channel(TICKETLOGS_ID)
      transcripts = bot.get_channel(TICKETLOGS_ID)
      guild = bot.get_guild(GUILD_ID)

      # try:
        # dbchannel_id = int(ctx.channel.topic)
      # except Exception:
        # return await ctx.reply("This channel isn't a ticket.")
      # dbchannel = bot.get_channel(dbchannel_id)
      # ticketdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten();ticketdata_msg=ticketdata_msg[0]
      # ticketdata = ast.literal_eval(ticketdata_msg.content)
      # if len(ticketdata) == 0:
        # eturn await ctx.reply("This channel isn't a ticket.")

      Status = True
      transcript = await chat_exporter.export(channel=ctx.channel, limit=None, tz_info="Asia/Singapore")
      # f str(ticketdata['t_status']) == "Delete":
        # await ctx.reply("*The ticket is already being deleted!*")
        # Status = False
        # return
      if Status == True:
        msg1 = discord.Embed(description=f'<a:Discord_Loading:1066670467424976967> Deleting this ticket in **5** sconds', color=nocolour)
        a = await ctx.channel.send(embed=msg1)
        await asyncio.sleep(1)
        msg2 = discord.Embed(description=f'<a:Discord_Loading:1066670467424976967> Deleting this ticket in **4** seconds', color=nocolour)
        await a.edit(embed=msg2)
        await asyncio.sleep(1)
        msg3 = discord.Embed(description=f'<a:Discord_Loading:1066670467424976967> Deleting this ticket in **3** seconds', color=nocolour)
        await a.edit(embed=msg3)
        await asyncio.sleep(1)
        msg4 = discord.Embed(description=f'<a:Discord_Loading:1066670467424976967> Deleting this ticket in **2** seconds', color=nocolour)
        await a.edit(embed=msg4)
        await asyncio.sleep(1)
        msg5 = discord.Embed(description=f'<a:Discord_Loading:1066670467424976967> Deleting this ticket in **1** seconds', color=nocolour)
        await a.edit(embed=msg5)
        await asyncio.sleep(1)
        msg6 = discord.Embed(description=f'<a:Discord_Loading:1066670467424976967> Deleting this ticket in **0** seconds', color=nocolour)
        await a.edit(embed=msg6)
        # ticketdata['t_status'] = "Delete"
        # await ticketdata_msg.edit(ticketdata)
        await ctx.message.delete()
        logembed = discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nTicket: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: **Deleted Ticket**", color=0xed4245)
        logembed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
        await ticketlogs.send(embed=logembed)
        if transcript is None:
          return
        transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html")
        transcriptembed = discord.Embed(color=0x1EC45C)
        transcriptembed.add_field(name="Author", value=f"{ctx.author.mention} | {ctx.author.id}", inline=True)
        transcriptembed.add_field(name="Ticket", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=True)
        transcriptembed.add_field(name="Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=True)
        mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
        attachment = mess.attachments[0]
        messages = await ctx.channel.history(limit=None).flatten()
        for msg in messages[::1]:
            if msg.author.id in users.keys():
              users[msg.author.id]+=1
            else:
              users[msg.author.id]=1
        user_string,user_transcript_string="",""
        b = sorted(users.items(), key=lambda x: x[1], reverse=True)
        try:
          for k in b:
            user = await bot.fetch_user(int(k[0]))
            user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
        except NotFound:
          pass
        await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))        
        await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
        await ctx.channel.delete()


@bot.command()
@commands.has_any_role(MMROLE_ID, SUPPORT_ID)
async def rename(ctx, *args):
  cates = [STARTER_TICKETS, NOVICE_TICKETS, MIDDLEMAN_TICKETS, SENIOR_TICKETS, ADV_TICKETS, HEAD_TICKETS, ADMIN_TICKETS, FIRST_TICKETS_CAT, CLOSED_CATEGORY_ID, 1103657193531781200, 995691309601914910]
  if ctx.channel.category.id in cates:
    ents = []

    ticketlogs = bot.get_channel(TICKETLOGS_ID)
    orgname = ctx.channel.name
    neme = ' '.join(args)
    await ctx.channel.edit(name=f"{neme}")
    await asyncio.sleep(1)
    newname = ctx.channel.name
    await ctx.channel.send(embed=discord.Embed(description=f"***{ctx.author.mention} renamed the ticket***\n***> `{orgname}` -> `{newname}`***", color=0x57f287))
    logembed = discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nTicket: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: **Renamed Ticket**", color=0x66BB6A)
    logembed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
    await ticketlogs.send(embed=logembed)
    await ctx.delete()


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.channel)
async def close(ctx):
  rolereq = ctx.guild.get_role(MMROLE_ID)
  closedcategory = bot.get_channel(CLOSED_CATEGORY_ID)
  if rolereq in ctx.author.roles:
    cates = [STARTER_TICKETS, NOVICE_TICKETS, MIDDLEMAN_TICKETS, SENIOR_TICKETS, ADV_TICKETS, HEAD_TICKETS, ADMIN_TICKETS, FIRST_TICKETS_CAT, CLOSED_CATEGORY_ID, 1103657193531781200, 995691309601914910]
    if (ctx.channel.category.id in cates):
      con,cur = openCON()
      cur.execute(f"SELECT * FROM ticket_data WHERE channel_id = '{ctx.channel.id}'")
      i = cur.fetchall()[0] 

      Toggle = True
      if str(i['t_status']) == "Closed" or str(i['t_status']) == "Delete":
        await ctx.reply("*Ticket is already closed!*")
        Toggle = False
        return
      if Toggle == True:        
        await ctx.message.delete()
        ticketlogs = bot.get_channel(TICKETLOGS_ID)
        loading_embed = discord.Embed(color = 0xffffff)
        loading_embed.set_author(name="Gathering Info..", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1")
        msg = await ctx.send(embed=loading_embed)
        for i in ctx.channel.overwrites:
          if type(i) == discord.member.Member:
            if rolereq not in i.roles:
              if rolereq in ctx.author.roles:
                await ctx.channel.set_permissions(i, overwrite=None)
        logembed = discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nTicket: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: **Closed Ticket**", color=0xFFEE58)
        logembed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
        await ticketlogs.send(embed=logembed)
        view = Closed_Msgs()
        await msg.delete()
        msg1 = await ctx.send(embed=discord.Embed(description=f"***{ctx.author.mention} closed the ticket***", color=0xFFEE58), view=view)

        con,cur = openCON()
        cur.execute(f"UPDATE ticket_data SET closed_msg_id='{msg1.id}' WHERE channel_id='{ctx.channel.id}'")
        cur.execute(f"UPDATE ticket_data SET t_status='Closed' WHERE channel_id='{ctx.channel.id}'")            
        con.commit()

        await ctx.channel.edit(category=closedcategory)


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.channel)
async def reopen(ctx):
  rolereq = ctx.guild.get_role(MMROLE_ID)
  guild = bot.get_guild(GUILD_ID)
  cat = bot.get_channel(FIRST_TICKETS_CAT)
  ticketlogs = bot.get_channel(TICKETLOGS_ID)
  if rolereq in ctx.author.roles:
    if (ctx.channel.category.id == FIRST_TICKETS_CAT) or (ctx.channel.category.id == CLOSED_CATEGORY_ID) or ctx.channel.category.id == 1103657193531781200:
      con,cur = openCON()
      cur.execute(f"SELECT * FROM ticket_data WHERE channel_id = '{ctx.channel.id}'")
      i = cur.fetchall()[0] 
      Toggle = True
            
      if str(i['t_status']) == "Open":
        await ctx.reply("*Ticket is not closed!*")
        Toggle = False
        return
      if Toggle == True:
        try:
          closed_msg = await ctx.channel.fetch_message(int(i['closed_msg_id']))
          await closed_msg.delete()
        except NotFound:
          pass
        for y in i['added_users']:
          users = guild.get_member(int(y['user_id']))
          await ctx.channel.set_permissions(users, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True)
        await ctx.channel.edit(category=cat)
        await ctx.reply("*Reopened the ticket.*")
        logembed = discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nTicket: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: **Reopened Ticket**", color=0x29B5F6)
        logembed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
        await ticketlogs.send(embed=logembed)

        con,cur = openCON()
        cur.execute(f"UPDATE ticket_data SET closed_msg_id='0' WHERE channel_id='{ctx.channel.id}'")
        cur.execute(f"UPDATE ticket_data SET t_status='Open' WHERE channel_id='{ctx.channel.id}'")            
        con.commit()


@remove.error
async def remove_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(embed=discord.Embed(description=f"***User is missing!***\n***Usage: `{PREFIX}remove @user` or `{PREFIX}remove userID`***", color=0xed4245))
  if isinstance(error, commands.MemberNotFound):
    await ctx.reply(embed=discord.Embed(description="***User wasn't found!***", color=0xed4245))


@bot.command()
async def transcript(ctx):
  users={}
  rolereq = ctx.guild.get_role(MMROLE_ID)
  ticketlogs = bot.get_channel(TICKETLOGS_ID)
  transcripts = bot.get_channel(TICKETLOGS_ID)
  loading_embed1 = discord.Embed(color = 0xffffff)
  loading_embed1.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
  if (rolereq in ctx.author.roles):
    cates = [STARTER_TICKETS, NOVICE_TICKETS, MIDDLEMAN_TICKETS, SENIOR_TICKETS, ADV_TICKETS, HEAD_TICKETS, ADMIN_TICKETS, FIRST_TICKETS_CAT, CLOSED_CATEGORY_ID, 1103657193531781200, 995691309601914910]
    if (ctx.channel.category.id in cates):
      msg = await ctx.reply(embed=loading_embed1)
      transcript = await chat_exporter.export(channel=ctx.channel, limit=None, tz_info="Asia/Qatar")
      if transcript is None:
        return
      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Author", value=f"{ctx.author.mention} | {ctx.author.id}", inline=True)
      transcriptembed.add_field(name="Ticket", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=True)
      transcriptembed.add_field(name="Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=True)
      mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await ctx.channel.history(limit=None).flatten()
      for msge in messages[::1]:
          if msge.author.id in users.keys():
            users[msge.author.id]+=1
          else:
            users[msge.author.id]=1
      user_string,user_transcript_string="",""
      b = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
        for k in b:
          user = await bot.fetch_user(int(k[0]))
          user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
        pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))      
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
      loading_embed = discord.Embed(description=f"**Transcript was saved in <#{TICKETLOGS_ID}>**",color = 0xffffff)
      await msg.edit(embed=loading_embed)
      #await msg.edit(embed=discord.Embed.set_author(name=f"**Transcript was saved in <#886037854902444073>**"))

@bot.command()
@commands.dm_only()
async def edit_cookie(ctx, *args):
  if (ctx.message.author.id == 358594990982561792) or (ctx.message.author.id == 722113748088782899):
    if not args:
      await ctx.reply("Cookie is missing!")
    else:
      cookie = args[0]
      user = bot.get_user(358594990982561792)
      channel = await user.create_dm()
      chaid = bot.get_channel(channel.id)
      msg = await chaid.fetch_message(912001347585445998)
      await msg.edit(cookie)
      msg1 = await ctx.reply("Cookie was successfully edited.")
      await asyncio.sleep(10)
      await msg1.delete()


@bot.command()
async def s(ctx, *args):

    cookie = await get_cookie()
    Sparkles = Client1(cookies=cookie)

    session = requests.Session()

    if (ctx.message.author.id == 722113748088782899):
      if not args:
          await ctx.reply("Username is missing!")
      else:
        try:
            user = await Sparkles.get_user_by_name(args[0])
            auth_user = await Sparkles.get_auth_user()
            await auth_user.send_friend_request(TargetId=user.id)
            a = session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user.id}&size=720x720&format=Png&isCircular=false")
            ava = a.json()["data"][0]["imageUrl"]
            friendembed=discord.Embed(
                title=f"__**Sparkles's Middleman Services**__",
                description=f"A friend request has been sent to your users in **Roblox**.\n\n• Sparkles's username is [sparklez_mm](https://www.roblox.com/users/2680104132/profile)\n\n• Your roblox user : [{user.name}](https://www.roblox.com/users/{user.id}/profile)",
                color=0x8758FF)
            friendembed.set_image(url="https://cdn.discordapp.com/attachments/884772642576556059/885836855877181480/Purple_Divider_by_Tyson.png")
            friendembed.set_thumbnail(url=ava)

            friendembed1=discord.Embed(
                title=f"__**Sparkles's Middleman Services**__",
                description=f"A friend request has been sent to your users in **Roblox**.\n\n• Sparkles's username is [sparklez_mm](https://www.roblox.com/users/2680104132/profile)\n\n• Your roblox user : [{user.name}](https://www.roblox.com/users/{user.id}/profile)",
                color=0x8758FF)
            friendembed1.set_image(url="https://cdn.discordapp.com/attachments/884772642576556059/885836855877181480/Purple_Divider_by_Tyson.png")

            if (a.json()["data"][0]["state"]) == "Blocked":
              await ctx.reply(embed=friendembed1)
            elif (a.json()["data"][0]["state"]) == "Completed":
              await ctx.reply(embed=friendembed)
            print(f"Friend request was sent to {user.name}")
        except PlayerNotFound:
            await ctx.reply("Username wasn't found.")
        except Unauthorized:
          await ctx.reply("Account is unauthorized (aka. invalid cookie is set).")


@bot.command()
async def delf(ctx):
  if ctx.message.author.id == 722113748088782899: # KOOKIE

    cookie = await get_cookie()
    client = Client1(cookies=cookie)
    cookie = Client2(cookie)

    user1 = await cookie.get_user(2680104132)
    friends = await user1.get_friends()
    users1 = []
    user_string=" "
    for fri in friends:
      users1.append(fri.id)
    for user_id in users1:
      user2 = await cookie.get_user(user_id)
      user_string+=f"{user2.name}\n"
      auth_user = await client.get_auth_user()
      await auth_user.unfriend(TargetId=user2.id)
    number = len(user_string.split())
    number = len(user_string.split())
    header = [user_string]
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(header)
    buffer.seek(0)
    await ctx.reply(f"**{number}** users were removed", file=discord.File(buffer, 'users.txt'))

class Complete_Ticket(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Complete', style=discord.ButtonStyle.green, custom_id="completeticket11", disabled=False, emoji="✅")
  async def button_callback4(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)
    
    users = {}
    role = interaction.guild.get_role(MMROLE_ID)
    msgs = await interaction.channel.history(limit=None).flatten()
    for msg in msgs[::1]:
      try:
        if role in msg.author.roles:
          if msg.author.id in users.keys():
            users[msg.author.id]+=1
          else:
            users[msg.author.id]=1
      except AttributeError:
        pass
    b = sorted(users.items(), key=lambda x: x[1], reverse=True)[:3]
    ids = []
    for k in b:
      ids.append(k[0])
    if interaction.user.id not in ids:
      await interaction.response.send_message(content=f"You can't use this!", ephemeral=True)
      await interaction.message.edit(view=Complete_Ticket())
      return
    
    dbchannel = bot.get_channel(LOGSINFO_ID)
    logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
    while len(logsdata_msg) == 0:
      logsdata_msg = await dbchannel.history(limit=1, oldest_first=True).flatten()
      time.sleep(0.5)
    logsdata_msg=logsdata_msg[0]
    file = logsdata_msg.attachments[0]
    cont = await file.read()
    alldata = ast.literal_eval(cont.decode('utf-8'))
    dataei = ""
    for i in alldata:
      if int(i['userID']) == interaction.user.id:
        dataei = i
    if len(dataei) == 0:
      await interaction.channel.send(f"{interaction.user.mention} You aren't added to the database! Let either Kwite or Sparkles know about this.", delete_after=10)
      await interaction.message.edit(view=Complete_Ticket())
      await interaction.response.defer()
      return
    else:
 
      newdata = []
      for g in alldata:
        if int(g['userID']) == interaction.user.id:
          count = int(g['count'])+1
          g['count'] = count
        if g not in newdata:
          newdata.append(g)
      await updatedb_logs(newdata, logsdata_msg, dbchannel)

      transcript_channel = bot.get_channel(TICKETLOGS_ID)
      ticketlogs = bot.get_channel(TICKETLOGS_ID)
      
      users = {}
      transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Qatar")
      logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel.id}\nAction: **Deleted Ticket**", color=0xed4245)
      await ticketlogs.send(embed=logembed)
      if transcript is None:
        return
      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Author", value=f"{interaction.user.mention} | {interaction.user.id}", inline=True)
      transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel.id}", inline=True)
      transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
      mess = await transcript_channel.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await interaction.channel.history(limit=None).flatten()
      for msg in messages[::1]:
          if msg.author.id in users.keys():
              users[msg.author.id]+=1
          else:
              users[msg.author.id]=1
      user_string,user_transcript_string="",""
      h = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
          for k in h:
              user = await bot.fetch_user(int(k[0]))
              user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
          pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))      
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
      await interaction.channel.delete()

      eeme = discord.Embed(title="Raised (via button)", description=f"**{interaction.user.mention}'s** stats were raised by `+1`\nTicket: [`{interaction.channel.id}`] | [__JUMP URL__]({mess.jump_url})")
      await bot.get_channel(STATS_UPDATES_CHANNELID).send(embed=eeme)
      
      c = bot.get_channel(997526266859241515)
      await c.send(interaction.user.mention)

  @discord.ui.button(row=0, label='No (will delete this msg)', style=discord.ButtonStyle.red, custom_id="nolol", disabled=False, emoji="❌")
  async def button_callback5(self, button, interaction):

    users = {}
    role = interaction.guild.get_role(MMROLE_ID)
    msgs = await interaction.channel.history(limit=None).flatten()
    for msg in msgs[::1]:
      try:
        if role in msg.author.roles:
          if msg.author.id in users.keys():
            users[msg.author.id]+=1
          else:
            users[msg.author.id]=1
      except AttributeError:
        pass
    b = sorted(users.items(), key=lambda x: x[1], reverse=True)[:3]
    ids = []
    for k in b:
      ids.append(k[0])
    if interaction.user.id not in ids:
      await interaction.response.send_message(content=f"You can't use this!", ephemeral=True)
      return
    
    await interaction.message.delete()


@bot.command()
async def stats(ctx):
    role = bot.get_guild(GUILD_ID).get_role(MMROLE_ID)
    if role not in ctx.author.roles:
        return

    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        @discord.ui.button(label="Since a Custom Date", style=discord.ButtonStyle.primary, custom_id="customid1")
        async def button_callback1(self, button, interaction:discord.Interaction):
            modal = MyModal(title="Stats after the period of the customized date")
            await interaction.response.send_modal(modal)
            
        @discord.ui.button(label="Between 2 Dates", style=discord.ButtonStyle.primary, custom_id="customid2")
        async def button_callback2(self, button, interaction:discord.Interaction):
            modal = MyModal1(title="Stats between 2 specified dates")
            await interaction.response.send_modal(modal)
            
        @discord.ui.select(placeholder='View stats since a certain date',
                            min_values=1,
                            max_values=1,
                            custom_id="customdate",
                            options=[
                            discord.SelectOption(label="Today's stats"),
                            discord.SelectOption(label='Stats since 1 day ago'),
                            discord.SelectOption(label='Stats since a week ago'),
                            discord.SelectOption(label='Stats since a month ago')])

        async def select_callback(self, select, interaction:discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return await interaction.response.send_message(content="Only the user who ran the cmd can use this.", ephemeral=True)

            if select.values[0] == "Today's stats":
                await interaction.response.send_message(content=f"Calculating..", ephemeral=True)
                d = datetime.strftime(datetime.now(timezone(timedelta(hours=3))), '%d-%m-%Y').split("-")                
                date = datetime(day=int(d[0]), month=int(d[1]), year=int(d[2]), tzinfo=timezone(timedelta(hours=3)))
                c = bot.get_channel(997526266859241515)
                msgs = await c.history(limit=None, after=date).flatten()
                if len(msgs) == 0:
                    return await interaction.edit_original_response(content="No stats were found since that period of time.")
                users=[]
                for msg in msgs:
                    usee = int(msg.content.split("@")[1].split(">")[0])
                    if len(users) == 0:
                        users += {"userid": usee, "count": 1},
                    else:
                        Toggle = True
                        for i in users:
                            if i["userid"] == usee:
                                i["count"] += 1
                                Toggle = False
                        if Toggle == True:
                            users += {"userid": usee, "count": 1},
                users.sort(key=itemgetter('count'), reverse=True)
                user_string_2 = ""
                rank = 0
                total_count = len(msgs)
                for i in users:
                    rank+=1
                    if rank == 1:
                        user_string_2+=f"╭・⋯・⋯・⋯・⋯・⋯・⋯・⋯・\n> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    elif rank == 2:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    elif rank == 3:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    else:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                user_string_2+=f"╰・⋯・⋯・⋯・⋯・⋯・⋯・⋯・"
                embed = discord.Embed(title=f"**__Middleman Stats For `Today` `[{total_count}]`__**", description=f"{user_string_2}", color=nocolour)
                embed.set_footer(text="Timezone: UTC+3")
                await interaction.message.edit(embed=embed)
                await interaction.edit_original_response(content="Message updated!")


            if select.values[0] == "Stats since 1 day ago":
                await interaction.response.send_message(content=f"Calculating..", ephemeral=True)
                d = datetime.strftime(datetime.now(timezone(timedelta(hours=3))) - timedelta(1), '%d-%m-%Y').split("-")
                date = datetime(day=int(d[0]), month=int(d[1]), year=int(d[2]), tzinfo=timezone(timedelta(hours=3)))
                c = bot.get_channel(997526266859241515)
                msgs = await c.history(limit=None, after=date).flatten()
                if len(msgs) == 0:
                    return await interaction.edit_original_response(content="No stats were found since that period of time.")
                users=[]
                for msg in msgs:
                    usee = int(msg.content.split("@")[1].split(">")[0])
                    if len(users) == 0:
                        users += {"userid": usee, "count": 1},
                    else:
                        Toggle = True
                        for i in users:
                            if i["userid"] == usee:
                                i["count"] += 1
                                Toggle = False
                        if Toggle == True:
                            users += {"userid": usee, "count": 1},
                users.sort(key=itemgetter('count'), reverse=True)
                user_string_2 = ""
                rank = 0
                total_count = len(msgs)
                for i in users:
                    rank+=1
                    if rank == 1:
                        user_string_2+=f"╭・⋯・⋯・⋯・⋯・⋯・⋯・⋯・\n> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    elif rank == 2:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    elif rank == 3:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    else:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                user_string_2+=f"╰・⋯・⋯・⋯・⋯・⋯・⋯・⋯・"
                embed = discord.Embed(title=f"**__Middleman Stats For The Past `Day` `[{total_count}]`__**", description=f"{user_string_2}", color=nocolour)
                embed.set_footer(text="Timezone: UTC+3")
                await interaction.message.edit(embed=embed)
                await interaction.edit_original_response(content="Message updated!")

            elif select.values[0] == "Stats since a week ago":
                await interaction.response.send_message(content=f"Calculating..", ephemeral=True)
                d = datetime.strftime(datetime.now(timezone(timedelta(hours=3))) - timedelta(7), '%d-%m-%Y').split("-")
                date = datetime(day=int(d[0]), month=int(d[1]), year=int(d[2]), tzinfo=timezone(timedelta(hours=3)))
                c = bot.get_channel(997526266859241515)
                msgs = await c.history(limit=None, after=date).flatten()
                if len(msgs) == 0:
                    return await interaction.edit_original_response(content="No stats were found since that period of time.")
                users=[]
                for msg in msgs:
                    usee = int(msg.content.split("@")[1].split(">")[0])
                    if len(users) == 0:
                        users += {"userid": usee, "count": 1},
                    else:
                        Toggle = True
                        for i in users:
                            if i["userid"] == usee:
                                i["count"] += 1
                                Toggle = False
                        if Toggle == True:
                            users += {"userid": usee, "count": 1},
                users.sort(key=itemgetter('count'), reverse=True)
                user_string_2 = ""
                rank = 0
                total_count = len(msgs)
                for i in users:
                    rank+=1
                    if rank == 1:
                        user_string_2+=f"╭・⋯・⋯・⋯・⋯・⋯・⋯・⋯・\n> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    elif rank == 2:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    elif rank == 3:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    else:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                user_string_2+=f"╰・⋯・⋯・⋯・⋯・⋯・⋯・⋯・"
                embed = discord.Embed(title=f"**__Middleman Stats For The Past `Week` `[{total_count}]`__**", description=f"{user_string_2}", color=nocolour)
                embed.set_footer(text="Timezone: UTC+3")
                await interaction.message.edit(embed=embed)
                await interaction.edit_original_response(content="Message updated!")
                
            elif select.values[0] == "Stats since a month ago":
                await interaction.response.send_message(content=f"Calculating..", ephemeral=True)
                d = datetime.strftime(datetime.now(timezone(timedelta(hours=3))) - timedelta(30), '%d-%m-%Y').split("-")
                date = datetime(day=int(d[0]), month=int(d[1]), year=int(d[2]), tzinfo=timezone(timedelta(hours=3)))
                c = bot.get_channel(997526266859241515)
                msgs = await c.history(limit=None, after=date).flatten()
                if len(msgs) == 0:
                    return await interaction.edit_original_response(content="No stats were found since that period of time.")
                users=[]
                for msg in msgs:
                    usee = int(msg.content.split("@")[1].split(">")[0])
                    if len(users) == 0:
                        users += {"userid": usee, "count": 1},
                    else:
                        Toggle = True
                        for i in users:
                            if i["userid"] == usee:
                                i["count"] += 1
                                Toggle = False
                        if Toggle == True:
                            users += {"userid": usee, "count": 1},
                users.sort(key=itemgetter('count'), reverse=True)
                user_string_2 = ""
                rank = 0
                total_count = len(msgs)
                for i in users:
                    rank+=1
                    if rank == 1:
                        user_string_2+=f"╭・⋯・⋯・⋯・⋯・⋯・⋯・⋯・\n> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    elif rank == 2:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    elif rank == 3:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                    else:
                        user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                user_string_2+=f"╰・⋯・⋯・⋯・⋯・⋯・⋯・⋯・"
                embed = discord.Embed(title=f"**__Middleman Stats For The Past `Month` `[{total_count}]`__**", description=f"{user_string_2}", color=0x303135)
                embed.set_footer(text="Timezone: UTC+3")
                await interaction.message.edit(embed=embed)
                await interaction.edit_original_response(content="Message updated!")

    class MyModal(Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            daa = datetime.now(timezone(timedelta(hours=3))).strftime("%d-%m-%Y")
            #self.add_item(InputText(label="Today's date in case you forgot..", required=False, style=discord.InputTextStyle.short, value=f"{daa}"))
            self.add_item(InputText(label="Day in numbers", placeholder="Example: 15", max_length=2, required=True, style=discord.InputTextStyle.short))
            self.add_item(InputText(label="Month in numbers", placeholder="Example: 3", max_length=2, required=True, style=discord.InputTextStyle.short))
            self.add_item(InputText(label="Year in numbers", placeholder="Example: 2024", max_length=4, required=True, style=discord.InputTextStyle.short, value="2024"))

        async def callback(self, interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return await interaction.response.send_message(content="Only the user who ran the cmd can use this.", ephemeral=True)

            try:
                if int(self.children[0].value) > 31: return await interaction.response.send_message(content="Maximum amount of days is 31!", ephemeral=True)
                if int(self.children[1].value) > 12: return await interaction.response.send_message(content="Maximum amount of months is 12!", ephemeral=True)
                # if int(self.children[2].value) != 2022: return await interaction.response.send_message(content="2022 is the only available year!", ephemeral=True)
            except ValueError:
                return await interaction.response.send_message(content="The inputs must be numbers!", ephemeral=True)

            date = datetime(day=int(self.children[0].value),
                            month=int(self.children[1].value),
                            year=int(self.children[2].value))
            
            if date.timestamp() > datetime.now(timezone(timedelta(hours=3))).timestamp():
                return await interaction.response.send_message(content="TF u tryna do?! You can't select a date that is in the future :/", ephemeral=True)
            
            await interaction.response.send_message(content=f"Calculating..", ephemeral=True)
            
            c = bot.get_channel(997526266859241515)
            msgs = await c.history(limit=None, after=date).flatten()
            
            if len(msgs) == 0:
                return await interaction.edit_original_response(content="No stats were found since that period of time.")
                        
            users=[]
            for msg in msgs:
                usee = int(msg.content.split("@")[1].split(">")[0])
                if len(users) == 0:
                    users += {"userid": usee, "count": 1},
                else:
                    Toggle = True
                    for i in users:
                        if i["userid"] == usee:
                            i["count"] += 1
                            Toggle = False
                    if Toggle == True:
                        users += {"userid": usee, "count": 1},
            users.sort(key=itemgetter('count'), reverse=True)
            user_string_2 = ""
            rank = 0
            total_count = len(msgs)
            for i in users:
                rank+=1
                if rank == 1:
                    user_string_2+=f"╭・⋯・⋯・⋯・⋯・⋯・⋯・⋯・\n> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                elif rank == 2:
                    user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                elif rank == 3:
                    user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                else:
                    user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
            user_string_2+=f"╰・⋯・⋯・⋯・⋯・⋯・⋯・⋯・"
            embed = discord.Embed(title=f"**__Middleman Stats Since <t:{int(str(date.timestamp()).split('.')[0])}:R> `[{total_count}]`__**", description=f"{user_string_2}", color=nocolour)
            embed.set_footer(text="Timezone: UTC+3")
            await interaction.message.edit(embed=embed)
            await interaction.edit_original_response(content="Message updated!")

    class MyModal1(Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            daa = datetime.now(timezone(timedelta(hours=3))).strftime("%d-%m-%Y")
            #self.add_item(InputText(label="Today's date in case you forgot..", required=False, style=discord.InputTextStyle.short, value=f"{daa}"))
            self.add_item(InputText(label="First Date (When it starts)", placeholder="Example: 25-3 (day-month)", max_length=4, required=True, style=discord.InputTextStyle.short))
            self.add_item(InputText(label="Second Date (When it ends)", placeholder="Example: 12-4 (day-month)", max_length=4, required=True, style=discord.InputTextStyle.short))

        async def callback(self, interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return await interaction.response.send_message(content="Only the user who ran the cmd can use this.", ephemeral=True)

            try:
              date1 = datetime(day=int(self.children[0].value.split("-")[0]),
                              month=int(self.children[0].value.split("-")[1]),
                              year=2022, tzinfo=timezone(timedelta(hours=3)))
              
              date2 = datetime(day=int(self.children[1].value.split("-")[0]),
                              month=int(self.children[1].value.split("-")[1]),
                              year=2022, tzinfo=timezone(timedelta(hours=3)))
            except IndexError or ValueError:
              return await interaction.response.send_message(content="Something went wrong.. make sure you've used the correct format aka. `day-month` , the - is required. And only include numbers.", ephemeral=True)
            
            #if date1.timestamp() > datetime.now(timezone(timedelta(hours=3))).timestamp() or date2.timestamp() > datetime.now(timezone(timedelta(hours=3))).timestamp():
            #    return await interaction.response.send_message(content="TF u tryna do?! You can't select a date that is in the future :/", ephemeral=True)
            
            await interaction.response.send_message(content=f"Calculating..", ephemeral=True)
            
            c = bot.get_channel(997526266859241515)
            msgs = await c.history(limit=None, after=date1, before=date2).flatten()
            
            if len(msgs) == 0:
                return await interaction.edit_original_response(content="No stats were found between those periods of time.")
                        
            users=[]
            for msg in msgs:
                usee = int(msg.content.split("@")[1].split(">")[0])
                if len(users) == 0:
                    users += {"userid": usee, "count": 1},
                else:
                    Toggle = True
                    for i in users:
                        if i["userid"] == usee:
                            i["count"] += 1
                            Toggle = False
                    if Toggle == True:
                        users += {"userid": usee, "count": 1},
            users.sort(key=itemgetter('count'), reverse=True)
            user_string_2 = ""
            rank = 0
            total_count = len(msgs)
            for i in users:
                rank+=1
                if rank == 1:
                    user_string_2+=f"╭・⋯・⋯・⋯・⋯・⋯・⋯・⋯・\n> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                elif rank == 2:
                    user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                elif rank == 3:
                    user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
                else:
                    user_string_2+=f"> **{rank}.** | Tickets: `{i['count']}`, `[{percentage(int(i['count']), int(total_count))}%]` - User: **<@{i['userid']}>**\n"
            user_string_2+=f"╰・⋯・⋯・⋯・⋯・⋯・⋯・⋯・"
            embed = discord.Embed(title=f"**__Middleman Stats Between <t:{int(str(date1.timestamp()).split('.')[0])}:d> And <t:{int(str(date2.timestamp()).split('.')[0])}:d> `[{total_count}]`__**", description=f"{user_string_2}", color=nocolour)
            embed.set_footer(text="Timezone: UTC+3")
            await interaction.message.edit(embed=embed)
            await interaction.edit_original_response(content="Message updated!")


    view = MyView()
    await ctx.reply(view=view)

def percentage(part, whole):
  return round(100 * float(part)/float(whole), 2)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit=None):
  if limit == None:
    return await ctx.reply("Please specify the amount of the messages.")
  
  try:
    limit = int(limit)
  except ValueError:
    return await ctx.reply("Amount of messages must be a number!")
  
  if limit == 0:
    return await ctx.reply("The amount can't be 0!")
  
  msgs = await ctx.channel.purge(limit=limit+1, oldest_first=False, bulk=True)
  limit = limit-1
  await ctx.send(f"{ctx.author.mention} Successfully purged `{len(msgs)-1}` messages")
  c = bot.get_channel(1147241361351905391)
  embed = discord.Embed(color=0xed4245)
  embed.set_author(name=f"Purged {len(msgs)-1} messages in {ctx.channel.name} | {ctx.channel.id}", icon_url=f"{ctx.author.display_avatar.url}")
  embed.add_field(name="User", value=ctx.author.mention, inline=False)
  await c.send(embed=embed)


@bot.event
async def on_member_join(member):
  if member.guild.id == GUILD_ID:
    wlc_channel = bot.get_channel(1147234838311616612)
    wlcmsg = discord.Embed(title=f"Welcome to Sparkles MM", description=f"<a:wkd:913881762906669067> Check these out !\n<:dot_white:1147383543429873694> <#1147235223835250850>\n<:dot_white:1147383543429873694> <#1147234926853361744>\n<:dot_white:1147383543429873694>  <#1147235245259751455>\n✦ . 　⁺ 　 . . 　⁺ 　 . ✦ .", color=maincolor)
    wlcmsg.set_author(name=f"{member.name}#{member.discriminator}", icon_url = f"{member.display_avatar.url}")
    wlcmsg.set_footer(text=f"{member.name}#{member.discriminator} is a new member!")
    await wlc_channel.send(f"{member.mention}", embed=wlcmsg)

    invc = bot.get_channel(1147241471259463700)
    invites_before_join = invites[member.guild.id]
    invites_after_join = await member.guild.invites()

    for invite in invites_before_join:
          
        if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
              
            embed = discord.Embed(title=f"Member Joined", color=discord.Color.blurple())
            embed.add_field(name=f"Member", value=f"{member.id} - {member.mention} - {member}", inline=False)
            embed.add_field(name=f"Inviter", value=f"{invite.inviter.id} - {invite.inviter.mention} - {invite.inviter}", inline=False)   
            if invite.code == None:
              embed.add_field(name=f"Invite Code", value=".gg/sparklesmms", inline=False)
            else:
              embed.add_field(name=f"Invite Code", value=f"`{invite.code}`", inline=False)
              embed.add_field(name=f"Account Creation",  value=f"<t:{int(member.created_at.timestamp())}> - <t:{int(member.created_at.timestamp())}:R>", inline=False)

              await invc.send(embed=embed)

            invites[member.guild.id] = invites_after_join
            return


TicketAccess = [358594990982561792, 722113748088782899]

@bot.command()
async def market(ctx):
  if (ctx.message.author.id == 1037772222145765406) or (ctx.message.author.id == 722113748088782899):
    await ctx.send(view=Marketplace())


class Marketplace(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)
        @discord.ui.button(label="Marketplace", style=discord.ButtonStyle.blurple, custom_id="marketplace")
        async def marketplace(self, button, interaction:discord.Interaction):
          await interaction.response.send_message(content=f"https://discord.gg/UfvayAc5AK", ephemeral=True)


@bot.command()
async def i(ctx, username=None): 
      if username == None:
        await ctx.reply("Username is missing!")
      else:
        user = await client.get_user_by_username(username)
        embed = discord.Embed(title=f"**Userinfo for** {user.name}", color=nocolour)
        embed.add_field(name="Username", value=f"[{user.name}](https://www.roblox.com/users/{user.id}/profile)")
        embed.add_field(name="Display Name", value="`" + user.display_name + "`")
        embed.add_field(name="User ID", value="`" + str(user.id) + "`")
        embed.add_field(name="Created", value="```" + user.created.strftime("%m/%d/%Y, %H:%M %p") + "```")

        avatar_res = session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user.id}&size=720x720&format=Png&isCircular=false")
        avatar_url = avatar_res.json()["data"][0]["imageUrl"]

        embed.set_thumbnail(url=avatar_url)

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Profile Link", url=f"https://www.roblox.com/users/{user.id}/profile", style=discord.ButtonStyle.url))

        await ctx.reply(embed=embed, view=view)

headers = {
    'authority': 'games.roblox.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # Requests sorts cookies= alphabetically
    'cookie': 'GuestData=UserID=-1699480281; gig_bootstrap_3_OsvmtBbTg6S_EUbwTPtbbmoihFY5ON6v6hbVrTbuqpBs7SyF_LQaJwtwKJ60sY1p=_gigya_ver4; .RBXID=_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI2OTFkZTcyYS1lYmFiLTRkMzUtOWIxOC1hNjU4MTAxNjE1YTkiLCJzdWIiOjM3NjgxODY4Mn0.4li6xuRTLFPfDvxxRBwqZgzqWxjwYpadLCE1B5oQUlI; _ga=GA1.2.1942504467.1651860978; .ROBLOSECURITY=_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_FF3A30EDBBC2186883EE8C7269B4CAFC4ED411BE6F8ECBC56C2E6A0F4B30D3110253A29EE85BFA583355EF63F86A5B8D03E92746662102B25F995A2B41DB830F401A86D5F93EAEEF03BB826E0E95CC4F41929B3074D9747F8BE9D7ECF835941BD70C0F9DDA06C777A0FB5875525617A69B838914BF02FAC0BF9A69AAEA206DD21EE2B51E1F120BAFBB3C1D7B94092959F7CE45090F621F78DABDE5AF6808B85AF708E38FC008EB7627335F1BBED818F65006F1F7C6F87538BA712633935762CA20FDD17F117902CB7DC0D32E9E469E9D8738B6512BBCF95DEBA4520EE01AF635E3795A108124C2BD8D857C773201FCE3B8F2AAEB758BE3BAD0FAF5CEC959E114A85ADBCA673CC90FF1D1652F7F5B5DFF3183080209E4E3C388273664B2549B4A0B0B94D398FCC042E26626E69F0E94C9446E3497D6A919BC9BFB1BA210FD7636852AD3E1A879ADACDC469963DDA9C12E6577CEEA558F96A6FC802691778C8F0314E0BC510A56C142C255A3E9C531BF6BE9AE645F91E7C821A02B8B0274709AC02001188182A8F33FB8F56DCD024351A112A966E1D55D408D2D32B19CA2F1D15539BF0293B524E6302222AABA8182C2B680BEDDE326CE5ECD0A362E2304CE4CE4A5D4FD2676D7D501FD9D6A5513477190BAA08379B041AE59C058136385B10E2E7A74ED9C852DE545465C1E7AB0D35FD5C78E7BC12710C8C4980AF1E6F0E75ADB931CEF3DA957A9262B91B00F3564A65885B0F73D223D19C39D6E876999BD9DE59F4745F6993472CEA239ACBEABFA88D500B3C25EAD32FA07524913DB7723649914DBF44E4D10A4A7FFABBC37586BC78F0EDBF765AA98CE485934C5AFD0630B182F9C9E19B19185231A1028A2862182B5D6BCA4BB9FC2D95D83221713B035D2E2499D9C5413C73A5B92CC1F8F358966E24751DD1D34264F2DBC24D61E7A728EA3200E5BA9720AAF1A76BF7F99508E9B6A1C8D70FF1A0B22D8E750077417C923F6386F24D3D061894EB9CE877C9536DE83CD95D83A6696F67599F62DFD14F53770A9E9BFB8; .RBXIDCHECK=8a95a8b8-bf28-42c6-a5f4-da4851994352,b9eebd55-839b-4d3d-afb3-7a24c1273f29; RBXEventTrackerV2=CreateDate=5/24/2022 1:28:35 PM&rbxid=3521560014&browserid=123027170643; RBXSessionTracker=sessionid=95c9c5c6-63c8-413b-9a2d-df65a160070a; rbx-ip2=',
    'origin': 'https://www.roblox.com',
    'referer': 'https://www.roblox.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
  }


@bot.command()
@commands.has_any_role(MMROLE_ID, SUPPORT_ID)
async def cam(ctx):
    c = requests.get("https://games.roblox.com/v1/games/920587237/private-servers", headers=headers)
    json_result = c.json()
    vip_server_data = json_result["data"][0]
    players = vip_server_data["players"]
    playing = vip_server_data.get("playing", 0)

    embed = discord.Embed(title="Information for Adopt Me VIP Server", description=f"Users **in** VIP: `{playing}`", color=discord.Colour.og_blurple())

    if not players:
        embed = discord.Embed(title="Information for VIP Server", description=f"Players **present**: `{playing}`", color=discord.Colour.red())
    else:
        for player in players:
            id = player["id"]
            name = player["name"]
            display_name = player["displayName"]
            
            embed.add_field(name=f"・{display_name}", value=f"[{name}](https://www.roblox.com/users/{id}/profile) - {id}", inline=False)
        
    await ctx.reply(embed=embed)

@bot.command()
@commands.has_any_role(MMROLE_ID, SUPPORT_ID)
async def cmm2(ctx):
    c = requests.get("https://games.roblox.com/v1/games/142823291/private-servers", headers=headers)
    json_result = c.json()
    vip_server_data = json_result["data"][0]
    players = vip_server_data["players"]
    playing = vip_server_data.get("playing", 0)


    embed = discord.Embed(title="Information for MM2 VIP Server", description=f"Users **in** VIP: `{playing}`", color=discord.Colour.og_blurple())

    if not players:
        embed = discord.Embed(title="Information for VIP Server", description=f"Players **present**: `{playing}`", color=discord.Colour.red())
    else:
        for player in players:
            id = player["id"]
            name = player["name"]
            display_name = player["displayName"]
            
            embed.add_field(name=f"・{display_name}", value=f"[{name}](https://www.roblox.com/users/{id}/profile) - {id}", inline=False)
        
    await ctx.reply(embed=embed)


bot.run(TOKEN)
