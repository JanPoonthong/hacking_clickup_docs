import requests
import config

headers = {
    "Authorization": f"Bearer {config.auth_token}",
    "Content-Type": "application/json",
}

response = requests.get(
    "https://app.clickup.com/docs/v1/team/36742991/docs?include_archived=false&search=&page_search=&dir=desc&section=all",
    headers=headers,
)

for i in response.json()["views"]:
    print(f"Big folder: {i['name']}")
    for j in i["pages"]:
        if j["parent"] != None:
            for k in i["pages"]:
                if j["parent"] == k["id"]:
                    print(True)
            print(f"\t{j['name']} has parent")
            print(f"\tName: {j['name']}")
            print(f"\tDescription: {j['text_content']}")
            print("")
        else:
            print(f"\tName: {j['name']}")
            print(f"\tDescription: {j['text_content']}")
            print("")
