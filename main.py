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

data = response.json()
data_view = response.json()["views"]

for i in range(len(data_view)):
    print(f"Big folder: {data_view[i]['name']}")
    num_data_view_page = len(data_view[i]["pages"])
    for j in range(num_data_view_page):
        if data_view[i]['pages'][j]['parent'] != None:
            print(f"\t{data_view[i]['pages'][j]['name']} has parent")
            print(f"\tName: {data_view[i]['pages'][j]['name']}")
            print(f"\tDescription: {data_view[i]['pages'][j]['text_content']}")
            print("")
        else:
            print(f"\tName: {data_view[i]['pages'][j]['name']}")
            print(f"\tDescription: {data_view[i]['pages'][j]['text_content']}")
            print("")
