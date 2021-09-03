import os

orarul_sunetelor = [[480, 550], [560, 630], [640, 710], [720, 790]]

orarul_orelor = [
	{
		'luni': ['1. Istoria', '2. L. Străină', '3. Comunicații O.', '4. D. P.'],
		'marți': ['1. L. Română', '2. C. A. D.', '3. Comunicații O.', '4. Matematica'],
		'miercuri': ['1. Geografia', '2. Comunicații O.', '3. Informatica', '4. L. Română'],
		'joi': ['1. C. A. D.', '2. Matematica', '3. Matematica'],
		'vineri': ['1. Ed. Fizică', '2. Cominicații S. R.', '3. Fizica']
	},
	{
		'luni': ['1. Istoria', '2. L. Română', '3. Comunicații O.'],
		'marți': ['1. Nimic', '2. C. A. D.', '3. Comunicații O.', '4. Matematica'],
		'miercuri': ['1. Ed. pentru soc.', '2. Comunicații O.', '3. Informatica', '4. L. Română'],
		'joi': ['1. C. A. D.', '2. Matematica'],
		'vineri': ['1. Ed. Fizică', '2. Cominicații S. R.', '3. Fizica']
	}
]

orarul_total_al_orelor = {
		'luni': '\n`1. Istoria\\Fizica`\n`2. L. Străină`\n`3. Comunicații O.`\n`4. Nimic\\D. P.`',
		'marți': '\n`1. Nimic\\L. Română`\n`2. C. A. D.`\n`3. Comunicații O.`\n`4. Matematica`',
		'miercuri': '\n`1. Ed. pentru soc.\\Geografia`\n`2. Comunicații O.`\n`3. Informatica`\n`4. L. Română`',
		'joi': '\n`1. C. A. D.`\n`2. Matematica`\n`3. Nimic\\Matematica`',
		'vineri': '\n`1. Ed. Fizică`\n`2. Cominicații S. R.`\n`4. Fizica`'}

denumirea_paritatii = ['pară', 'impară']

zilele_scolare = ['luni', 'marți', 'miercuri', 'joi', 'vineri']

server_owner = 'Daito#8141'

command_channel_id = 753531622757761105

music_channel_id = 754018313029288127

bot_version = '2.7'


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
