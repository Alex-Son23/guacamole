from pprint import pprint 
import fake_useragent
import httpx
import json
import urllib.parse
import time
from random_username.generate import generate_username



AUTH_URL = "https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
CHECK = "https://gateway.blum.codes/v1/user/username/check"


{
    "1": {
        "phone": "79939818786",
        "proxy": {
            "ip": "104.239.86.231",
            "port": 6141,
            "user": "pbomsduk",
            "password": "t3flfdg7jrxi"
        },
        "user-agent": "",
        "registered": True 
    },
    "2": {
        "phone": "79939818786",
        "proxy": {
            "ip": "104.239.86.231",
            "port": 6141,
            "user": "pbomsduk",
            "password": "t3flfdg7jrxi"
        },
        "user-agent": ""
    }
}

s = "104.239.86.231!6141!pbomsduk!t3flfdg7jrxi|216.173.109.238!6469!pbomsduk!t3flfdg7jrxi|216.173.109.80!6311!pbomsduk!t3flfdg7jrxi|138.128.145.203!6122!pbomsduk!t3flfdg7jrxi|64.137.66.249!5834!pbomsduk!t3flfdg7jrxi|64.137.103.238!6826!pbomsduk!t3flfdg7jrxi|64.137.66.83!5668!pbomsduk!t3flfdg7jrxi|64.137.88.35!6274!pbomsduk!t3flfdg7jrxi|216.173.103.251!6765!pbomsduk!t3flfdg7jrxi|64.137.108.167!5760!pbomsduk!t3flfdg7jrxi|104.239.86.22!5932!pbomsduk!t3flfdg7jrxi|64.137.108.17!5610!pbomsduk!t3flfdg7jrxi|209.99.129.89!6077!pbomsduk!t3flfdg7jrxi|"

# accs = []

# with open("accounts.txt", "r") as f:
#     for i in f.readlines():
#         n = i.split()
#         accs.append(
#             {
#                 "number": n[0],
#                 "proxy": n[1],
#             }
#         )
        


# pprint(accs)
# pprint(proxy)

class Proxy:
    ip: str
    port: str
    user: str
    password: str
    
    def __init__(self, proxy_data: dict) -> None:
        self.ip = proxy_data["ip"]
        self.port = proxy_data["port"]
        self.user = proxy_data["user"]
        self.password = proxy_data["password"]
    
    def __str__(self):
        return f"http://{self.user}:{self.password}@{self.ip}:{self.port}"
    
    
    # def check_proxy(self) -> bool:
    #     with httpx.Client(proxy=self.proxy_link) as client:
    #         resp = client.get('google.com')
    #         if resp.status_code == 200:
    #             return True
    #         else:
    #             return False
    

class Profile:
    proxy: Proxy
    headers: dict
    phone: str
    client: httpx.Client
    user_agent: str
    query: str
    username: str
    referral_token: str
    headers = {
            "content-type": "application/json",
            "accept": "application/json, text/plain, */*",
            "sec-fetch-site": "same-site",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en;q=0.9",
            "sec-fetch-mode": "cors",
            "origin": "https://telegram.blum.codes",
            "sec-fetch-dest": "empty"
        }
    
    def __init__(self, phone: str, proxy_data: dict, query: str, username: str, user_agent: str = "") -> None:
        self.proxy = Proxy(proxy_data)
        self.phone = phone
        self.client = httpx.Client(proxy=str(self.proxy))
        self.user_agent = user_agent
        self.headers["user-agent"] = self.user_agent
        self.username = username
        self.query = query
        self.make_query()
        self.referral_token = urllib.parse.parse_qs(query)["start_param"][0][4:]
    
    def make_query(self):
        current_timestamp = int(time.time())
        encoded_str = self.query
        params = urllib.parse.parse_qs(encoded_str)
        print(params)
        user_json = urllib.parse.unquote(params['user'][0])
        user_data = json.loads(user_json)
        user_data['username'] = self.username
        
        auth_date_json = urllib.parse.unquote(params['auth_date'][0])
        auth_date_data = json.loads(auth_date_json)
        auth_date_data = str(current_timestamp)
        
        
        updated_user_json = json.dumps(user_data)
        updated_user_encoded = urllib.parse.quote(updated_user_json)
        
        updated_auth_data_json = json.dumps(auth_date_data)
        updated_auth_data_encoded = urllib.parse.quote(updated_auth_data_json)
        
        params['user'][0] = updated_user_encoded
        params['auth_date'][0] = updated_auth_data_encoded
        updated_encoded_str = urllib.parse.urlencode(params, doseq=True)
        return updated_encoded_str


class ProfileService:
    def new_profile(self, number: str, proxy: dict):
        with open("data.json", "r") as f:
            accs = json.load(f)
        accs["accs"][number] = {
            "proxy": self.get_free_proxy(),
            "user-agent": fake_useragent.UserAgent(platforms="mobile").random
        }
    
    def use_profile(self, id: int) -> Profile:
        with open("data.json", "r") as f:
            all_accs = json.load(f)
        acc = all_accs[str(id)]
        if not acc["user-agent"]:
            acc["user-agent"] = fake_useragent.UserAgent(platforms="mobile").random
        with open("data.json", "w") as f:
            json.dump(all_accs, f)
        profile = Profile(phone=acc["phone"], proxy_data=acc["proxy"], user_agent=acc["user-agent"], query=acc["query"], username=acc["username"])
        return profile


class RegisterService:

    def __init__(self, profile_service: ProfileService):
        self.profile_service = profile_service

    def create_one(self, id: int):
        requester = self.profile_service.use_profile(id=id)
        
        if not self.check_username(requester, requester.username):
            new_username = generate_username()[0]
            while not self.check_username(requester, new_username):
                new_username = generate_username()[0]
        
        requester.username = new_username
        
        content = {
            "query": requester.query,
            "username": requester.username,
            "referralToken": requester.referral_token
        }
        
        resp = requester.client.post(AUTH_URL, headers=requester.headers, json=json.dumps(content))
        return resp.status
    
    def check_username(self, profile: Profile, username: str):
        resp = profile.client.post(url=CHECK, json=json.dumps({"username": username}), headers=profile.headers)
        print(username, resp)
        return True if resp.status_code == 200 else False     
        


    def create_many(self, ids: list):
        pass


test = RegisterService(ProfileService())
print(test.create_one(id=1))


# register(query='sфыв', username='s', referral_token='asdasd', avatar_file_key='asdasd')    



# class RegisterBLum:
    
#     def __init__(self) -> None:
        
"query_id=AAGixp1fAgAAAKLGnV-kprsj&user=%7B%22id%22%3A5899142818%2C%22first_name%22%3A%22alex%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22humblealx%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1718048498&hash=7ecb5d3709ce4ad5bd504e24faa549473e40eaa8aedf3c1190e290d12b8d368d"


"user=%7B%22id%22%3A7493728124%2C%22first_name%22%3A%22darvin%22%2C%22last_name%22%3A%22tink%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=3051893017577474126&chat_type=private&start_param=ref_vbaxovVKQr&auth_date=1718050772&hash=54935857deb179557aabc58805fd2df0f0c6210af8084ff0bf87c08b67b90068"
# юзер нейм после

{"query":"user=%7B%22id%22%3A6664852258%2C%22first_name%22%3A%22-%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22superniggamega%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=7531170506392353065&chat_type=private&start_param=ref_vbaxovVKQr&auth_date=1717864586&hash=0ae580c05285c5e1fa88d165d8a79d96a73b4a209cce8d41c323afc1e3372fae","username":"superniggamega","referralToken":"vbaxovVKQr","avatarFileKey":"https://subscription.blum.codes/user/avatar/6664852258"}




# class Accounts:
    # def new_account(self, number: str):
    #     with open("data.json", "r") as f:
    #             accs = json.loads(f)
    #     accs["accs"][number] = {
    #         "proxy": self.get_free_proxy(),
    #         "user-agent": fake_useragent.UserAgent(platforms="mobile").random
    #     }
    #     with open("data.json", "r") as f:
    #         json.dumps(accs, f)
    
    # def get_free_proxy(self):
    #     proxies = []

    #     with open("proxy.txt", "r") as f:
    #         for i in f.readlines():
    #             n = i.split()
    #             print(n)
    #             proxies.append(
    #                 {
    #                     "ip": n[0],
    #                     "port": n[1],
    #                     "user": n[2],
    #                     "password": n[3]
    #                 }
    #             )
        
    #     accs = []
        
    #     with open("data.json", "r") as f:
    #         accs = json.loads(f)
        
    #     for proxy in proxies:
    #         if proxy not in [x["proxy"] for x in accs.items()]:
    #             if Proxy(proxy).check_proxy:
    #                 return proxy


# class Registration:
    # headers = {
    #         "content-type": "application/json",
    #         "accept": "application/json, text/plain, */*",
    #         "sec-fetch-site": "same-site",
    #         "accept-encoding": "gzip, deflate, br",
    #         "accept-language": "en-GB,en;q=0.9",
    #         "sec-fetch-mode": "cors",
    #         "origin": "https://telegram.blum.codes",
    #         "sec-fetch-dest": "empty"
    #     }



    # def check_username(self, username: str):
        
    #     headers = {
    #         "Accept": "application/json, text/plain, */*",
    #         "Accept-Encoding": "gzip, deflate, br",
    #         "Accept-Language": "ru",
    #         "Connection": "keep-alive",
    #         "Content-Type": "application/json",
    #         "Host": "gateway.blum.codes",
    #         "Origin": "https://telegram.blum.codes",
    #         "Sec-Fetch-Dest": "empty",
    #         "Sec-Fetch-Mode": "cors",
    #         "Sec-Fetch-Site": "same-site"
    #     }


    # async def register(query: str, referral_token: str, avatar_file_key: str, username: str):
    #     headers = {
    #         "content-type": "application/json",
    #         "accept": "application/json, text/plain, */*",
    #         "sec-fetch-site": "same-site",
    #         "accept-encoding": "gzip, deflate, br",
    #         "accept-language": "en-GB,en;q=0.9",
    #         "sec-fetch-mode": "cors",
    #         "origin": "https://telegram.blum.codes",
    #         "content-length": 507, #?????
    #         "sec-fetch-dest": "empty"
    #     }
    #     user_agent = fake_useragent.UserAgent(platforms="mobile").random
        
    #     headers["user-agent"] = user_agent
        
        
    #     data = {
    #         "query": query,
    #         "username": username,
    #         "referralToken": referral_token,
    #         "avatarFileKey": avatar_file_key,
    #         }
        
    #     pprint(headers)
    #     pprint(data)
        
    #     # aiohttp.a
    
