import requests
import config

login_url = "https://app.clickup.com/v1/login?include_teams=true"
login_header = {"Authorization": f"{config.basic_token}"}
auth_token = requests.post(login_url, headers=login_header).json()["token"]

headers = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json",
}

response = requests.get(
    "https://app.clickup.com/docs/v1/team/36742991/docs?include_archived=false&search=&page_search=&order_by=date_viewed&dir=desc&section=all",
    headers=headers,
)

data = response.json()["views"]


for i in range(len(data)):
    print(data[i]["pages"][0]["name"])
    print(data[i]["pages"][0]["text_content"])
