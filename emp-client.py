import json, os, re, requests

URL_AUTH = "https://www.empatica.com/connect/authenticate.php"
URL_SESSIONS_MAIN = "https://www.empatica.com/connect/sessions.php"
URL_SESSIONS_LIST = "https://www.empatica.com/connect/connect.php/users/{uid}/sessions?from=0&to=999999999999"

OUT_FILE = "out.csv"
DELIM = ","

s = requests.Session()

# Authenticate
auth_info = {"username": os.environ["E4_USER"], "password": os.environ["E4_PASS"]}
s.post(URL_AUTH, auth_info).raise_for_status()

# Get user ID
resp = s.get(URL_SESSIONS_MAIN)
resp.raise_for_status()
user_id = re.search(r"userId = ([0-9]*);", resp.text).group(1)

# List all sessions
resp = s.get(URL_SESSIONS_LIST.format(uid = user_id))
resp.raise_for_status()
sessions_list = json.loads(resp.text)

if sessions_list:
	f = open(OUT_FILE, "w")
	f.write(DELIM.join(sessions_list[0].keys()))
	for session in sessions_list:
		f.write("\n" + DELIM.join(session.values()))


