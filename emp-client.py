import argparse, json, os, re, requests

URL_AUTH = 'https://www.empatica.com/connect/authenticate.php'
URL_SESSIONS_MAIN = 'https://www.empatica.com/connect/sessions.php'
URL_SESSIONS_LIST = 'https://www.empatica.com/connect/connect.php/users/{uid}/sessions?from=0&to=999999999999'
URL_DOWNLOAD = 'https://www.empatica.com/connect/download.php?id={id}'
DEFAULT_CSV_FILE = 'out.csv'
DEFAULT_OUT_PATH = '.'
DELIM = ','

parser = argparse.ArgumentParser(description='Empatica Client')

parser.add_argument('-u', '--user',  action='store')
parser.add_argument('-p', '--pwd', action='store')

parser.add_argument('-a', '--all_sessions',  action='store_true')
parser.add_argument('-i', '--session_id',  action='store')
parser.add_argument('-l', '--sessions_list', action='store_true')

parser.add_argument('-o', '--out', action='store')


args = parser.parse_args()

s = requests.Session()

# Authenticate
if not (args.user or 'E4_USER' in os.environ) or not (args.pwd or 'E4_PWD' in os.environ):
	raise Exception('Credentials must be specified by params or environ variables (E4_USER, E4_PWD)')
user = args.user or os.environ['E4_USER']
pwd = args.pwd or os.environ['E4_PWD']

auth_info = {'username': user, 'password': pwd}
s.post(URL_AUTH, auth_info).raise_for_status()

# Get user ID
resp = s.get(URL_SESSIONS_MAIN)
resp.raise_for_status()
user_id = re.search(r'userId = ([0-9]*);', resp.text).group(1)

# List all sessions
resp = s.get(URL_SESSIONS_LIST.format(uid = user_id))
resp.raise_for_status()
sessions_list = json.loads(resp.text)


if args.sessions_list:
	if sessions_list:
		with open(args.out or DEFAULT_CSV_FILE, 'w') as f:
			f.write(DELIM.join(sessions_list[0].keys()))
			for session in sessions_list:
				f.write('\n' + DELIM.join(session.values()))
elif args.session_id:
	print('Downloading %s...' % args.session_id)
	resp = s.get(URL_DOWNLOAD.format(id=args.session_id))
	with open(args.out or '%s%s.zip' % (DEFAULT_OUT_PATH, args.session_id), 'wb') as f:
		f.write(resp.content)

elif args.all_sessions:
	for session in sessions_list:
		print('Downloading %s...' % session['id'])
		resp = s.get(URL_DOWNLOAD.format(id=session['id']))
		with open('%s/%s.zip' % (args.out or DEFAULT_OUT_PATH, session['id']), 'wb') as f:
			f.write(resp.content)

