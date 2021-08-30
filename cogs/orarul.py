import main
import config
import asyncio
import pytz
import datetime
import discord
import discord.ext
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle


def get_schedule_on_weekday(mention, day):
	return f'Salut {mention}. Acesta este orarul lecțiilor pe {day}.{config.orarul_total_al_orelor[day]}'


def get_time_schedule(mention):
	def fomrat(num):
		num = str(num)
		if len(num) == 1:
			num = '0' + num
		return num

	text = f'Salut {mention}. Acesta este orarul sunetelor.'
	lesson_num = 1
	for lesson in config.orarul_sunetelor:
		text += f'\n`{lesson_num}. {fomrat(int(lesson[0]/60))}:{fomrat(lesson[0]%60)} - {fomrat(int(lesson[1]/60))}:{fomrat(lesson[1]%60)}`'
		lesson_num += 1
	return text


def get_schedule_on_all_weekdays(mention):
	embed = discord.Embed(title=f'Orarul lecțiilor', description=f'Salut {mention}. Acesta este orarul lecțiilor pe toată săptămâna.', color=discord.Colour.gold())
	for day in config.zilele_scolare:
		embed.add_field(name=day.capitalize(), value=config.orarul_total_al_orelor[day], inline=True)

	return embed


async def start_live_schedule(editable_msg, mention):
	def fomat_len(n):
		n = str(n)
		if len(n) == 1:
			n = '0' + n
		return n

	def format_dt_now(dt):
		return f'{fomat_len(dt.day)} {fomat_len(dt.month)} {fomat_len(dt.year)}   {fomat_len(dt.hour)}:{fomat_len(dt.minute)}:{fomat_len(dt.second)}:{fomat_len(dt.microsecond)}'

	if main.num_of_live_schedule_threads > 10:
		main.num_of_live_schedule_threads = 0

	main.num_of_live_schedule_threads += 1
	num_of_threads = main.num_of_live_schedule_threads
	# time_delta = datetime.datetime(2021, 8, 16, 11, 29, 50) - datetime.datetime.now()  # Pentru testare.
	editable_msg_text = ''

	while True:
		if num_of_threads != main.num_of_live_schedule_threads:
			await editable_msg.edit(content=editable_msg_text + '   **Actualizarea a fost intrerupta**')
			return

		dt_now = datetime.datetime.now(pytz.timezone("Europe/Chisinau"))
		# dt_now = datetime.datetime.now() + time_delta  # Pentru testare.
		time_now = dt_now.hour * 60 + dt_now.minute
		imparitate = dt_now.isocalendar()[1] % 2
		day = dt_now.weekday()

		if day == 5:
			await editable_msg.edit(content=f"Salut {mention}. Azi este sambată.")
			return
		if day == 6:
			await editable_msg.edit(content=f"Salut {mention}. Azi este duminică.")
			return

		day_name = config.zilele_scolare[day]

		if time_now < config.orarul_sunetelor[0][0]:
			await editable_msg.edit(content=f'Salut {mention}. Lecțiile incă nu s-au inceput.')
			return
		if config.orarul_sunetelor[len(config.orarul_orelor[imparitate][day_name]) - 1][1] <= time_now:
			await editable_msg.edit(content=f'Salut {mention}. Lecțiile s-au finalizat.')
			return

		# Cilul in care se contruiste mesaju pentru editare.
		count = 0
		editable_msg_text = f'Salut {mention}. Aceasta este orarul extins in săptămână {config.denumirea_paritatii[imparitate]} a lecțtiilor pe {day_name}.'
		# Se verifica daca lectia deja decurge.
		while count < len(config.orarul_orelor[imparitate][day_name]):
			if config.orarul_sunetelor[count][0] <= time_now < config.orarul_sunetelor[count][1]:
				minutes = config.orarul_sunetelor[count][1] - time_now - 1
				seconds = 60 - dt_now.second
				editable_msg_text += f'\n**{config.orarul_orelor[imparitate][day_name][count]}** - Pauză in {minutes}:{seconds}'
				count += 1
			# Se asigura prinatarea corecta a ultimei lectii.
			elif count == len(config.orarul_orelor[imparitate][day_name])-1:
				editable_msg_text += f'\n{config.orarul_orelor[imparitate][day_name][count]}'
				count += 1
			# Se verifica daca acum este pauza.
			elif config.orarul_sunetelor[count][1] <= time_now < config.orarul_sunetelor[count + 1][0]:
				minutes = config.orarul_sunetelor[count + 1][0] - time_now - 1
				seconds = 60 - dt_now.second
				editable_msg_text += f'\n{config.orarul_orelor[imparitate][day_name][count]}'
				editable_msg_text += f'\n**{config.orarul_orelor[imparitate][day_name][count + 1]}** - Lecție in {minutes}:{seconds}'
				count += 2
			else:
				editable_msg_text += f'\n{config.orarul_orelor[imparitate][day_name][count]}'
				count += 1

		await editable_msg.edit(content=editable_msg_text + '\n' + format_dt_now(dt_now))
		await asyncio.sleep(1)


def stop_live_schedule():
	main.num_of_live_schedule_threads += 1


def get_tomorrow_schedule(mention):
	dt_now = datetime.datetime.now(pytz.timezone("Europe/Chisinau"))
	dt_now += datetime.timedelta(days=1)
	day = dt_now.weekday()
	msg_text = f'Salut {mention}. '
	if day == 6:
		dt_now += datetime.timedelta(days=1)
		day = dt_now.weekday()
		msg_text += f'Mâine este duminică.'
	elif day == 5:
		dt_now += datetime.timedelta(days=2)
		day = dt_now.weekday()
		msg_text += f'Mâine este sâmbătă.'

	day_name = config.zilele_scolare[day]
	imparitate = dt_now.isocalendar()[1] % 2
	msg_text += f'Acesta este orarul în săptămână {config.denumirea_paritatii[imparitate]} a lecțiilor pe {day_name}.'
	for lesson in config.orarul_orelor[imparitate][day_name]:
		msg_text += f'\n{lesson}'
	return msg_text


def get_today_schedule(mention):
	dt_now = datetime.datetime.now(pytz.timezone("Europe/Chisinau"))
	day = dt_now.weekday()
	imparitate = dt_now.isocalendar()[1] % 2

	if day == 6:
		return f'Salut {mention}. Azi este duminică.'
	if day == 5:
		return f'Salut {mention}. Azi este sâmbătă.'

	day_name = config.zilele_scolare[day]
	msg_text = f'Acesta este orarul în săptămână {config.denumirea_paritatii[imparitate]} a lecțiilor pe {day_name}.'
	for lesson in config.orarul_orelor[imparitate][day_name]:
		msg_text += f'\n{lesson}'
	return msg_text


def get_yesterday_schedule(mention):
	dt_now = datetime.datetime.now(pytz.timezone("Europe/Chisinau"))
	dt_now += datetime.timedelta(days=-1)
	day = dt_now.weekday()
	msg_text = f'Salut {mention}. '

	if day == 6:
		dt_now += datetime.timedelta(days=-1)
		day = dt_now.weekday()
		msg_text = f'Salut {mention}. Ieri a fost duminică.\n'
	elif day == 5:
		dt_now += datetime.timedelta(days=-2)
		day = dt_now.weekday()
		msg_text = f'Salut {mention}. Ieri a fost sâmbătă.\n'

	day_name = config.zilele_scolare[day]
	imparitate = dt_now.isocalendar()[1] % 2
	msg_text += f'Acesta este orarul în săptămână {config.denumirea_paritatii[imparitate]} a lecțiilor pe {day_name}.'
	for lesson in config.orarul_orelor[imparitate][day_name]:
		msg_text += f'\n{lesson}'
	return msg_text


class Orarul(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(pass_context=True, aliases=['o', 'ora'])
	@main.is_command_allowed
	async def orar(self, ctx):
		# Crearea si trasmiterea mesajului cu optiuni din partea bot-ului.
		embed = discord.Embed(title=f'Funcțiile pentru orar', description=f'Salut {ctx.author.mention}. Mesajul va fi șters peste 1 minut.', color=discord.Colour.gold())
		embed.add_field(name='Lun Mar Mie Joi Vin', value=f'Afișeaza orarul lecțiilor in zilele respective.', inline=True)
		embed.add_field(name='Orarul sunetelor', value=f'Afișeaza orarul sunetelor.', inline=True)
		embed.add_field(name='Orarul total', value=f'Afișeaza orarul lecțiilor pe toată săptămâna.', inline=True)
		embed.add_field(name='Orar live', value=f'Pornește afișarea si actualizare orarului live. În acest orar este scirs lecția curentă, lecția urmatoare si timpul rămas până la ele.', inline=True)
		embed.add_field(name='Oprește orarul', value=f'Oprește ciclul de actualizare a orarului live.', inline=True)
		embed.add_field(name='Mâine Azi Ieri', value=f'Afișeaza orarul concret a lecțiilor in ziua respectivă.', inline=True)

		btn_mon = Button(style=ButtonStyle.grey, label='Lun', id='luni')
		btn_tue = Button(style=ButtonStyle.grey, label='Mar', id='marți')
		btn_wed = Button(style=ButtonStyle.grey, label='Mie', id='miercuri')
		btn_thu = Button(style=ButtonStyle.grey, label='Joi', id='joi')
		btn_fri = Button(style=ButtonStyle.grey, label='Vin', id='vineri')
		week_days = [btn_mon, btn_tue, btn_wed, btn_thu, btn_fri]

		btn_sunet = Button(style=ButtonStyle.blue, label='Orarul sunetelor', id='sunet')
		btn_orarul_total = Button(style=ButtonStyle.grey, label='Orarul total', id='total')
		btn_special = [btn_sunet, btn_orarul_total]

		btn_start_orar_live = Button(style=ButtonStyle.green, label='Orar live', id='start_orar_live')
		btn_stop_orar_live = Button(style=ButtonStyle.red, label='Oprește orarul', id='stop_orar_live')
		btns_orar_live = [btn_start_orar_live, btn_stop_orar_live]

		btn_maine = Button(style=ButtonStyle.green, label='Mâine', id='maine')
		btn_azi = Button(style=ButtonStyle.grey, label='Azi', id='azi')
		btn_ieri = Button(style=ButtonStyle.grey, label='Ieri', id='ieri')
		btn_days = [btn_maine, btn_azi, btn_ieri]

		components = [week_days, btn_special, btns_orar_live, btn_days]
		the_bot_msg = await ctx.channel.send(embed=embed, components=components)

		# Afigurarea functionalitatii butoanelor.
		def check(the_interacted_ctx):
			return the_interacted_ctx.message.id == the_bot_msg.id

		try:
			interacted_ctx = await self.client.wait_for('button_click', timeout=59, check=check)
		except asyncio.TimeoutError:
			await the_bot_msg.delete()
			await ctx.message.delete()
		else:
			await the_bot_msg.delete()
			if interacted_ctx.component.id in config.zilele_scolare:
				await interacted_ctx.channel.send(get_schedule_on_weekday(interacted_ctx.author.mention, interacted_ctx.component.id))
			elif interacted_ctx.component.id == btn_sunet.id:
				await interacted_ctx.channel.send(get_time_schedule(interacted_ctx.author.mention))
			elif interacted_ctx.component.id == btn_orarul_total.id:
				await interacted_ctx.channel.send(embed=get_schedule_on_all_weekdays(interacted_ctx.author.mention))
			elif interacted_ctx.component.id == btn_start_orar_live.id:
				editable_msg = await ctx.channel.send('Loading ...')
				await start_live_schedule(editable_msg, interacted_ctx.author.mention)
			elif interacted_ctx.component.id == btn_stop_orar_live.id:
				stop_live_schedule()
			elif interacted_ctx.component.id == btn_maine.id:
				await interacted_ctx.channel.send(get_tomorrow_schedule(interacted_ctx.author.mention))
			elif interacted_ctx.component.id == btn_azi.id:
				await interacted_ctx.channel.send(get_today_schedule(interacted_ctx.author.mention))
			elif interacted_ctx.component.id == btn_ieri.id:
				await interacted_ctx.channel.send(get_yesterday_schedule(interacted_ctx.author.mention))


def setup(client):
	client.add_cog(Orarul(client))
