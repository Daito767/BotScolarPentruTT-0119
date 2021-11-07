import os

orarul_sunetelor = [[480, 560], [570, 650], [660, 740], [760, 840]]

orarul_orelor = [
	{
		'luni': ['1. Nimic', '2. L. Străină', '3. Comunicații O.', '4. Comunicații O.'],
		'marți': ['1. L. Română', '2. C. A. D.', '3. Matematica'],
		'miercuri': ['1. Geografia', '2. Cominicații S. R.', '3. Ed. Fizică', '4. Fizica'],
		'joi': ['1. Informatica', '2. C. A. D.', '3. Matematica', '4. Matematica'],
		'vineri': ['3. Comunicații O.', '4. Fizica']
	},
	{
		'luni': ['1. Istoria', '2. L. Străină', '3. Comunicații O.', '4. Comunicații O.'],
		'marți': ['1. L. Română', '2. C. A. D.', '3. Matematica', '4. D. P.'],
		'miercuri': ['1. Ed. pentru soc.', '2. Cominicații S. R.', '3. Ed. Fizică'],
		'joi': ['1. Informatica', '2. C. A. D.', '3. Matematica', '4. L. Română'],
		'vineri': ['3. Comunicații O.', '4. Fizica']
	}
]

orarul_total_al_orelor = {
		'luni': '\n`1. Istoria\\Nimic`\n`2. L. Străină`\n`3. Comunicații O.`\n`4. Comunicații O.`',
		'marți': '\n`1. L. Română`\n`2. C. A. D.`\n`3. Matematica`\n`4. D. P.\\Nimic`',
		'miercuri': '\n`1. Ed. pentru soc.\\Geografia`\n`2. Cominicații S. R.`\n`3. Ed. Fizică`\n`4. Nimic\\Fizica`',
		'joi': '\n`1. Informatica`\n`2. C. A. D.`\n`3. Matematica`\n`4. L. Română\\Matematica`',
		'vineri': '\n`3. Comunicații O.`\n`4. Fizica`'}

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
