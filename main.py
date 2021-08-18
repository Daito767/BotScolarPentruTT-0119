import config
import os
import inspect
import asyncio
import discord
import discord.ext
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

TOKEN = ''
if 'local_config.py' in os.listdir('.'):
	import local_config
	TOKEN = local_config.TOKEN
else:
	TOKEN = config.get_token()


intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', case_insensitive=True)

client.remove_command("help")
cog_names = []
num_of_live_schedule_threads = 0


def is_command_allowed(func):
	async def decorator(*args, **kwargs):
		if inspect.getfullargspec(func).args[0] == 'self':
			ctx = args[1]
		else:
			ctx = args[0]

		if ctx.author.bot:
			return

		if ctx.channel.id == 753531622757761105 or str(ctx.author) == 'Daito#8141':
			await func(*args, **kwargs)
		elif ctx.channel.type is discord.ChannelType.private:
			await ctx.channel.send(f'Salut {ctx.author.mention}, nu aveți permisiunea de a executa comenzi înafara serverului.')
		else:
			await ctx.message.delete()

	decorator.__name__ = func.__name__
	sig = inspect.signature(func)
	decorator.__signature__ = sig.replace(parameters=tuple(sig.parameters.values()))
	return decorator


@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Gravity Falls'))
	DiscordComponents(client)
	print('----------Ready---------')


@client.event
async def on_message(message: discord.Message):
	if message.author.bot and str(message.channel.id) != '754018313029288127' and str(message.channel.id) != '753531622757761105':
		if str(message.author) != 'ZyBot#3764' and str(message.author) != 'DyBot#6312':
			await message.delete()
			return

	await client.process_commands(message)


# @client.event
# async def on_command_error(ctx, error):
#	await ctx.channel.send(f'Salut {ctx.author.mention}. {error}')


@client.command(pass_context=True, aliases=['a', 'ajutor', 'cmd', 'h'])
@is_command_allowed
async def help(ctx: discord.ext.commands.Context):
	embed = discord.Embed(title=f'Informație despre comenzi', description=f'Salut {ctx.author.mention}, pentru mai multe informații vă puteți adresa unui :technologist: **Admin**.', color=discord.Colour.from_rgb(175, 245, 71))
	embed.add_field(name=':date: Orarul  :timer:', value='**!o** sau **!ora** sau **!orar** - oferă un set de funcții legate de afișarea orarului. Puteți găsi mai multe detalii după introducerea comenzii.', inline=False)
	embed.add_field(name=':robot: Statutul bot-ului', value='**!s**  sau **!statut**  sau **!status** - aceasta comandă va permite sa setați statul bot-ului. Puteți găsi mai multe detalii după introducerea comenzii.', inline=False)
	embed.add_field(name=':interrobang: Ajutor :gear:', value='**!h**  sau **!help**  sau **!a** sau **!ajutor** sau **!cmd** - oferă informație despre comenzile disponibile pentru executare.', inline=False)
	await ctx.channel.send(embed=embed)


@client.command(pass_context=True, aliases=['cog', 'c'])
@is_command_allowed
async def cogs(ctx, *args):
	msg_text = f'Salut {ctx.author.mention}. Alegeti operatiunea dorita de dumneavoastra.'
	btn_reload = Button(style=ButtonStyle.green, label='Reincarca', id='reload')
	btn_load = Button(style=ButtonStyle.blue, label='Incarca', id='load')
	btn_unload = Button(style=ButtonStyle.red, label='Descarca', id='unload')
	msg = await ctx.channel.send(msg_text, components=[[btn_reload, btn_load, btn_unload]])

	def check(m):
		return m.channel == ctx.channel and (m.component.id == 'reload' or m.component.id == 'load' or m.component.id == 'unload')

	try:
		response = await client.wait_for('button_click', timeout=4, check=check)
	except asyncio.TimeoutError:
		await ctx.message.delete()
		await msg.delete()
	else:
		await msg.delete()
		global cog_names
		args_without_error = []
		args = list(args)
		if len(args) == 0:
			args = cog_names.copy()

		for arg in args:
			if response.component.id == 'load':
				if not f'{arg}.py' in os.listdir('./cogs'):
					await ctx.channel.send(f'**[ERROR]** Salut {ctx.author.mention}. Cog-ul: "{arg}" nu exitsa.', components=[])
				elif arg in cog_names:
					await ctx.channel.send(f'**[ERROR]** Salut {ctx.author.mention}. Cog-ul: "{arg}" a fost deja incarcat.', components=[])
				else:
					client.load_extension(f'cogs.{arg}')
					cog_names.append(arg)
					args_without_error.append(arg)
			elif response.component.id == 'reload':
				if not f'{arg}.py' in os.listdir('./cogs'):
					await ctx.channel.send(f'**[ERROR]** Salut {ctx.author.mention}. Cog-ul: "{arg}" nu exitsa.', components=[])
				elif arg not in cog_names:
					await ctx.channel.send(f'**[ERROR]** Salut {ctx.author.mention}. Cog-ul: "{arg}" nu a fost incarcat.', components=[])
				else:
					client.reload_extension(f'cogs.{arg}')
					args_without_error.append(arg)
			elif response.component.id == 'unload':
				if arg in cog_names:
					client.unload_extension(f'cogs.{arg}')
					cog_names.remove(arg)
					args_without_error.append(arg)
				else:
					await ctx.channel.send(f'**[ERROR]** Salut {ctx.author.mention}. Cog-ul: "{arg}" nu a fost incarcat.', components=[])

		msg_text = f'Salut {ctx.author.mention}. Operatiunea "{response.component.label} : {str(args_without_error)}" a fost executata cu succes.'
		await ctx.channel.send(msg_text, components=[])


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')
		cog_names.append(filename[:-3])

client.run(TOKEN)
