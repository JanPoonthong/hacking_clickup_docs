import os
import os.path
import requests
from reportlab.pdfgen import canvas

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
    try:
        os.mkdir(f"{i['name']}")
        print("Directory ", f"{i['name']}", " Created ")
    except FileExistsError:
        print("Directory ", f"{i['name']}", " already exists")

for i in response.json()["views"]:
    os.chdir(i["name"])
    for j in i["pages"]:
        my_canvas = canvas.Canvas(f"{j['name']}.pdf")
        my_canvas.setFont("Helvetica", 20)
        my_canvas.drawString(100, 750, f"Title: {j['name']}")
        my_canvas.setFont("Helvetica", 12)
        my_canvas.drawString(100, 730, f"Description: {j['text_content']}")
        my_canvas.save()
    os.chdir("../")
