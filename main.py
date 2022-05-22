import requests
import config
import os
import os.path

from reportlab.pdfgen import canvas


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
    # isdir = os.path.isdir(i["name"])
    os.chdir(i["name"])
    for j in i["pages"]:
        my_canvas = canvas.Canvas(f"{j['name']}.pdf")
        my_canvas.setFont("Helvetica", 20)
        my_canvas.drawString(100, 750, f"Title: {j['name']}")
        my_canvas.setFont("Helvetica", 12)
        my_canvas.drawString(100, 730, f"Description: {j['text_content']}")
        my_canvas.save()

        if j["parent"] != None:
            for k in i["pages"]:
                if j["parent"] == k["id"]:
                    pass
                    # print(k["name"])
                    # print(True)
                if i["id"] == j["view_id"]:
                    pass
                    # print(i["name"], i["id"], j["name"], j["view_id"])
            # print(f"\t{j['name']} has parent")
            # print(f"\tName: {j['name']}")
            # print(f"\tDescription: {j['text_content']}")
            # print("")

        else:
            pass
            # print(f"\tName: {j['name']}")
            # print(f"\tDescription: {j['text_content']}")
            # print("")

        # my_canvas = canvas.Canvas(f"{j['name']}.pdf")
        # my_canvas.setFont("Helvetica", 20)
        # my_canvas.drawString(100, 750, f"Title: {j['name']}")
        # my_canvas.setFont("Helvetica", 12)
        # my_canvas.drawString(100, 730, f"Description: {j['text_content']}")
        # my_canvas.save()
    os.chdir("../")
