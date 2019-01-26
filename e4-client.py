import argparse
import json
import os
import re
import requests


class E4Connect:
    URL_AUTH = 'https://www.empatica.com/connect/authenticate.php'
    URL_SESSIONS_MAIN = 'https://www.empatica.com/connect/sessions.php'
    URL_SESSIONS_LIST = 'https://www.empatica.com/connect/connect.php/users/{uid}/sessions?from=0&to=999999999999'
    URL_DOWNLOAD = 'https://www.empatica.com/connect/download.php?id={id}'
    URL_PURCHASED_DEVS = 'https://www.empatica.com/connect/connect.php/users/{uid}/api/purchasedDevices'

    def __init__(self, user, pwd):
        self.s = requests.Session()
        self.user_id = None
        self.auth(user, pwd)

    def auth(self, user, pwd):
        auth_info = {'username': user, 'password': pwd}
        self.s.post(E4Connect.URL_AUTH, auth_info).raise_for_status()

        resp = self.s.get(E4Connect.URL_SESSIONS_MAIN)
        resp.raise_for_status()
        self.user_id = re.search(r'userId = ([0-9]*);', resp.text).group(1)

    def sessions_list(self):
        resp = self.s.get(E4Connect.URL_SESSIONS_LIST.format(uid=self.user_id))
        resp.raise_for_status()
        return json.loads(resp.text)

    def download_session(self, session_id, file_path):
        resp = self.s.get(E4Connect.URL_DOWNLOAD.format(id=session_id))
        file_path = os.path.join(file_path, '%s.zip' % session_id) if os.path.isdir(file_path) else file_path
        with open('%s' % file_path, 'wb') as f:
            f.write(resp.content)

    def purchased_devices(self):
        resp = self.s.get(E4Connect.URL_PURCHASED_DEVS.format(uid=self.user_id))
        resp.raise_for_status()
        return json.loads(resp.text)


if __name__ == "__main__":
    DEFAULT_CSV_SESSIONS = 'sessions.csv'
    DEFAULT_CSV_DEVICES = 'devices.csv'
    DEFAULT_OUT_PATH = '.'
    DELIM = ','

    parser = argparse.ArgumentParser(description='Empatica Client')

    parser.add_argument('-u', '--user', action='store', help='Username.')
    parser.add_argument('-p', '--pwd', action='store', help='Password.')

    parser.add_argument('-a', '--all_sessions', action='store_true', help='Downloads all sessions of a user.')
    parser.add_argument('-i', '--session_id', action='store', help='Downloads a specific session.')
    parser.add_argument('-l', '--sessions_list', action='store_true',
                        help='Downloads the list of sessions in CSV format.')
    parser.add_argument('-d', '--purchased_devs', action='store_true',
                        help='Downloads a list of purchased devices in CSV format.')

    parser.add_argument('-o', '--out', action='store',
                        help='Output file (for single files) or path (for multiple files).')

    args = parser.parse_args()

    # Retrieve credentials
    if not (args.user or 'E4_USER' in os.environ) or not (args.pwd or 'E4_PWD' in os.environ):
        raise Exception('Credentials must be specified by params or environ variables (E4_USER, E4_PWD)')
    user = args.user or os.environ['E4_USER']
    pwd = args.pwd or os.environ['E4_PWD']

    # Authenticate
    e4c = E4Connect(user, pwd)

    if args.sessions_list or args.all_sessions:
        sessions_list = e4c.sessions_list()

        if args.sessions_list:
            if sessions_list:
                args.out = os.path.join(args.out, DEFAULT_CSV_SESSIONS) if args.out and os.path.isdir(args.out) else None
                with open(args.out or DEFAULT_CSV_SESSIONS, 'w') as f:
                    f.write(DELIM.join(sessions_list[0].keys()))
                    for session in sessions_list:
                        f.write('\n' + DELIM.join(session.values()))
        elif args.all_sessions:
            for session in sessions_list:
                print('Downloading %s...' % session['id'])
                e4c.download_session(session['id'], args.out or DEFAULT_OUT_PATH)

    elif args.session_id:
        print('Downloading %s...' % args.session_id)
        e4c.download_session(args.session_id, args.out or DEFAULT_OUT_PATH)

    elif args.purchased_devs:
        purchases_list = e4c.purchased_devices()

        if purchases_list:

            args.out = os.path.join(args.out, DEFAULT_CSV_DEVICES) if args.out and os.path.isdir(args.out) else None
            with open(args.out or DEFAULT_CSV_DEVICES, 'w') as f:
                f.write(DELIM.join(purchases_list[0].keys()))
                for p in purchases_list:
                    f.write('\n' + DELIM.join(p.values()))
