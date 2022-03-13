import os

orarul_sunetelor = [[480, 560], [570, 650], [660, 740], [760, 840]]

orarul_orelor = [
	{
		'luni': ['1. Ed. Fizică', '2. L. Străină', '3. isteme T. M.'],
		'marți': ['1. Nimic', '2. Filosofie', '3. Matematica', '4. Bazele L. D.'],
		'miercuri': ['1. L. Română', '2. Informatica', '3. Sisteme R. TV', '4. L. Română'],
		'joi': ['1. Tehn. Com.', '2. Matematica', '3. Istoria'],
		'vineri': ['1. Nimic', '2. Sisteme T. M.', '3. Fizica', '4. Fizica']
	},
	{
		'luni': ['1. Ed. Fizică', '2. L. Străină', '3. isteme T. M.'],
		'marți': ['1. Geografia', '2. Filosofie', '3. Matematica', '4. Bazele L. D.'],
		'miercuri': ['1. Ed. pentru soc.', '2. Informatica', '3. Sisteme R. TV', '4. L. Română'],
		'joi': ['1. Tehn. Com.', '2. Matematica', '3. Matematica'],
		'vineri': ['1. Nimic', '2. Sisteme T. M.', '3. D. P.', '4. Fizica']
	}
]

orarul_total_al_orelor = {
		'luni': '\n`1. Ed. Fizică`\n`2. L. Străină`\n`3. Sisteme T. M.`',
		'marți': '\n`1. Geografia\\Nimic`\n`2. Filosofie`\n`3. Matematica`\n`4. Bazele L. D.`',
		'miercuri': '\n`1. Ed. pentru soc.\\L. Română`\n`2. Informatica`\n`3. Sisteme R. TV`\n`4. L. Română`',
		'joi': '\n`1. Tehn. Com.`\n`2. Matematica`\n`3. Matematica\\Istoria`',
		'vineri': '\n`1. Nimic`\n`2. Sisteme T. M.`\n`3. D. P.\\Fizica`\n`4. Fizica`'}

denumirea_paritatii = ['pară', 'impară']

zilele_scolare = ['luni', 'marți', 'miercuri', 'joi', 'vineri']

server_owner = 'Daito#8141'

command_channel_id = 753531622757761105

music_channel_id = 754018313029288127

bot_version = '3.0'


TOKEN = ''
db_name = ''
db_host = ''
db_password = ''
db_port = ''
db_user = ''

is_local_run = False
if 'local_config.py' in os.listdir('.'):
	import local_config
	TOKEN = local_config.TOKEN
	db_name = local_config.db_name
	db_host = local_config.db_host
	db_password = local_config.db_password
	db_port = local_config.db_port
	db_user = local_config.db_user
	is_local_run = True
else:
	TOKEN = os.getenv("TOKEN")
	db_name = os.getenv("db_name")
	db_host = os.getenv("db_host")
	db_password = os.getenv("db_password")
	db_port = os.getenv("db_port")
	db_user = os.getenv("db_user")
