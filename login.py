import requests
import config


def login_clickup():
    login_url = "https://app.clickup.com/v1/login?include_teams=true"
    login_header = {"Authorization": f"Basic {config.basic_token}"}
    auth_token = requests.post(login_url, headers=login_header).json()["token"]
    return auth_token


auth_token = login_clickup()
print(auth_token)
