import os

orarul_sunetelor = [[480, 560], [570, 650], [660, 740], [760, 840]]

orarul_orelor = [
	{
		'luni': ['1. Nimic', '2. L. Străină', '3. Ed. Fizică', '4. L. Română'],
		'marți': ['1. Nimic', '2. Sisteme T. M.', '3. Matematica', '4. Filosofie'],
		'miercuri': ['1. L. Română', '2. Sisteme R. TV', '3. Bazele L. D.', '4. Tehn. Com.'],
		'joi': ['1. Informatica', '2. Fizica', '3. Matematica', '4. Matematica'],
		'vineri': ['1. Fizica', '2. Sisteme T. M.']
	},
	{
		'luni': ['1. Istoria', '2. L. Străină', '3. Ed. Fizică', '4. L. Română'],
		'marți': ['1. Geografia', '2. Sisteme T. M.', '3. Matematica', '4. Filosofie'],
		'miercuri': ['1. Ed. pentru soc.', '2. Sisteme R. TV', '3. Bazele L. D.', '4. Tehn. Com.'],
		'joi': ['1. Informatica', '2. Fizica', '3. Matematica'],
		'vineri': ['1. D. P.', '2. Cominicații S. R.']
	}
]

orarul_total_al_orelor = {
		'luni': '\n`1. Istoria\\Nimic`\n`2. L. Străină`\n`3. Ed. Fizică`\n`4. L. Română`',
		'marți': '\n`1. Geografia\\Nimic`\n`2. Sisteme T. M.`\n`3. Matematica`\n`4. Filosofie`',
		'miercuri': '\n`1. Ed. pentru soc.\\L. Română`\n`2. Sisteme R. TV`\n`3. Bazele L. D.`\n`4. Tehn. Com.`',
		'joi': '\n`1. Informatica`\n`2. Fizica`\n`3. Matematica`\n`4. Nimic\\Matematica`',
		'vineri': '\n`1. D. P.\\Fizica`\n`2. Sisteme T. M.`'}

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
