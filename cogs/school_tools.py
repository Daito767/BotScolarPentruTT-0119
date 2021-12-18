import discord
import os
import discord.ext
import config
import asyncio
from discord.ext import commands, tasks
import main
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption


class SchoolTools(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(pass_context=True, aliases=['converteaza'])
	@main.is_command_allowed
	async def convert(self, ctx, *args):
		enum_systems_len = {'b': 2, 'q': 8, 'd': 10, 'h': 16}
		num_symbols = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

		cmds = args[0]
		default_value = args[1]
		result = ''
		i = 0

		while i < len(cmds) - 1:
			sys_now = cmds[i]
			sys_next = cmds[i + 1]
			i += 1

			if sys_now == 'd':
				value = int(default_value)
				rest_result = ''
				result += f'\n{sys_now}->{sys_next}'
				while value > 0:
					new_value = int(value / enum_systems_len[sys_next])
					new_rest = rest = value - new_value * enum_systems_len[sys_next]
					if rest > 9:
						new_rest = f'{rest} - {chr(rest + 55)}'
						rest = chr(rest + 55)

					result += f'\n{value} : {enum_systems_len[sys_next]} = {new_value} rest {new_rest}'
					rest_result = f'{rest}' + rest_result
					value = new_value

				result += f'\nR: {default_value} -> {rest_result}\n-------------------'
				default_value = rest_result

			elif sys_next == 'd':
				n = 0
				result_nums = []
				result += f'\n\n{sys_now} -> {sys_next}\n'
				value = 0
				while n < len(default_value):
					current_num = num_symbols[default_value[n]]
					power = len(default_value) - n - 1
					result += f'({num_symbols[default_value[n]]}*{enum_systems_len[sys_now]}^{power}) + '
					new_value = num_symbols[default_value[n]] * enum_systems_len[sys_now] ** power

					if new_value > 0:
						result_nums.append(num_symbols[default_value[n]] * enum_systems_len[sys_now] ** power)

					n += 1

				result = result[:-3]
				result += ' = '
				for result_num in result_nums:
					value += result_num
					result += f'{result_num} + '

				result = result[:-3]
				result += f' = {value}'
				result += f'\nR: {default_value} -> {value}\n-------------------'
				default_value = value

		await ctx.channel.send(result)


def setup(client):
	client.add_cog(SchoolTools(client))
