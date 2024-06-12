import urllib.parse
import json
import time
import httpx
# Исходная строка
encoded_str = "user=%7B%22id%22%3A7493728124%2C%22first_name%22%3A%22darvin%22%2C%22last_name%22%3A%22tink%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=3051893017577474126&chat_type=private&start_param=ref_vbaxovVKQr&auth_date=1718050772&hash=54935857deb179557aabc58805fd2df0f0c6210af8084ff0bf87c08b67b90068"

# Парсим строку на отдельные параметры
params = urllib.parse.parse_qs(encoded_str)
print(params)

# Декодируем значение параметра 'user'
user_json = urllib.parse.unquote(params['user'][0])

ref = params["start_param"][0][4:]
print(ref)

# Преобразуем JSON-строку в словарь Python
user_data = json.loads(user_json)

current_timestamp = int(time.time())
# Меняем значение 'username'
user_data['username'] = 'new_username'

# Преобразуем обновленный словарь обратно в JSON-строку
updated_user_json = json.dumps(user_data)

# Кодируем JSON-строку
updated_user_encoded = urllib.parse.quote(updated_user_json)

# Обновляем параметр 'user' в словаре параметров
params['user'][0] = updated_user_encoded
auth_date_json = urllib.parse.unquote(params['user'][0])
auth_date_data = json.loads(auth_date_json)
auth_date_data['auth_date'] = str(current_timestamp)
updated_auth_data_json = json.dumps(auth_date_data)
updated_auth_data_encoded = urllib.parse.quote(updated_auth_data_json)
params['auth_date'][0] = updated_auth_data_encoded

# Собираем строку с обновленными параметрами
updated_encoded_str = urllib.parse.urlencode(params, doseq=True)

# Выводим обновленную строку
print(updated_encoded_str)

"query_id=AAGtmaIWAwAAAK2ZohZ7Lkp6&user=%7B%22id%22%3A6822205869%2C%22first_name%22%3A%22aleksandr%22%2C%22last_name%22%3A%22%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1718150955&hash=e36d1ae00feccd3e8382029c461d4b35aeeda93837a85df390abd425864a1ad8"


with open("data.json", "r") as f:
        all_accs = json.load(f)

print(all_accs)

# http://pbomsduk:t3flfdg7jrxi@104.239.86.231:6141
# print(httpx.Client(proxy="http://pbomsduk:t3flfdg7jrxi@104.239.86.231:6141").post("https://gateway.blum.codes/v1/user/username/check", content=json.dumps({"username": "wearyLion9"}), headers={'accept': 'application/json, text/plain, */*',
#  'accept-encoding': 'gzip, deflate, br',
#  'accept-language': 'en-GB,en;q=0.9',
#  'content-type': 'application/json',
#  'origin': 'https://telegram.blum.codes',
#  'sec-fetch-dest': 'empty',
#  'sec-fetch-mode': 'cors',
#  'sec-fetch-site': 'same-site',
#  'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) '
#                'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 '
#                'Mobile/15E148 Safari/604.1 OPX/2.2.0'}))


print(httpx.Client(proxy="http://pbomsduk:t3flfdg7jrxi@104.239.86.231:6141").get("https://pypi.org", ))
