import os


orarul_sunetelor = [[480, 540], [550, 610], [620, 680], [690, 750]]

orarul_orelor = [
	{
		'luni': ['1. Fizica', '2. Decizii M. S. V.', '3. Dispozitive E.', '4. Geografia'],
		'marți': ['1. Ed. Fizica', '2. L. Română'],
		'miercuri': ['1. Fizica', '2. Informatica', '3. L. Străină', '4. Matematica'],
		'joi': ['1. Matematica', '2. Surse A.', '3. L. Română', '4. Surse A.'],
		'vineri': ['1. Linii de T.', '2. Matematica', '3. Dispozitive E.']
	},
	{
		'luni': ['1. Fizica', '2. Decizii M. S. V.', '3. Dispozitive E.', '4. Istoria'],
		'marți': ['1. Ed. Fizica', '2. L. Română'],
		'miercuri': ['1. D. P.', '2. Informatica', '3. L. Străină', '4. Matematica'],
		'joi': ['1. Ed. pentru soc.', '2. Surse A.', '3. L. Română', '4. Surse A.'],
		'vineri': ['1. Linii de T.', '2. Matematica', '3. Dispozitive E.', '4. Linii de T.']
	}
]

orarul_total_al_orelor = {
		'luni': '\n1. Fizica\n2. Decizii M. S. V.\n3. Dispozitive E.\n4. Istoria\\Geografia',
		'marți': '\n1. Ed. Fizica\n2. L. Română',
		'miercuri': '\n1. D. P.\\Fizica\n2. Informatica\n3. L. Străină\n4. Matematica',
		'joi': '\n1. Ed. pentru soc.\\Matematica\n2. Surse A.\n3. L. Română\n4. Surse A.',
		'vineri': '\n1. Linii de T.\n2. Matematica\n3. Dispozitive E.\n4. Linii de T.\\Nimic'}

denumirea_paritatii = ['pară', 'impară']

zilele_scolare = ['luni', 'marți', 'miercuri', 'joi', 'vineri']

server_owner = 'Daito#8141'

command_channel_id = 753531622757761105

music_channel_id = 754018313029288127


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
