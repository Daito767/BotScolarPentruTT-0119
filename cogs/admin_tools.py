import discord
import os
import discord.ext
import config
import asyncio
from discord.ext import commands, tasks
import main
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType, Select, SelectOption


class AdminTools(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(pass_context=True, aliases=['s', 'statut'])
	@main.is_command_allowed
	async def status(self, ctx, *args):
		def add_field_activity_type(e):
			e.add_field(name='Tipul de activitate', value=f'Activitatea executata de bot.\n(Se joacă :video_game:, Vizionează :film_frames:, Acultă :headphones:)', inline=True)

		def add_field_status_type(e):
			e.add_field(name='Starea in rețea', value=f'Starea a bot-ului în rețea.\n(Online :green_circle:, Inactiv :crescent_moon:, Nu deranja :no_entry:)', inline=True)

		if len(args) == 0:
			embed = discord.Embed(title=f'Setarea statutului', description=f'Salut {ctx.author.mention}. Cu ajutorul acestei comenzi setați statutul bot-ului.\n**[ERROR]** Trebuie să adăugați denumirea activității.\nExemplu: **!statut** `Denumirea activității` sau **!s** `Denumirea activității`', color=discord.Colour.red())
			add_field_activity_type(embed)
			add_field_status_type(embed)
			await ctx.channel.send(embed=embed)
			return

		activity_name = ''
		for arg in args:
			if arg == args[0]:
				activity_name += arg
			else:
				activity_name += ' ' + arg

		embed = discord.Embed(title=f'Setarea statutului', description=f'Salut {ctx.author.mention}. Cu ajutorul acestei comenzi setați statutul bot-ului. Mesajul va fi ștres după 40 secunde de inacativitate.', color=discord.Colour.blue())
		add_field_activity_type(embed)
		add_field_status_type(embed)
		embed.add_field(name='Selectați tipul activității și starea in rețea a bot-ului:', value='Alegeți câte o opțiune din meniurile de selectare. :arrow_down:', inline=False)

		so_play = SelectOption(label=f'Se joacă acum: {activity_name}', value='Se joacă', description='', emoji='🎮')
		so_watch = SelectOption(label=f'Urmărește: {activity_name}', value='Vizionează', description='', emoji='🎬')
		so_listen = SelectOption(label=f'Ascultă pe {activity_name}', value='Acultă', description='', emoji='🎧')
		activity_select = Select(placeholder='Alegeti tipul de acivitate:', options=[so_play, so_watch, so_listen])

		so_online = SelectOption(label=f'Online', value='Online', description='', emoji='🟢')
		so_idle = SelectOption(label=f'Inactiv', value='Inactiv', description='', emoji='🌙')
		so_do_not_distrub = SelectOption(label=f'Nu deranja', value='Nu deranja', description='', emoji='⛔')
		status_select = Select(placeholder='Alegeti starea in rețea:', options=[so_online, so_idle, so_do_not_distrub])

		the_bot_msg = await ctx.channel.send(embed=embed, components=[activity_select, status_select])

		# Afigurarea functionalitatii butoanelor.
		def check(the_event):
			return the_event.message.id == the_bot_msg.id

		activity_type = None
		status_type = None
		activity_text = ''
		status_text = ''
		while activity_type is None or status_type is None:
			try:
				event = await self.client.wait_for('select_option', timeout=39, check=check)
				await event.respond(type=InteractionType.DeferredUpdateMessage)
				value = event.interacted_component[0].value
			except asyncio.TimeoutError:
				await the_bot_msg.delete()
				await ctx.message.delete()
				return
			else:
				if value == so_play.value:
					activity_type = discord.Game(activity_name)
					activity_text = so_play.label
				elif value == so_watch.value:
					activity_type = discord.Activity(type=discord.ActivityType.watching, name=activity_name)
					activity_text = so_watch.label
				elif value == so_listen.value:
					activity_type = discord.Activity(type=discord.ActivityType.listening, name=activity_name)
					activity_text = so_listen.label
				elif value == so_online.value:
					status_type = discord.Status.online
					status_text = so_online.label
				elif value == so_idle.value:
					status_type = discord.Status.idle
					status_text = so_idle.label
				elif value == so_do_not_distrub.value:
					status_type = discord.Status.dnd
					status_text = so_do_not_distrub.label

		await self.client.change_presence(status=status_type, activity=activity_type)

		embed = discord.Embed(title=f'Setarea statutului', description=f'Salut {ctx.author.mention}. **Ați setat statutul bot-ului cu succes**. Posibil va dura puțin, până când se va aplica setarea: `{activity_text}` cu statutul in rețea: `{status_text}`.', color=discord.Colour.green())
		add_field_activity_type(embed)
		add_field_status_type(embed)

		await the_bot_msg.edit(embed=embed, components=[])


def setup(client):
	client.add_cog(AdminTools(client))
